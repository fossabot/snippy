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

"""content: Content helpers for testing."""

import copy
import datetime
import re
import traceback

import json
import mock
import pprintpp

from snippy.config.config import Config
from snippy.constants import Constants as Const
from snippy.content.collection import Collection
from snippy.meta import __docs__
from snippy.meta import __homepage__
from snippy.meta import __openapi__
from snippy.meta import __version__
from tests.testlib.database import Database
from tests.testlib.helper import Helper
from tests.testlib.reference import Reference
from tests.testlib.snippet import Snippet
from tests.testlib.solution import Solution

class Content(object):  # pylint: disable=too-many-public-methods
    """Helper methods for content testing."""

    # Contents
    EXPORT_TIME = Helper.EXPORT_TIME
    IMPORT_TIME = Helper.IMPORT_TIME

    # Snippets
    REMOVE_TIME = Snippet.REMOVE_CREATED  # Default snippet utc times must be same.
    FORCED_TIME = Snippet.FORCED_CREATED  # Default snippet utc must be same.
    EXITED_TIME = Snippet.EXITED_CREATED
    NETCAT_TIME = Snippet.NETCAT_CREATED
    UMOUNT_TIME = Snippet.UMOUNT_CREATED
    INTERP_TIME = Snippet.INTERP_CREATED

    # Solutions
    BEATS_TIME = Solution.BEATS_CREATED  # Default solution utc must be same.
    NGINX_TIME = Solution.NGINX_CREATED  # Default solution utc must be same.
    KAFKA_TIME = Solution.KAFKA_CREATED
    KAFKA_MKDN_TIME = Solution.KAFKA_MKDN_CREATED

    # References
    GITLOG_TIME = Reference.GITLOG_CREATED  # Default reference utc must be same.
    REGEXP_TIME = Reference.REGEXP_CREATED  # Default reference utc must be same.
    PYTEST_TIME = Reference.PYTEST_CREATED

    JSON = Const.CONTENT_FORMAT_JSON
    MKDN = Const.CONTENT_FORMAT_MKDN
    TEXT = Const.CONTENT_FORMAT_TEXT
    YAML = Const.CONTENT_FORMAT_YAML

    @staticmethod
    def store(content):
        """Store content into database.

        Args:
            content (dict): Content in a dictionary.
        """

        Database.store(content)

    @staticmethod
    def delete():
        """Delete all existing content and the database."""

        Database.delete_all_contents()
        Database.delete_storage()

    @staticmethod
    def output():
        """Print all content stored in database."""

        Database.print_contents()

    @staticmethod
    def db_cli_params():
        """Return required CLI parameters for database."""

        return Database.get_cli_params()

    @staticmethod
    def deepcopy(content):
        """Return a deepcopy from given content.

        This allows user to modify content without changing the original
        content.

        Args:
            content (dict): Single content that is copied.

        Returns:
            dict: Deepcopy of the content.
        """

        return copy.deepcopy(content)

    @classmethod
    def dump_text(cls, content):
        """Return text from given content.

        This can be used for example to convert test case content to text
        string to be used as a response from mocked editor.

        In order to be able to insert multiple Markdown contents to database,
        the UUID must be unique. Because of this, the conversion must not use
        the methods that masks the content fields to common values. This is
        applicaple only to Markdown content which has the full metadata.

        The text string is returned from resource. The collection adds one
        extra newline in the string.

        Args:
            content (dict): Single content that is converted to text.

        Returns:
            str: Text string created from given content.
        """

        collection = Collection()
        collection.load_dict('2018-10-20T06:16:27.000001+00:00', {'data': [content]})

        # Collection adds one extra newline which must be removed. The rstrip()
        # cannot be used because it would remove all the trailing newlines.
        return collection.dump_text(Config.templates)[:-1]

    @classmethod
    def dump_mkdn(cls, content):
        """Return Markdown from given content.

        See dump_text.

        Args:
            content (dict): Single content that is converted to Markdown.

        Returns:
            str: Text string in Markdown format created from given content.
        """

        collection = Collection()
        collection.load_dict('2018-10-20T06:16:27.000001+00:00', {'data': [content]})

        return collection.dump_mkdn(Config.templates)

    @staticmethod
    def dump_dict(content):
        """Return content in dictionary format.

        Args:
            content (str): Content in text string format.

        Returns:
            dict: Content in dictionary format.
        """

        collection = Collection()
        collection.load_text(Content.IMPORT_TIME, content)

        return collection.dump_dict()[0]

    @staticmethod
    def get_collection(content):
        """Return collection from content.

        Args:
            content (dict): Content in a dictionary format.

        Returns:
            CollectionI(): Content stored in collection.
        """

        collection = Collection()
        collection.load(Const.CONTENT_FORMAT_DICT, Content.IMPORT_TIME, {'data': [content]})

        return collection

    @classmethod
    def assert_storage(cls, content):
        """Compare content stored in database.

        The assert comparisons use equality implemented for collection data
        class. This quarantees that the count of resources in collection is
        same between expected content and collection created from database.

        The comparison tests all but the key attribute between references
        stored in collection. The key attribute is an index in database and
        it cannot be compared.

        The content UUID must be unique for the database. UUID's are allocated
        in order where content is stored which can be random between different
        tests. Because of this, the content UUID is always masked away.

        Text formatted content does not have all fields. For example created
        and updated fields are missing and cannot be compared. Because of this,
        some fields are masked away when comparing text content.

        If the result and expected content are compared only as collections,
        there are cases that are not noticed. A content fields in collection
        are for example sorted and trimmed in some cases. The given content
        dictionary format from test cases must be set correctly in order to
        keep the content definitions in test correct. Because of this, the
        content must be compared also in dictionary format.

        The original content must not be changed because it is in most cases
        default content shared between all tests.

        Args:
            content (dict): Excepted content compared against database.
        """

        if not content:
            assert not Database.get_collection()

            return

        result_collection = cls._get_db_collection()
        result_dictionary = cls._get_db_dictionary(result_collection)
        expect_collection = cls._get_expect_collection(Const.CONTENT_FORMAT_DICT, content)
        expect_dictionary = cls._get_expect_dictionary(content)
        try:
            assert result_collection == expect_collection
            assert result_dictionary == expect_dictionary
        except AssertionError:
            Content._print_assert(result_collection, expect_collection)
            Content._print_assert(result_dictionary, expect_dictionary)
            raise AssertionError

    @classmethod
    def assert_storage_size(cls, size):
        """Compare content count stored in database."""

        try:
            assert size == len(Database.get_collection())
        except AssertionError:
            print('database contains {} contents when expected size was {}'.format(len(Database.get_collection()), size))
            raise AssertionError

    @classmethod
    def assert_restapi(cls, result, expect):
        """Compare content received from REST API.

        See the description for assert_storage method.

        Args:
            result (dict): Result JSON from REST API.
            expect (dict): Excepted JSON in REST API response.
        """

        result_dict = Content._get_result_restapi(result)
        expect_dict = Content._get_expect_restapi(expect)
        try:
            assert result_dict == expect_dict
        except AssertionError:
            print('result:')
            pprintpp.pprint(result_dict)
            print('expect:')
            pprintpp.pprint(expect_dict)
            raise AssertionError

    @classmethod
    def assert_json(cls, json_mock, json_file, filename, content):
        """Compare JSON against expected content.

        See the description for assert_storage method.

        Args:
            json_mock (obj): Mocked JSON dump method.
            json_file (obj): Mocked file where the JSON content was saved.
            filename (str): Expected filename.
            content (dict): Excepted content compared against generated JSON.
        """

        result_collection = cls._get_result_collection(Const.CONTENT_FORMAT_JSON, json_mock)
        result_dictionary = cls._get_result_dictionary(Const.CONTENT_FORMAT_JSON, json_mock)
        expect_collection = cls._get_expect_collection(Const.CONTENT_FORMAT_JSON, content)
        expect_dictionary = cls._get_expect_dictionary(content)
        try:
            assert result_collection == expect_collection
            assert result_dictionary == expect_dictionary
            json_file.assert_called_once_with(filename, 'w')
        except AssertionError:
            Content._print_assert(result_collection, expect_collection)
            Content._print_assert(result_dictionary, expect_dictionary)
            raise AssertionError

    @classmethod
    def assert_mkdn(cls, mkdn_mock, filename, content):
        """Compare Markdown against expected content.

        See the description for assert_storage method.

        Args:
            mkdn_mock (obj): Mocked file where the Markdown content was saved.
            filename (str): Expected filename.
            content (dict): Excepted content compared against Markdown file.
        """

        result_collection = cls._get_result_collection(Const.CONTENT_FORMAT_MKDN, mkdn_mock)
        result_markdown = cls._read_text(Const.CONTENT_FORMAT_MKDN, mkdn_mock)
        expect_collection = cls._get_expect_collection(Const.CONTENT_FORMAT_MKDN, content)
        expect_markdown = result_collection.dump_mkdn(Config.templates)
        try:
            assert result_collection == expect_collection
            assert result_markdown == expect_markdown
            mkdn_mock.assert_called_once_with(filename, 'w')
        except AssertionError:
            Content._print_assert(result_collection, expect_collection)
            Content._print_assert(result_markdown, expect_markdown)
            raise AssertionError

    @classmethod
    def assert_text(cls, text, filename, content):
        """Compare proprietary text format against expected content.

        See description for assert_storage method.

        Args:
            text (obj): Mocked file where the Markdown content was saved.
            filename (str): Expected filename.
            content (dict): Excepted content compared against Markdown file.
        """

        if not filename:
            text.assert_not_called()
            text.return_value.__enter__.return_value.write.assert_not_called()

            return

        result_collection = cls._get_result_collection(Const.CONTENT_FORMAT_TEXT, text)
        result_text = cls._read_text(Const.CONTENT_FORMAT_TEXT, text)
        expect_collection = cls._get_expect_collection(Const.CONTENT_FORMAT_TEXT, content)
        expect_text = expect_collection.dump_text(Config.templates)
        try:
            assert result_collection == expect_collection
            assert result_text == expect_text
            text.assert_called_once_with(filename, 'w')
        except AssertionError:
            Content._print_assert(result_collection, expect_collection)
            Content._print_assert(result_text, expect_text)
            raise AssertionError

    @classmethod
    def assert_yaml(cls, yaml, yaml_file, filenames, content):
        """Compare YAML against expected content.

        See description for assert_storage method.

        Args:
            yaml (obj): Mocked YAML dump method.
            yaml_file (obj): Mocked file where the YAML content was saved.
            filenames (str|list): Expected filename or list of filenames.
            content (dict): Excepted content compared against generated YAML.
        """

        result_collection = cls._get_result_collection(Const.CONTENT_FORMAT_YAML, yaml)
        result_dictionary = cls._get_result_dictionary(Const.CONTENT_FORMAT_YAML, yaml)
        expect_collection = cls._get_expect_collection(Const.CONTENT_FORMAT_YAML, content)
        expect_dictionary = cls._get_expect_dictionary(content)
        try:
            assert result_collection == expect_collection
            assert result_dictionary == expect_dictionary
            if isinstance(filenames, (list, tuple)):
                for filename in filenames:
                    yaml_file.assert_any_call(filename, 'w')
            else:
                yaml_file.assert_called_once_with(filenames, 'w')
        except AssertionError:
            Content._print_assert(result_collection, expect_collection)
            Content._print_assert(result_dictionary, expect_dictionary)
            raise AssertionError

    @staticmethod
    def get_api_meta():
        """Return default REST API metadata."""

        meta = {
            'version': __version__,
            'homepage': __homepage__,
            'docs': __docs__,
            'openapi': __openapi__
        }

        return meta

    @staticmethod
    def get_cli_meta():
        """Return default metadata for exported data."""

        meta = {
            'updated': Content.EXPORT_TIME,
            'version': __version__,
            'homepage': __homepage__
        }

        return meta

    @staticmethod
    def get_file_content(content_format, contents):
        """Return mocked file.

        The method returns file content for different content formats. Returned
        type changes depending on the content format. For example JSON and YAML
        require simple dictionary for the file content but text files require a
        Mocked open.

        Args:
            content_format (str): Content format.
            contents (dict): Content dictionary.

        Returns:
            Mock or dict: Dictionary or mocked file open depending on content.
        """

        if content_format in (Content.JSON, Content.YAML):
            return {'data': contents['data']}

        mocked_file = Const.EMPTY
        for content in contents['data']:
            if content_format == Content.TEXT:
                mocked_file = mocked_file + Content.dump_text(content)
            elif content_format == Content.MKDN:
                mocked_file = mocked_file + Content.dump_mkdn(content)
                mocked_file = mocked_file + '\n---\n\n'

        if content_format == Content.MKDN:
            mocked_file = mocked_file[:-6]  # Remove last separator for Markdown content.

        return mock.mock_open(read_data=mocked_file)

    @staticmethod
    def _get_expect_restapi(expect):
        """Return comparable dictionary from expected content.

        The expected dictionary is a default content defined for testing. The
        default content is defined to be in storage format which uses tuples
        instead of lists which are used in the REST API. This method converts
        and copies the expected content to REST API format.

        The original expected data must not be changed because it is shared
        between all tests.

        Only the responses with the 'data' key have to be modified. This key
        contains default content stored in the database format which needs to
        be modified to match the response from the JSON REST API.

        Args:
            expect (dict): Excepted JSON in REST API response.

        Returns:
            dict: Comparable JSON REST API dictionary from expected content.
        """

        def _convert(content):
            """Convert content attributes to list."""

            if 'data' in content:
                content['data'] = list(content['data'])
            if 'groups' in content:
                content['groups'] = list(content['groups'])
            if 'tags' in content:
                content['tags'] = list(content['tags'])
            if 'links' in content:
                content['links'] = list(content['links'])
            if 'versions' in content:
                content['versions'] = list(content['versions'])
            if 'uuid' in content:
                content['uuid'] = Database.VALID_UUID

        if 'data' not in expect:
            return expect

        expect = copy.deepcopy(expect)
        try:
            if isinstance(expect['data'], list):
                for data in expect['data']:
                    _convert(data['attributes'])
            else:
                _convert(expect['data']['attributes'])
        except KeyError:
            raise Exception(
                'test case failure:\n\n{}\nwith dictionary:\n{}'.format(
                    traceback.format_exc(), json.dumps(expect, sort_keys=True, indent=4)
                )
            )

        return expect

    @staticmethod
    def _get_result_restapi(result):
        """Return comparable dictionary from test case result.

        Error response from JSON API can contain error string resulted from
        REST API schema validation. This error string can be a long JSON
        structure. For simplicity and test case maintainability reasons,
        the schema validation error is masked away.

        See the description for assert_storage method.

        Args:
            result (dict): Result JSON from REST API.

        Returns:
            dict: Comparable JSON REST API dictionary frm test case result.
        """

        try:
            if isinstance(result['data'], list):
                for data in result['data']:
                    if 'uuid' in data['attributes']:
                        data['attributes']['uuid'] = Database.VALID_UUID
            else:
                if 'uuid' in result['data']['attributes']:
                    result['data']['attributes']['uuid'] = Database.VALID_UUID
        except KeyError:
            pass

        try:
            for error in result['errors']:
                if 'json media validation failed' in error['title']:
                    error['title'] = 'json media validation failed'
        except KeyError:
            pass

        return result

    @classmethod
    def _get_db_collection(cls):
        """Return comparable collection from database.

        See the description for assert_storage method.

        Returns:
            Collection(): Comparable collection from database.
        """

        collection = Database.get_collection()
        for digest in collection.keys():
            collection[digest].uuid = Database.VALID_UUID

        return collection

    @classmethod
    def _get_db_dictionary(cls, collection):
        """Return comparable dictionary from database.

        See the description for assert_storage method.

        Returns:
            dict: Comparable dictionary from database.
        """

        dictionary = {}
        dictionary['data'] = collection.dump_dict()

        return dictionary

    @classmethod
    def _get_expect_dictionary(cls, content):
        """Return comparable dictionary from expected content.

        See the description for assert_storage method.

        Args:
            content (dict): Reference content.

        Returns:
            content (dict): Comparable reference content.
        """

        content = copy.deepcopy(content)
        for data in content['data']:
            data['uuid'] = Database.VALID_UUID

        return content

    @staticmethod
    def _get_result_dictionary(content_format, mock_object):
        """Return comparable dictionary from test case result.

        See the description for assert_storage method.

        Args:
            content_format (str): Content format stored in mock.
            mock_object (obj): Mock object where content was stored.

        Returns:
            dict: Comparable dictinary from the test case mock.
        """

        dictionary = {}
        if content_format == Const.CONTENT_FORMAT_JSON:
            dictionary = mock_object.dump.mock_calls[0][1][0]
        elif content_format == Const.CONTENT_FORMAT_YAML:
            for call in mock_object.safe_dump.mock_calls:
                if 'data' not in dictionary:
                    dictionary = call[1][0]
                else:
                    dictionary['data'].append(call[1][0]['data'][0])

        for data in dictionary['data']:
            data['uuid'] = Database.VALID_UUID

        return dictionary

    @staticmethod
    def _get_result_collection(content_format, mock_object):
        """Return comparable collection from test case result.

        See the description for assert_storage method.

        Args:
            content_format (str): Content format stored in mock.
            mock_object (obj): Mock object where content was stored.

        Returns:
            Collection(): Comparable collection from test case result.
        """

        collection = Collection()
        if content_format == Const.CONTENT_FORMAT_JSON:
            for call in mock_object.dump.mock_calls:
                collection.load_dict(Content.IMPORT_TIME, call[1][0])
        elif content_format in (Const.CONTENT_FORMAT_MKDN, Const.CONTENT_FORMAT_TEXT):
            handle = mock_object.return_value.__enter__.return_value
            for call in handle.write.mock_calls:
                collection.load(content_format, Content.IMPORT_TIME, call[1][0])
        elif content_format == Const.CONTENT_FORMAT_YAML:
            for call in mock_object.safe_dump.mock_calls:
                collection.load_dict(Content.IMPORT_TIME, call[1][0])

        for digest in collection.keys():
            collection[digest].uuid = Database.VALID_UUID

        return collection

    @staticmethod
    def _get_expect_collection(content_format, content):
        """Return comparable collection from expected content.

        See the description for assert_storage method.

        Args:
            content_format (str): Content format stored in mock.
            content (dict): Reference content.

        Returns:
            Collection(): Comparable collection from expected content.
        """

        references = Collection()
        references.load_dict(Content.IMPORT_TIME, {'data': content['data']})

        for digest in references.keys():
            references[digest].uuid = Database.VALID_UUID

        if content_format == Const.CONTENT_FORMAT_TEXT:
            for digest in references.keys():
                references[digest].created = Content.IMPORT_TIME
                references[digest].updated = Content.IMPORT_TIME

        return references

    @staticmethod
    def _read_text(content_format, mock_object):
        """Return text saved in mock.

        See description for assert_storage method.

        Args:
            content_format (str): Content format stored in mock.
            mock_object (obj): Mock object where content was stored.

        Returns:
            str: String from the mocked object.
        """

        text = Const.EMPTY
        if content_format in (Const.CONTENT_FORMAT_MKDN, Const.CONTENT_FORMAT_TEXT):
            handle = mock_object.return_value.__enter__.return_value
            for call in handle.write.mock_calls:
                text = text + call[1][0]

            text = re.sub(r'uuid     : \S+', 'uuid     : ' + Database.VALID_UUID, text)

        return text

    @staticmethod
    def _print_assert(result, expect):
        """Print differences between results and expected values.

        Args:
            result: Result value from test.
            expect: Expected value defined in test.
        """

        print("=" * 120)
        if type(result) is not type(expect):
            print("Cannot compare different types.")
            print(result)
            print(expect)

            return

        if result == expect:
            print("Comparing result and expected types of {} which are equal.".format(type(expect)))

            return

        if isinstance(result, Collection):
            if expect.keys() != result.keys():
                print("Asserted collections do not have same resources.")
                print("result")
                for digest in result.keys():
                    pprintpp.pprint(result[digest].dump_dict([]))
                print("=" * 120)
                print("expect")
                for digest in expect.keys():
                    pprintpp.pprint(expect[digest].dump_dict([]))

                return

            for digest in expect.keys():
                result_dict = result[digest].dump_dict([]) if digest in result.keys() else {}
                expect_dcit = expect[digest].dump_dict([])
                pprintpp.pprint(result_dict)
                pprintpp.pprint(expect_dcit)
                fields = [field for field in result_dict if result_dict[field] != expect_dcit[field]]
                print("Differences in resource: {:.16}".format(digest))
                print("=" * 120)
                for field in fields:
                    print("result[{:.16}].{}:".format(digest, field))
                    pprintpp.pprint(result_dict[field])
                    print("expect[{:.16}].{}:".format(digest, field))
                    pprintpp.pprint(expect_dcit[field])
        elif isinstance(result, dict):
            print("Comparing result and expected types of {} which are different.".format(type(expect)))
            pprintpp.pprint(result)
            pprintpp.pprint(expect)
            fields = [field for field in expect if expect[field] != result[field]]
            print("=" * 120)
            for field in fields:
                print("result {}:".format(field))
                pprintpp.pprint(result[field])
                print("expect {}:".format(field))
                pprintpp.pprint(expect[field])
        elif isinstance(result, str):
            print("Comparing result and expected types of {} which are different.".format(type(expect)))
            print(result)
            print(expect)
        print("=" * 120)


class Field(object):  # pylint: disable=too-few-public-methods
    """Helper methods for content field testing."""

    @staticmethod
    def is_iso8601(timestamp):
        """Test if timestamp is in ISO8601 format."""

        # Python 2 does not support timezone parsing.
        #
        # The %z directive is # available only from Python 3.2 onwards.
        #
        # From Python 3.7 onwards, the datetime strptime is able to parse
        # timezone in format that includes colon delimiter in UTC offset [3].
        #
        # [1] https://bugs.python.org/issue31800
        # [2] https://stackoverflow.com/a/49784038
        # [3] https://stackoverflow.com/a/48539157
        # [4] https://github.com/python/cpython/commit/32318930da70ff03320ec50813b843e7db6fbc2e
        if Const.PYTHON37:
            try:
                datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%f%z')
            except ValueError:
                return False
        elif not Const.PYTHON2:
            try:
                timestamp = timestamp.replace('+00:00', '+0000')
                datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%f%z')
            except ValueError:
                return False
        else:
            timestamp = timestamp[:-6]  # Remove last '+00:00'.
            try:
                datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%f')
            except ValueError:
                return False

        return True
