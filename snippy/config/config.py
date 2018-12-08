#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Snippy - command, solution, reference and code snippet manager.
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

"""config: Global configuration."""

import datetime
import io
import os.path
import sys

import pkg_resources

from snippy.cause import Cause
from snippy.constants import Constants as Const
from snippy.config.source.cli import Cli
from snippy.config.source.editor import Editor
from snippy.content.collection import Collection
from snippy.devel.profiler import Profiler
from snippy.logger import Logger


class Config(object):
    """Global configuration object."""

    _logger = Logger.get_logger(__name__)

    @classmethod
    def init(cls, args):
        """Initialize global configuration."""

        if args is None:
            args = []

        # Set logger and development configuration.
        cls._init_logs(args)

        cls.source = Cli(args)

        # Static storage and template configurations.
        cls.storage_schema = cls._storage_schema()
        cls.storage_path = cls.source.storage_path
        cls.storage_file = cls._storage_file()
        cls.templates = {
            'text': {
                'snippet': cls._content_template('snippet.txt'),
                'solution': cls._content_template('solution.txt'),
                'reference': cls._content_template('reference.txt')
            },
            'mkdn': {
                'snippet': cls._content_template('snippet.md'),
                'solution': cls._content_template('solution.md'),
                'reference': cls._content_template('reference.md')
            }
        }

        # Static server configurations.
        cls.base_path_app = cls.source.base_path_app
        cls.compact_json = cls.source.compact_json
        cls.server = cls.source.server
        cls.server_ip = cls.source.server_ip
        cls.server_port = cls.source.server_port
        cls.ssl_cert = cls._ssl_file(cls.source.ssl_cert)
        cls.ssl_key = cls._ssl_file(cls.source.ssl_key)
        cls.ssl_ca_cert = cls._ssl_file(cls.source.ssl_ca_cert)

        # Dynamic configuration.
        cls.load(cls.source)

    @classmethod
    def load(cls, source):  # pylint: disable=too-many-statements
        """Load dynamic configuration from source."""

        cls.source = source

        # logger: Only quiet flag is updated. If all logging configuration
        # would be updated, the server would print logs only from the first
        # operation. The reason to update quiet flag is to be able to prevent
        # test cases to print unnecessary help dialog when test creates the
        # Snippy() object. This allows the first creation to be silent but
        # allows further configuration from tests with snippy.run().
        cls.quiet = bool(cls.source.quiet)
        cls._update_logger()
        cls._logger.debug('config source: %s', cls.source)

        # operation
        cls.operation = cls.source.operation
        cls.operation_digest = cls.source.digest
        cls.operation_uuid = cls.source.uuid
        cls.merge = cls.source.merge

        # content
        cls.content_category = cls.source.category
        cls.content_data = cls.source.data
        cls.content_brief = cls.source.brief
        cls.content_description = cls.source.description
        cls.content_groups = cls.source.groups
        cls.content_tags = cls.source.tags
        cls.content_links = cls.source.links
        cls.content_name = cls.source.name
        cls.content_filename = cls.source.filename
        cls.content_versions = cls.source.versions
        cls.content_source = cls.source.source

        # search
        cls.search_cat_kws = cls.source.scat
        cls.search_all_kws = cls.source.sall
        cls.search_tag_kws = cls.source.stag
        cls.search_grp_kws = cls.source.sgrp
        cls.search_filter = cls.source.search_filter
        cls.search_limit = cls.source.search_limit
        cls.search_offset = cls.source.search_offset
        cls.remove_fields = cls.source.remove_fields
        cls.sort_fields = cls.source.sort_fields

        # migrate
        cls.defaults = cls.source.defaults
        cls.template = cls.source.template

        # options
        cls.editor = cls.source.editor
        cls.use_ansi = not cls.source.no_ansi
        cls.failure = cls.source.failure

        # Server must be updated again because only the first init starts the server.
        cls.server = cls.source.server

        # Parsed from defined configuration.
        cls.is_operation_create = bool(cls.operation == 'create')
        cls.is_operation_search = bool(cls.operation == 'search')
        cls.is_operation_update = bool(cls.operation == 'update')
        cls.is_operation_delete = bool(cls.operation == 'delete')
        cls.is_operation_export = bool(cls.operation == 'export')
        cls.is_operation_import = bool(cls.operation == 'import')
        cls.is_category_snippet = bool(cls.content_category == Const.SNIPPET)
        cls.is_category_solution = bool(cls.content_category == Const.SOLUTION)
        cls.is_category_reference = bool(cls.content_category == Const.REFERENCE)
        cls.is_category_all = bool(cls.content_category == Const.ALL_CATEGORIES)
        cls.operation_filename = cls._operation_filename((cls.content_category,))
        cls.operation_file_format = cls._operation_file_format(cls.operation_filename)
        cls.is_operation_file_json = bool(cls.operation_file_format == Const.CONTENT_FORMAT_JSON)
        cls.is_operation_file_mkdn = bool(cls.operation_file_format == Const.CONTENT_FORMAT_MKDN)
        cls.is_operation_file_text = bool(cls.operation_file_format == Const.CONTENT_FORMAT_TEXT)
        cls.is_operation_file_yaml = bool(cls.operation_file_format == Const.CONTENT_FORMAT_YAML)

        cls.debug()

    @classmethod
    def reset(cls):
        """Reset configuration."""

        Profiler.disable()

    @classmethod
    def get_collection(cls, resource=None):
        """Get resource collection from configuration source.

        Get collection of resources from various configuration sources. A
        configuration source can be a set of CLI parameters or a REST API
        request.

        If resource updates are provided on top of configured content, the
        updates are added on top of configured content. For example when
        existing content is updated, the stored content must be shown on
        text editor.

        Args:
            resource (Resource()): Content updates on top of configured content.

        Returns:
            Collection(): Configured content in Collection object.
        """

        collection = Collection()
        timestamp = Config.utcnow()
        if cls.editor:
            if not resource:
                resource = Collection().get_resource(cls.content_category, timestamp)
            Editor.read(timestamp, Config.templates, resource, collection)
        else:
            cls._read_collection(timestamp, collection)

        return collection

    @classmethod
    def get_resource(cls, updates):
        """Get resource from configuration source.

        The configuration source is updated with given in the Resource()
        object.

        If the resource updates from one of the configuration sources fail,
        same content is returned.

        Args:
            resource (Resource()): Content updates on top of configured content.

        Returns:
            Resource(): Updated resource from one of the configuration sources.
        """

        collection = cls.get_collection(updates)
        if len(collection) == 1:
            resource = next(collection.resources())
        else:
            cls._logger.debug('updating resource from configuration source failed: %d', len(collection))
            resource = None

        return resource

    @classmethod
    def _init_logs(cls, args):
        """Init logger and development configuration."""

        # Parse log configuration manually in order to init the logger as
        # early as possible. The same parameters are read by the argparse.
        # which will make more through option checking. The value is always
        # following the parameter name.
        log_msg_max = Logger.DEFAULT_LOG_MSG_MAX
        try:
            value = int(args[args.index('--log-msg-max') + 1])
            if isinstance(value, int) and value > 0:
                log_msg_max = int(args[args.index('--log-msg-max') + 1])
        except (IndexError, ValueError):
            pass

        cls.debug_logs = bool('--debug' in args)
        cls.log_json = bool('--log-json' in args)
        cls.log_msg_max = log_msg_max
        cls.profiler = bool('--profile' in args)
        cls.quiet = bool('-q' in args)
        cls.very_verbose = bool('-vv' in args)

        # Profile code.
        Profiler.enable(cls.profiler)

        cls._update_logger()
        cls._logger.debug('config initial command line arguments: %s', args)

    @classmethod
    def _update_logger(cls):
        """Update logger configuration."""

        Logger.configure({
            'debug': cls.debug_logs,
            'log_json': cls.log_json,
            'log_msg_max': cls.log_msg_max,
            'quiet': cls.quiet,
            'very_verbose': cls.very_verbose
        })

        cls._logger.debug(
            'config source debug: %s, very verbose: %s, quiet: %s, json: %s msg max: %d',
            cls.debug_logs,
            cls.very_verbose,
            cls.quiet,
            cls.log_json,
            cls.log_msg_max
        )

    @classmethod
    def _read_collection(cls, timestamp, collection):
        """Read configurared content."""

        resource = collection.get_resource(cls.content_category, timestamp)
        resource.data = cls.content_data
        resource.brief = cls.content_brief
        resource.description = cls.content_description
        resource.groups = cls.content_groups
        resource.tags = cls.content_tags
        resource.links = cls.content_links
        resource.name = cls.content_name
        resource.filename = cls.content_filename
        resource.versions = cls.content_versions
        resource.source = cls.content_source
        resource.digest = resource.compute_digest()
        collection.migrate(resource)

    @classmethod
    def _storage_schema(cls):
        """Test that database schema file exist."""

        # The database schema is installed with the tool and it must always exist.
        schema_file = os.path.join(pkg_resources.resource_filename('snippy', 'data/storage'), 'database.sql')
        if not os.path.isfile(schema_file):
            Logger.print_status('NOK: cannot run because database schema is not accessible: {}'.format(schema_file))
            sys.exit(1)

        return schema_file

    @classmethod
    def _content_template(cls, template):
        """Get defined content template installed with the tool."""

        filename = os.path.join(pkg_resources.resource_filename('snippy', 'data/templates'), template)
        if not os.path.isfile(filename):
            Logger.print_status('NOK: cannot run because content template path is not accessible: {}'.format(filename))
            sys.exit(1)

        template = Const.EMPTY
        with io.open(filename, encoding='utf-8') as infile:
            template = infile.read()

        return template

    @classmethod
    def _storage_file(cls):
        """Construct store file with absolute path."""

        if Config.storage_path:
            storage_path = Config.storage_path
        else:
            storage_path = pkg_resources.resource_filename('snippy', 'data/storage')

        if os.path.exists(storage_path) and os.access(storage_path, os.W_OK):
            storage_file = os.path.join(storage_path, 'snippy.db')
        else:
            # This is a special case which prevents additional error log after
            # tool is already about to exit with help text from the CLI parser.
            if not cls.source.failure:
                Logger.print_status('NOK: cannot run because content storage path is not accessible: {}'.format(storage_path))
            sys.exit(1)

        return storage_file

    @classmethod
    def _ssl_file(cls, filename):
        """Test that given SSL/TLS certificate or key file exist."""

        if filename is not None and not os.path.isfile(filename):
            Logger.print_status('NOK: cannot run secured server because ssl/tls certificate file cannot be read: {}'.format(filename))
            sys.exit(1)

        return filename

    @classmethod
    def get_operation_file(cls, collection=None):
        """Return file for operation.

        Use the resource filename field only in case of export operation when
        there is a single resource in collection and when user did not define
        target file from command line.

        If collection is provided with more than one resource, the operation
        file is still updated. The collection might be a search result from
        different category than originally defined.

        Args:
            collection (Collection): Resources in Collection container.

        Returns:
            string: Operation filename.
        """

        filename = cls.operation_filename
        if cls.is_operation_export and collection and not cls.content_filename:
            if len(collection) == 1 and next(collection.resources()).filename:
                filename = next(collection.resources()).filename
            else:
                categories = collection.category_list()
                filename = cls._operation_filename(categories)
            cls.operation_filename = filename
            cls.operation_file_format = cls._operation_file_format(filename)
            cls.is_operation_file_json = bool(cls.operation_file_format == Const.CONTENT_FORMAT_JSON)
            cls.is_operation_file_mkdn = bool(cls.operation_file_format == Const.CONTENT_FORMAT_MKDN)
            cls.is_operation_file_text = bool(cls.operation_file_format == Const.CONTENT_FORMAT_TEXT)
            cls.is_operation_file_yaml = bool(cls.operation_file_format == Const.CONTENT_FORMAT_YAML)

        return filename

    @classmethod
    def is_supported_file_format(cls):
        """Test if file format is supported."""

        return bool(cls.is_operation_file_json or
                    cls.is_operation_file_mkdn or
                    cls.is_operation_file_text or
                    cls.is_operation_file_yaml)

    @classmethod
    def default_content_file(cls, category):
        """Return default content file.

        Args:
            category (str): User defined content category.

        Returns:
            string: Filename with absolute path.
        """

        filename = category + 's.yaml'
        filename = os.path.join(pkg_resources.resource_filename('snippy', 'data/defaults'), filename)

        return filename

    @classmethod
    def _operation_filename(cls, categories):
        """Return operation default filename

        Filename is set based on priority order of
          1) command line input
          2) content template or content defaults operations
          3) content category specific defaults

        Args:
            categories (tuple): List of categories related to operation.

        Returns:
            string: Operation filename.
        """

        filename = None
        if cls.source.filename:
            filename = cls.source.filename

        if cls.defaults:
            filename = cls.default_content_file(cls.content_category)

        if cls.template:
            filename = os.path.join('./', cls.content_category + '-template.txt')

        if not filename:
            if len(categories) == 1:
                defaults = categories[0] + 's.yaml'
            else:
                defaults = 'content.yaml'
            filename = os.path.join('./', defaults)

        return filename

    @classmethod
    def _operation_file_format(cls, filename):
        """Extract operation file format.

        The file format must be exactly as defined for supported file formats.

        Args:
            filename (string): Filename with file extension defining the format.

        Returns:
            string: Operation file format.
        """

        file_format = Const.CONTENT_FORMAT_NONE
        name, extension = os.path.splitext(filename)
        if name and extension == '.json':
            file_format = Const.CONTENT_FORMAT_JSON
        elif name and (extension == '.md' or extension == '.mkdn'):  # pylint: disable=consider-using-in
            file_format = Const.CONTENT_FORMAT_MKDN
        elif name and (extension == '.text' or extension == '.txt'):  # pylint: disable=consider-using-in
            file_format = Const.CONTENT_FORMAT_TEXT
        elif name and (extension == '.yaml' or extension == '.yml'):  # pylint: disable=consider-using-in
            file_format = Const.CONTENT_FORMAT_YAML
        else:
            Cause.push(Cause.HTTP_BAD_REQUEST, 'cannot identify file format for file: {}'.format(filename))

        return file_format

    @classmethod
    def validate_search_context(cls, collection, operation):  # pylint: disable=too-many-branches
        """Validate content search context."""

        # Search keys are treated in priority order of 1) digest, 2) uuid,
        # 3) content data and 4) search keywords. Search keywords are already
        # validated and invalid keywords are interpreted as 'list all' which
        # is always correct at this point.
        cls._logger.debug('validating search context with %d results', len(collection))
        if cls._is_content_digest():
            if cls.operation_digest:
                if not collection:
                    Cause.push(Cause.HTTP_NOT_FOUND,
                               'cannot find content with message digest: %s' % cls.operation_digest)
                elif len(collection) > 1:
                    Cause.push(Cause.HTTP_CONFLICT,
                               'content digest: %.16s :matched more than once: %d :preventing: %s :operation' %
                               (cls.operation_digest, len(collection), operation))
            else:
                Cause.push(Cause.HTTP_BAD_REQUEST, 'cannot use empty message digest for: %s :operation' % operation)
        elif cls._is_content_uuid():
            if cls.operation_uuid:
                if not collection:
                    Cause.push(Cause.HTTP_NOT_FOUND,
                               'cannot find content with content uuid: %s' % cls.operation_uuid)
                elif len(collection) > 1:
                    Cause.push(Cause.HTTP_CONFLICT,
                               'content uuid: %.16s :matched more than once: %d :preventing: %s :operation' %
                               (cls.operation_uuid, len(collection), operation))
            else:
                Cause.push(Cause.HTTP_BAD_REQUEST, 'cannot use empty content uuid for: %s :operation' % operation)
        elif cls.content_data:
            if any(cls.content_data):
                data = Const.EMPTY.join(cls.content_data)
                data = data[:30] + (data[30:] and '...')
                if not collection:
                    Cause.push(Cause.HTTP_NOT_FOUND, 'cannot find content with content data: %s' % data)
                elif len(collection) > 1:
                    Cause.push(Cause.HTTP_CONFLICT,
                               'content data: %s :matched more than once: %d :preventing: %s :operation' %
                               (data, len(collection), operation))
            else:
                Cause.push(Cause.HTTP_BAD_REQUEST, 'cannot use empty content data for: %s :operation' % operation)
        elif cls._is_search_keywords():
            if not collection:
                Cause.push(Cause.HTTP_NOT_FOUND, 'cannot find content with given search criteria')
            elif len(collection) > 1:
                Cause.push(Cause.HTTP_CONFLICT,
                           'search keywords matched more than once: %d :preventing: %s :operation' % (len(collection), operation))
        else:
            Cause.push(Cause.HTTP_BAD_REQUEST, 'no message digest, content data or search keywords were provided')

    @classmethod
    def _is_search_keywords(cls):
        """Test if search is made with any of the search option.

        The seach categories (search_cat_kws) is not considered optional search
        keywords because this category is set always implicitly if not provided
        by the user.
        """

        return bool(cls.search_all_kws or cls.search_tag_kws or cls.search_grp_kws)

    @classmethod
    def _is_content_digest(cls):
        """Test if content digest was defined from command line."""

        return bool(cls.operation_digest is not None)

    @classmethod
    def _is_content_uuid(cls):
        """Test if content uuid was defined from command line."""

        return bool(cls.operation_uuid is not None)

    @classmethod
    def is_search_criteria(cls):
        """Test if any of the search criterias were used."""

        criteria = False
        if cls._is_search_keywords() or cls._is_content_digest() or cls._is_content_uuid() or cls.content_data:
            criteria = True

        return criteria

    @staticmethod
    def utcnow():
        """Get UTC time stamp in ISO8601 format."""

        utc = datetime.datetime.utcnow()

        return utc.strftime('%Y-%m-%dT%H:%M:%S.%f+0000')

    @classmethod
    def debug(cls):
        """Debug Config."""

        cls._logger.debug('configured storage file: %s', cls.storage_file)
        cls._logger.debug('configured storage schema: %s', cls.storage_schema)
        cls._logger.debug('configured content operation: %s', cls.operation)
        cls._logger.debug('configured content category: %s', cls.content_category)
        cls._logger.debug('configured content data: %s', cls.content_data)
        cls._logger.debug('configured content brief: %s', cls.content_brief)
        cls._logger.debug('configured content description: %s', cls.content_description)
        cls._logger.debug('configured content groups: %s', cls.content_groups)
        cls._logger.debug('configured content tags: %s', cls.content_tags)
        cls._logger.debug('configured content links: %s', cls.content_links)
        cls._logger.debug('configured content name: %s', cls.content_name)
        cls._logger.debug('configured content filename: %s', cls.content_filename)
        cls._logger.debug('configured content versions: %s', cls.content_versions)
        cls._logger.debug('configured content source: %s', cls.content_source)
        cls._logger.debug('configured operation digest: %s', cls.operation_digest)
        cls._logger.debug('configured operation uuid: %s', cls.operation_uuid)
        cls._logger.debug('configured operation filename: "%s"', cls.operation_filename)
        cls._logger.debug('configured operation file format: "%s"', cls.operation_file_format)
        cls._logger.debug('configured search all keywords: %s', cls.search_all_kws)
        cls._logger.debug('configured search cat keywords: %s', cls.search_cat_kws)
        cls._logger.debug('configured search tag keywords: %s', cls.search_tag_kws)
        cls._logger.debug('configured search group keywords: %s', cls.search_grp_kws)
        cls._logger.debug('configured search result regexp filter: %s', cls.search_filter)
        cls._logger.debug('configured search result limit: %s :and offset: %s', cls.search_limit, cls.search_offset)
        cls._logger.debug('configured search result filter fields: %s', cls.remove_fields)
        cls._logger.debug('configured search result sorted fields: %s', cls.sort_fields)
        cls._logger.debug('configured option editor: %s', cls.editor)
        cls._logger.debug('configured option use ansi characters in text output: %s', cls.use_ansi)
        cls._logger.debug('configured option defaults: %s', cls.defaults)
        cls._logger.debug('configured option template: %s', cls.template)
        cls._logger.debug('configured option server: %s', cls.server)
        cls._logger.debug('configured option server app base path: %s', cls.base_path_app)
        cls._logger.debug('configured option server ip: %s :and port: %s', cls.server_ip, cls.server_port)
        cls._logger.debug('configured option server compact json: %s', cls.compact_json)
        cls._logger.debug('configured option server ssl certificate file: %s', cls.ssl_cert)
        cls._logger.debug('configured option server ssl key file: %s', cls.ssl_key)
        cls._logger.debug('configured option server ssl ca certificate file: %s', cls.ssl_ca_cert)
