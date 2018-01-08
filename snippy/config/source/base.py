#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Snippy - command, solution and code snippet management.
#  Copyright 2017-2018 Heikki J. Laaksonen  <laaksonen.heikki.j@gmail.com>
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

"""base.py: Base class for configuration sources."""

import re
from snippy.metadata import __version__
from snippy.cause.cause import Cause
from snippy.config.constants import Constants as Const
from snippy.config.source.parser import Parser
from snippy.logger.logger import Logger


class ConfigSourceBase(object):  # pylint: disable=too-many-instance-attributes
    """Base class for configuration sources."""

    # Operations
    CREATE = 'create'
    SEARCH = 'search'
    UPDATE = 'update'
    DELETE = 'delete'
    EXPORT = 'export'
    IMPORT = 'import'
    OPERATIONS = ('create', 'search', 'update', 'delete', 'export', 'import')

    # Fields
    DATA = 'data'
    BRIEF = 'brief'
    GROUP = 'group'
    TAGS = 'tags'
    LINKS = 'links'
    CATEGORY = 'category'
    FILENAME = 'filename'
    RUNALIAS = 'runalias'
    VERSIONS = 'versions'
    UTC = 'utc'
    DIGEST = 'digest'
    KEY = 'key'
    ALL_FIELDS = ('data', 'brief', 'group', 'tags', 'links', 'category', 'filename',
                  'runalias', 'versions', 'utc', 'digest', 'key')

    # Defaults
    LIMIT_DEFAULT = 20

    def __init__(self):
        self._logger = Logger(__name__).get()
        self._repr = Const.EMPTY

        self.brief = Const.EMPTY
        self.category = Const.UNKNOWN_CONTENT
        self.data = None
        self.debug = False
        self.defaults = False
        self.digest = None
        self.editor = False
        self.filename = Const.EMPTY
        self.group = Const.DEFAULT_GROUP
        self.limit = self.LIMIT_DEFAULT
        self.links = ()
        self.no_ansi = False
        self.operation = Const.EMPTY
        self.profile = False
        self.quiet = False
        self._regexp = Const.EMPTY
        self.rfields = (self.ALL_FIELDS)
        self.sall = None
        self.server = False
        self.sfields = {}
        self.sgrp = None
        self.stag = None
        self.tags = ()
        self.template = False
        self.version = __version__
        self.very_verbose = False
        self._set_repr()

    def __repr__(self):

        return self._repr

    def _set_repr(self):
        """Set object representation."""

        namespace = []
        class_name = type(self).__name__
        attributes = list(self.__dict__.keys())
        attributes.remove('_logger')
        attributes.remove('_repr')
        attributes = [attribute.lstrip('_') for attribute in attributes]
        for attribute in sorted(attributes):
            namespace.append('%s=%r' % (attribute, getattr(self, attribute)))
        self._repr = '%s(%s)' % (class_name, ', '.join(namespace))

    def set_conf(self, parameters):
        """Set API configuration parameters."""

        # Parameters that where the tool must be aware if the parameter
        # was given at all must bed defined to None if no parameter set.
        self.brief = parameters.get('brief', Const.EMPTY)
        self.category = parameters.get('category')
        self.data = parameters.get('data', None)
        self.debug = parameters.get('debug', False)
        self.defaults = parameters.get('defaults', False)
        self.digest = parameters.get('digest', None)
        self.editor = parameters.get('editor', False)
        self.filename = parameters.get('filename', Const.EMPTY)
        self.group = parameters.get('group', Const.DEFAULT_GROUP)
        self.limit = parameters.get('limit', self.LIMIT_DEFAULT)
        self.links = parameters.get('links', ())
        self.no_ansi = parameters.get('no_ansi', False)
        self.operation = parameters.get('operation')
        self.profile = parameters.get('profile', False)
        self.quiet = parameters.get('quiet', False)
        self.regexp = parameters.get('regexp', Const.EMPTY)
        self.rfields = parameters.get('fields', self.ALL_FIELDS)
        self.sall = parameters.get('sall', None)
        self.server = parameters.get('server', False)
        self.sfields = parameters.get('sort', ('brief'))
        self.sgrp = parameters.get('sgrp', None)
        self.stag = parameters.get('stag', None)
        self.tags = parameters.get('tags', ())
        self.template = parameters.get('template', False)
        self.very_verbose = parameters.get('very_verbose', False)

        self._set_repr()

    @property
    def data(self):
        """Get content data."""

        return self._data

    @data.setter
    def data(self, value):
        """Content data is stored as a tuple with one line per element.
        There is a quarantee that each line contains only one newline
        at the end of string in the tuple.

        Any value including empty string is considered valid data."""

        if value is not None:
            string_ = Parser.to_string(value)
            data = tuple(string_.split(Const.DELIMITER_DATA))
        else:
            data = ()

        self._data = data  # pylint: disable=attribute-defined-outside-init

    @property
    def tags(self):
        """Get content tags."""

        return self._tags

    @tags.setter
    def tags(self, value):
        """Content tags are stored as a tuple with one tag per element."""

        self._tags = Parser.keywords(value)  # pylint: disable=attribute-defined-outside-init

    @property
    def links(self):
        """Get content links."""

        return self._links

    @links.setter
    def links(self, value):
        """Content links are stored as a tuple with one link per element."""

        self._links = Parser.links(value)  # pylint: disable=attribute-defined-outside-init

    @property
    def sall(self):
        """Get 'search all' keywords."""

        return self._sall

    @sall.setter
    def sall(self, value):
        """Search all keywords stored as a tuple with one keywords per
        element."""

        self._sall = Parser.search_keywords(value)  # pylint: disable=attribute-defined-outside-init

    @property
    def stag(self):
        """Get 'search tag' keywords."""

        return self._stag

    @stag.setter
    def stag(self, value):
        """Search tag keywords stored as a tuple with one keywords per
        element."""

        self._stag = Parser.search_keywords(value)  # pylint: disable=attribute-defined-outside-init

    @property
    def sgrp(self):
        """Get 'search group' keywords."""

        return self._sgrp

    @sgrp.setter
    def sgrp(self, value):
        """Search group keywords stored as a tuple with one keywords per
        element."""

        self._sgrp = Parser.search_keywords(value)  # pylint: disable=attribute-defined-outside-init

    @property
    def regexp(self):
        """Get search regexp filter."""

        return self._regexp

    @regexp.setter
    def regexp(self, value):
        """Search regexp filter must be Python regexp."""

        try:
            re.compile(value)
            self._regexp = value
        except re.error:
            self._regexp = Const.EMPTY
            Cause.push(Cause.HTTP_BAD_REQUEST,
                       'listing matching content without filter because it was not syntactically correct regular expression')

    @property
    def limit(self):
        """Get search result limit."""

        return self._limit

    @limit.setter
    def limit(self, value):
        """Search result limit."""

        self._limit = self.LIMIT_DEFAULT  # pylint: disable=attribute-defined-outside-init
        try:
            self._limit = int(value)  # pylint: disable=attribute-defined-outside-init
        except ValueError:
            self._logger.info('search result limit is not a number and thus default use: %d', self._limit)

    @property
    def sfields(self):
        """Get sorted fields in internal presentation."""

        return self._sfields

    @sfields.setter
    def sfields(self, value):
        """Sorted fields are stored in internal presentation from given
        value. The internal format contains field index that matches to
        database column index. The order where the sorted column names
        was received must be persisted. Otherwise the sort does not work
        correctly."""

        sorted_dict = {}
        sorted_dict['order'] = []
        sorted_dict['value'] = {}
        field_names = Parser.keywords(value, sort_=False)
        for field in field_names:
            try:
                if field[0].startswith('-'):
                    index_ = self.ALL_FIELDS.index(field[1:])
                    sorted_dict['order'].append(index_)
                    sorted_dict['value'][index_] = True
                else:
                    index_ = self.ALL_FIELDS.index(field)
                    sorted_dict['order'].append(index_)
                    sorted_dict['value'][index_] = False
            except ValueError:
                Cause.push(Cause.HTTP_BAD_REQUEST, 'sort option validation failed for non existent field={}'.format(field))
        self._logger.debug('config source internal format for sorted fields: %s', sorted_dict)
        self._sfields = sorted_dict  # pylint: disable=attribute-defined-outside-init

    @property
    def rfields(self):
        """Get removed fields."""

        return self._rfields

    @rfields.setter
    def rfields(self, value):
        """Removed fields are presented as tuple and they are converted
        from requested fields."""

        requested_fields = Parser.keywords(value)
        self._rfields = tuple(set(self.ALL_FIELDS) - set(requested_fields))  # pylint: disable=attribute-defined-outside-init
        self._logger.debug('content fields that are removed from response: %s', self._rfields)
