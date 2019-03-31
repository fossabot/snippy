#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Snippy - command, solution, reference and code snippet manager.
#  Copyright 2017-2019 Heikki J. Laaksonen  <laaksonen.heikki.j@gmail.com>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""base: Base class for the resource API endpoints."""

from snippy.cause import Cause
from snippy.config.config import Config
from snippy.config.source.api import Api
from snippy.logger import Logger
from snippy.server.rest.generate import Generate
from snippy.server.rest.validate import Validate


class ApiResource(object):
    """Base class for the resource API endpoints."""

    # JSON API v1.0 specification media header. Additional character set is a
    # deviation from the specification. It is considered very useful so that
    # client always knows explicitly how to decode HTTP responses.
    MEDIA_JSON_API = 'application/vnd.api+json; charset=UTF-8'

    def __init__(self, content=None, category=None):
        self._logger = Logger.get_logger(__name__)
        self._category = category
        self._content = content

    @Logger.timeit(refresh_oid=True)
    def on_post(self, request, response, **kwargs):  # pylint: disable=unused-argument
        """Create new resource.

        Args:
            request (object): Falcon Request.
            response (object): Falcon Response.
        """

        self._logger.debug('run: %s %s', request.method, request.uri)
        collection = Validate.json_object(request)
        for resource in collection:
            api = Api(self._category, Api.CREATE, resource)
            Config.load(api)
            self._content.run()
        if Cause.is_ok():
            response.content_type = ApiResource.MEDIA_JSON_API
            response.body = Generate.collection(self._content.collection, request, response)
            response.status = Cause.http_status()
        else:
            response.content_type = ApiResource.MEDIA_JSON_API
            response.body = Generate.error(Cause.json_message())
            response.status = Cause.http_status()

        Cause.reset()
        self._logger.debug('end: %s %s', request.method, request.uri)

    @Logger.timeit(refresh_oid=True)
    def on_put(self, request, response, **kwargs):  # pylint: disable=unused-argument,no-self-use
        """Update content.

        Args:
            request (object): Falcon Request.
            response (object): Falcon Response.
        """

        ApiNotImplemented.send(request, response)

    @Logger.timeit(refresh_oid=True)
    def on_get(self, request, response, sall=None, stag=None, sgrp=None):
        """Search resources.

        Args:
            request (object): Falcon Request.
            response (object): Falcon Response.
            sall (str): Search all ``sall`` path parameter.
            stag (str): Search tags ``stag`` path parameter.
            sgrp (str): Search groups ``sgrp`` path parameter.
        """

        self._logger.debug('run: %s %s', request.method, request.uri)
        if sall:
            request.params['sall'] = sall
        if stag:
            request.params['stag'] = stag
        if sgrp:
            request.params['sgrp'] = sgrp
        api = Api(self._category, Api.SEARCH, request.params)
        Config.load(api)
        self._content.run()
        if not self._content.collection and Config.search_limit != 0:
            Cause.push(Cause.HTTP_NOT_FOUND, 'cannot find resources')
        if Cause.is_ok():
            response.content_type = ApiResource.MEDIA_JSON_API
            response.body = Generate.collection(self._content.collection, request, response, pagination=True)
            response.status = Cause.http_status()
        else:
            response.content_type = ApiResource.MEDIA_JSON_API
            response.body = Generate.error(Cause.json_message())
            response.status = Cause.http_status()

        Cause.reset()
        self._logger.debug('end: %s %s', request.method, request.uri)

    @Logger.timeit(refresh_oid=True)
    def on_delete(self, request, response, **kwargs):  # pylint: disable=unused-argument
        """Delete resource.

        Args:
            request (object): Falcon Request.
            response (object): Falcon Response.
        """

        self._logger.debug('run: %s %s', request.method, request.uri)
        Cause.push(Cause.HTTP_NOT_FOUND, 'cannot delete content without identified resource')
        response.content_type = ApiResource.MEDIA_JSON_API
        response.body = Generate.error(Cause.json_message())
        response.status = Cause.http_status()

        Cause.reset()
        self._logger.debug('end: %s %s', request.method, request.uri)

    @staticmethod
    @Logger.timeit(refresh_oid=True)
    def on_options(_, response, sall=None, stag=None, sgrp=None):  # pylint: disable=unused-argument
        """Respond with allowed methods.

        Args:
            request (object): Falcon Request.
            response (object): Falcon Response.
            sall (str): Search all ``sall`` path parameter.
            stag (str): Search tags ``stag`` path parameter.
            sgrp (str): Search groups ``sgrp`` path parameter.
        """

        response.status = Cause.HTTP_200
        response.set_header('Allow', 'DELETE,GET,OPTIONS,POST')


class ApiResourceId(object):
    """Access resources with resource ID."""

    def __init__(self, content, category):
        self._logger = Logger.get_logger(__name__)
        self._category = category
        self._content = content

    @Logger.timeit(refresh_oid=True)
    def on_post(self, request, response, identity):
        """Update resource.

        Args:
            request (object): Falcon Request.
            response (object): Falcon Response.
            identity (str): Partial or full message digest or UUID.
        """

        self._logger.debug('run: %s %s', request.method, request.uri)
        if request.get_header('x-http-method-override', default='post').lower() == 'put':
            self.on_put(request, response, identity)
        elif request.get_header('x-http-method-override', default='post').lower() == 'patch':
            self.on_patch(request, response, identity)
        elif request.get_header('x-http-method-override', default='post').lower() == 'delete':
            self.on_delete(request, response, identity)
        else:
            Cause.push(Cause.HTTP_BAD_REQUEST, 'cannot create resource with id, use x-http-method-override to override the request')
            response.content_type = ApiResource.MEDIA_JSON_API
            response.body = Generate.error(Cause.json_message())
            response.status = Cause.http_status()

        Cause.reset()
        self._logger.debug('end: %s %s', request.method, request.uri)

    @Logger.timeit(refresh_oid=True)
    def on_get(self, request, response, identity):
        """Search resource based on resource ID.

        If the given uuid matches to multiple resources or no resources at
        all, an error is returned. This conflicts against the JSON API v1.0
        specifications. See the Snippy documentation for more information.

        Args:
            request (object): Falcon Request.
            response (object): Falcon Response.
            identity (str): Partial or full message digest or UUID.
        """

        self._logger.debug('run: %s %s', request.method, request.uri)
        local_params = {'identity': identity}
        api = Api(self._category, Api.SEARCH, local_params)
        Config.load(api)
        self._content.run()
        if len(self._content.collection) != 1:
            Cause.push(Cause.HTTP_NOT_FOUND, 'content identity: %s was not unique and matched to: %d resources' %
                       (identity, len(self._content.collection)))
        if Cause.is_ok():
            response.content_type = ApiResource.MEDIA_JSON_API
            response.body = Generate.resource(self._content.collection, request, response, identity, pagination=True)
            response.status = Cause.http_status()
        else:
            response.content_type = ApiResource.MEDIA_JSON_API
            response.body = Generate.error(Cause.json_message())
            response.status = Cause.http_status()

        Cause.reset()
        self._logger.debug('end: %s %s', request.method, request.uri)

    @Logger.timeit(refresh_oid=True)
    def on_delete(self, request, response, identity):
        """Delete resource based on the resource ID.

        Args:
            request (object): Falcon Request.
            response (object): Falcon Response.
            identity (str): Partial or full message digest or UUID.
        """

        self._logger.debug('run: %s %s', request.method, request.uri)
        local_params = {'identity': identity}
        api = Api(self._category, Api.DELETE, local_params)
        Config.load(api)
        self._content.run()
        if Cause.is_ok():
            response.status = Cause.http_status()
        else:
            response.content_type = ApiResource.MEDIA_JSON_API
            response.body = Generate.error(Cause.json_message())
            response.status = Cause.http_status()

        Cause.reset()
        self._logger.debug('end: %s %s', request.method, request.uri)

    @Logger.timeit(refresh_oid=True)
    def on_put(self, request, response, identity):
        """Update resource based on the resource ID.

        Args:
            request (object): Falcon Request.
            response (object): Falcon Response.
            identity (str): Partial or full message digest or UUID.
        """

        self._logger.debug('run: %s %s', request.method, request.uri)
        collection = Validate.json_object(request, identity)
        for resource in collection:
            api = Api(self._category, Api.UPDATE, resource)
            Config.load(api)
            self._content.run()
        if Cause.is_ok():
            response.content_type = ApiResource.MEDIA_JSON_API
            response.body = Generate.resource(self._content.collection, request, response, identity)
            response.status = Cause.http_status()
        else:
            response.content_type = ApiResource.MEDIA_JSON_API
            response.body = Generate.error(Cause.json_message())
            response.status = Cause.http_status()

        Cause.reset()
        self._logger.debug('end: %s %s', request.method, request.uri)

    @Logger.timeit(refresh_oid=True)
    def on_patch(self, request, response, identity):
        """Update partial resource based on resource ID.

        Args:
            request (object): Falcon Request.
            response (object): Falcon Response.
            identity (str): Partial or full message digest or UUID.
        """

        self._logger.debug('run: %s %s', request.method, request.uri)
        self.on_put(request, response, identity)
        Cause.reset()
        self._logger.debug('end: %s %s', request.method, request.uri)

    @staticmethod
    @Logger.timeit(refresh_oid=True)
    def on_options(_, response, identity):  # pylint: disable=unused-argument
        """Respond with allowed methods.

        Args:
            request (object): Falcon Request.
            response (object): Falcon Response.
            identity (str): Partial or full message digest or UUID.
        """

        response.status = Cause.HTTP_200
        response.set_header('Allow', 'DELETE,GET,OPTIONS,PATCH,POST,PUT')


class ApiResourceIdField(object):
    """Access content with resource ID and attribute."""

    def __init__(self, content, category):
        self._logger = Logger.get_logger(__name__)
        self._category = category
        self._content = content

    @Logger.timeit(refresh_oid=True)
    def on_get(self, request, response, identity, field):
        """Get defined content field based on resource ID.

        If the given uuid matches to multiple resources or no resources at
        all, an error is returned. This conflicts against the JSON API v1.0
        specifications. See the Snippy documentation for more information.

        Args:
            request (object): Falcon Request.
            response (object): Falcon Response.
            identity (str): Partial or full message digest or UUID.
            field (str): Resource attribute.
        """

        self._logger.debug('run: %s %s', request.method, request.uri)
        local_params = {'identity': identity, 'fields': field}
        api = Api(self._category, Api.SEARCH, local_params)
        Config.load(api)
        self._content.run()
        if len(self._content.collection) != 1:
            Cause.push(Cause.HTTP_NOT_FOUND, 'content identity: %s was not unique and matched to: %d resources' %
                       (identity, len(self._content.collection)))
        if Cause.is_ok():
            response.content_type = ApiResource.MEDIA_JSON_API
            response.body = Generate.resource(self._content.collection, request, response, identity, field=field, pagination=False)
            response.status = Cause.http_status()
        else:
            response.content_type = ApiResource.MEDIA_JSON_API
            response.body = Generate.error(Cause.json_message())
            response.status = Cause.http_status()

        Cause.reset()
        self._logger.debug('end: %s %s', request.method, request.uri)

    @staticmethod
    @Logger.timeit(refresh_oid=True)
    def on_options(_, response, identity, field):  # pylint: disable=unused-argument
        """Respond with allowed methods.

        Args:
            request (object): Falcon Request.
            response (object): Falcon Response.
            identity (str): Partial or full message digest or UUID.
            field (str): Resource attribute.
        """

        response.status = Cause.HTTP_200
        response.set_header('Allow', 'GET,OPTIONS')


class ApiNotImplemented(object):  # pylint: disable=too-few-public-methods
    """Stanrard response for not allowed HTTP methods."""

    @classmethod
    def send(cls, request, response):
        """Send standard 405 Not Allowed HTTP response.

        Args:
            request (object): Falcon Request.
            response (object): Falcon Response.
        """

        Cause.push(Cause.HTTP_METHOD_NOT_ALLOWED, 'fields api does not support method: {}'.format(request.method))
        response.content_type = ApiResource.MEDIA_JSON_API
        response.body = Generate.error(Cause.json_message())
        response.status = Cause.http_status()
