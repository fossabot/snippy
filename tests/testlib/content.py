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

"""content: Content helpers for testing."""

import copy
import datetime
import re

import mock
import pprintpp

from snippy.cause import Cause
from snippy.config.config import Config
from snippy.constants import Constants as Const
from snippy.content.collection import Collection
from snippy.meta import __docs__
from snippy.meta import __homepage__
from snippy.meta import __openapi__
from snippy.meta import __version__
from tests.testlib.reference_helper import ReferenceHelper as Reference
from tests.testlib.snippet_helper import SnippetHelper as Snippet
from tests.testlib.solution_helper import SolutionHelper as Solution
from tests.testlib.sqlitedb_helper import SqliteDbHelper as Database

class Content(object):  # pylint: disable=too-many-public-methods
    """Helper methods for content testing."""

    # Contents
    EXPORT_TIME = '2018-02-02T02:02:02.000001+0000'
    IMPORT_TIME = '2018-03-02T02:02:02.000001+0000'

    # Snippets
    REMOVE_TIME = '2017-10-14T19:56:31.000001+0000'
    FORCED_TIME = '2017-10-14T19:56:31.000001+0000'
    EXITED_TIME = '2017-10-20T07:08:45.000001+0000'
    NETCAT_TIME = '2017-10-20T07:08:45.000001+0000'
    UMOUNT_TIME = '2018-05-07T11:11:55.000001+0000'
    INTERP_TIME = '2018-01-11T07:59:46.000001+0000'

    # Solutions
    BEATS_TIME = '2017-10-20T11:11:19.000001+0000'
    NGINX_TIME = '2017-10-20T06:16:27.000001+0000'

    # References
    GITLOG_TIME = '2018-06-22T13:11:13.678729+0000'
    REGEXP_TIME = '2018-05-21T13:11:13.678729+0000'
    PYTEST_TIME = '2016-04-21T12:10:11.678729+0000'

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
    def assert_storage(cls, content):
        """Compare content stored in database.

        The assert comparisons use equality implemented for collection data
        class. This quarantees that the count of resources in collection is
        same between expected content and in collection created from database.

        The comparison tests all but the key attribute in between references.
        The key attribute is an index in database and it cannot be compared.

        The content UUID must be unique for the database. UUID's are allocated
        in order where content is stored which can be random between different
        tests. Because of this, content UUID is always masked away.

        Text formatted content does not have created and updated fields in the
        text. Because of this, they cannot be compared against reference and
        these two fields are masked away when comparing text content.

        The original content must not be changed because it is pointing to the
        default content shared between all the tests.

        Args:
            content (dict): Excepted content compared against database.
        """

        if not content:
            assert not Database.get_collection()

            return

        references = cls._read_refs(Const.CONTENT_FORMAT_NONE, content)
        collection = Database.get_collection()
        try:
            assert references == collection
        except AssertionError:
            Content._print_assert(references, collection)
            raise AssertionError

    @classmethod
    def assert_json(cls, json, json_file, filename, content):
        """Compare JSON against expected content.

        See description for assert_storage method.

        Args:
            json (obj): Mocked JSON dump method.
            json_file (obj): Mocked file where the JSON content was saved.
            filename (str): Expected filename.
            content (dict): Excepted content compared against generated JSON.
        """

        references = cls._read_refs(Const.CONTENT_FORMAT_JSON, content)
        match_dict = cls._mask_uuid(content)
        collection = cls._read_mock(Const.CONTENT_FORMAT_JSON, json)
        saved_dict = cls._read_dict(Const.CONTENT_FORMAT_JSON, json)
        try:
            assert references == collection
            assert match_dict == saved_dict
            json_file.assert_called_once_with(filename, 'w')
        except AssertionError:
            Content._print_assert(references, collection)
            Content._print_assert(match_dict, saved_dict)
            raise AssertionError

    @classmethod
    def assert_mkdn(cls, mkdn, filename, content):
        """Compare Markdown against expected content.

        See description for assert_storage method.

        Args:
            mkdn (obj): Mocked file where the Markdown content was saved.
            filename (str): Expected filename.
            content (dict): Excepted content compared against Markdown file.
        """

        references = cls._read_refs(Const.CONTENT_FORMAT_MKDN, content)
        match_mkdn = references.dump_mkdn(Config.templates)
        collection = cls._read_mock(Const.CONTENT_FORMAT_MKDN, mkdn)
        saved_mkdn = cls._read_text(Const.CONTENT_FORMAT_MKDN, mkdn)
        try:
            mkdn.assert_called_once_with(filename, 'w')
            assert match_mkdn == saved_mkdn
            assert references == collection
        except AssertionError:
            Content._print_assert(references, collection)
            Content._print_assert(match_mkdn, saved_mkdn)
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

        references = cls._read_refs(Const.CONTENT_FORMAT_TEXT, content)
        match_text = references.dump_text(Config.templates)
        collection = cls._read_mock(Const.CONTENT_FORMAT_TEXT, text)
        saved_text = cls._read_text(Const.CONTENT_FORMAT_TEXT, text)
        try:
            text.assert_called_once_with(filename, 'w')
            assert match_text == saved_text
            assert references == collection
        except AssertionError:
            Content._print_assert(references, collection)
            Content._print_assert(match_text, saved_text)
            raise AssertionError

    @classmethod
    def assert_yaml(cls, yaml, yaml_file, filename, content):
        """Compare YAML against expected content.

        See description for assert_storage method.

        Args:
            yaml (obj): Mocked YAML dump method.
            yaml_file (obj): Mocked file where the YAML content was saved.
            filename (str): Expected filename.
            content (dict): Excepted content compared against generated YAML.
        """

        references = cls._read_refs(Const.CONTENT_FORMAT_YAML, content)
        match_dict = cls._mask_uuid(content)
        collection = cls._read_mock(Const.CONTENT_FORMAT_YAML, yaml)
        saved_dict = cls._read_dict(Const.CONTENT_FORMAT_YAML, yaml)
        try:
            assert references == collection
            assert saved_dict == match_dict
            yaml_file.assert_called_once_with(filename, 'w')
        except AssertionError:
            Content._print_assert(references, collection)
            Content._print_assert(match_dict, saved_dict)
            raise AssertionError

    @staticmethod
    def verified(mocker, snippy, content):
        """Compare given content against content stored in database."""

        mocker.patch.object(Config, 'utcnow', side_effect=(Content.EXPORT_TIME,)*len(content))
        assert len(Database.get_collection()) == len(content)
        with mock.patch('snippy.content.migrate.open', mock.mock_open()) as mock_file:
            for digest in content:
                mock_file.reset_mock()
                cause = snippy.run(['snippy', 'export', '-d', digest, '-f', 'content.txt'])
                assert cause == Cause.ALL_OK
                mock_file.assert_called_once_with('content.txt', 'w')
                file_handle = mock_file.return_value.__enter__.return_value
                file_handle.write.assert_has_calls([mock.call(Snippet.get_template(content[digest]) + Const.NEWLINE)])

    @staticmethod
    def ordered(contents):
        """Sort JSON in order to compare random order JSON structures.

        Because the 'contents' parameter may be modified in here, the data
        structure is always deep copied in order to avoid modifying the
        original which may be the content helper default JSON data.

        Args:
            contents (dict): Server response or content helper default JSON data.
        """

        contents = copy.deepcopy(contents)

        # API errors have special case that containes random order hash
        # structure inside a string. This string is masked.
        #
        # TODO: It should be possible to sort and compare this also.
        if 'errors' in contents:
            for error in contents['errors']:
                error['title'] = 'not compared because of hash structure in random order inside the string'

        # Validate predefined set of UUIDs.
        if 'data' in contents:
            if isinstance(contents['data'], list):
                for data in contents['data']:
                    if Content._is_valid_uuid(data['attributes']):
                        data['attributes']['uuid'] = Database.VALID_UUID
            else:
                if Content._is_valid_uuid(contents['data']['attributes']):
                    contents['data']['attributes']['uuid'] = Database.VALID_UUID

        # Sort the content structure in order to be able to compare it.
        json_list = []
        if isinstance(contents, list):
            json_list = (contents)
        else:
            json_list.append(contents)

        contents = []
        for content in json_list:
            contents.append(Content._sorter(content))

        return tuple(contents)

    @staticmethod
    def json_dump(json_dump, mock_file, filename, content):
        """Compare given content against yaml dump.

        Both test data and reference data must be validated for UUIDs. The
        list of UUIDs is predefined but it must be unique so each content may
        have any of the valid UUIDs.

        Because the 'content' parameter may be modified in here, the data
        structure is always deep copied in order to avoid modifying the
        original which may be the content helper default JSON data.

        Args:
            json_dump (obj): Mocked yaml object.
            mock_file (obj): Mocked file object.
            filename (str): Expected filename used to for mocked file.
            content (str): Content expected to be dumped into JSON file.
        """

        content = copy.deepcopy(content)

        dictionary = json_dump.dump.mock_calls[0][1][0]
        for data in content['data']:
            if Content._is_valid_uuid(data):
                data['uuid'] = Database.VALID_UUID

        for data in dictionary['data']:
            if Content._is_valid_uuid(data):
                data['uuid'] = Database.VALID_UUID
        mock_file.assert_called_once_with(filename, 'w')
        json_dump.dump.assert_called_with(content, mock.ANY)

    @staticmethod
    def text_dump(mock_file, filename, content):
        """Compare given content against yaml dump.

        Args:
            mock_file (obj): Mocked file where the text content was saved.
            filename (str): Expected filename.
            content (dict): Excepted content.
        """

        references = Const.EMPTY
        content = copy.deepcopy(content)
        for data in content['data']:
            references = references + Reference.dump(data, Content.TEXT)
            references = references + '\n'
        references = [references]

        mock_calls = []
        handle = mock_file.return_value.__enter__.return_value
        for call in handle.write.mock_calls:
            mock_calls.append(call[1][0])
        try:
            mock_file.assert_called_once_with(filename, 'w')
            assert mock_calls == references
        except AssertionError:
            Content._print_compare(mock_file, mock_calls, references, filename)
            raise AssertionError

    @staticmethod
    def yaml_dump(yaml_dump, mock_file, filename, content, call=0):
        """Compare given content against yaml dump.

        Both test data and reference data must be validated for UUIDs. The
        list of UUIDs is predefined but it must be unique so each content may
        have any of the valid UUIDs.

        Because the 'content' parameter may be modified in here, the data
        structure is always deep copied in order to avoid modifying the
        original which may be the content helper default JSON data.

        Args:
            yaml_dump (obj): Mocked yaml object.
            mock_file (obj): Mocked file object.
            filename (str): Expected filename used to for mocked file.
            content (str): Content expected to be dumped into YAML file.
            call (int): The call order number for yaml dump.
        """

        content = copy.deepcopy(content)
        for data in content['data']:
            if Content._is_valid_uuid(data):
                data['uuid'] = Database.VALID_UUID

        dictionary = yaml_dump.safe_dump.mock_calls[call][1][0]
        for data in dictionary['data']:
            if Content._is_valid_uuid(data):
                data['uuid'] = Database.VALID_UUID

        try:
            mock_file.assert_any_call(filename, 'w')
            yaml_dump.safe_dump.assert_any_call(content, mock.ANY, default_flow_style=mock.ANY)
        except AssertionError:
            print("===REFERENCES===")
            pprintpp.pprint(content)
            print("===MOCK_CALLS===")
            pprintpp.pprint(yaml_dump.safe_dump.mock_calls[0][1][0])
            print("================")

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
    def imported_dict(content_read):
        """Return imported dictionary from content."""

        return {'data': list(content_read.values())}

    @staticmethod
    def mocked_open(content_read):
        """Return mocked open from content."""

        mocked_open = Const.EMPTY
        for item in content_read.values():
            mocked_open = mocked_open + Snippet.get_template(item) + Const.NEWLINE

        return mock.mock_open(read_data=mocked_open)

    @staticmethod
    def mocked_file(content, content_format):
        """Return mocked file.

        The method returns a mocked file which returns a string in requested
        content format.

        Args:
            content (dict): Content in dictionary.
            content_format (str): Content format.

        Returns:
            str: Mocked file open.
        """

        mocked_file = Const.EMPTY
        for item in content.values():
            mocked_file = mocked_file + Snippet.dump(item, content_format)
            if content_format == Content.MKDN:
                mocked_file = mocked_file + '\n---\n\n'

        if content_format == Content.MKDN:
            mocked_file = mocked_file[:-6]  # Remove last separator for Markdown content.

        return mock.mock_open(read_data=mocked_file)

    @staticmethod
    def updated_nginx():
        """Return updated nginx solution."""

        # Generate updated nginx solution.
        content_read = {
            'af2c51570a909031': copy.deepcopy(Solution.DEFAULTS[Solution.NGINX])
        }
        content_read['af2c51570a909031']['data'] = tuple([w.replace('# Instructions how to debug nginx.', '# Changed instruction set.') for w in content_read['af2c51570a909031']['data']])  # pylint: disable=line-too-long
        content_read['af2c51570a909031']['description'] = 'Changed instruction set.'

        return content_read

    @staticmethod
    def updated_kafka1():
        """Return updated kafka solution."""

        # Generate updated kafka solution. No FILE defined.
        content_read = {
            '3cbade9454ac80d2': copy.deepcopy(Solution.DEFAULTS[Solution.KAFKA])
        }
        content_read['3cbade9454ac80d2']['data'] = tuple([w.replace('## FILE   : kubernetes-docker-log-driver-kafka.txt', '## FILE   : ') for w in content_read['3cbade9454ac80d2']['data']])  # pylint: disable=line-too-long
        content_read['3cbade9454ac80d2']['filename'] = Const.EMPTY
        content_read['3cbade9454ac80d2']['digest'] = '3cbade9454ac80d20eb1b8300dc7537a3851c078791b6e69af48e289c9d62e09'

        return content_read

    @staticmethod
    def updated_kafka2():
        """Return updated kafka solution."""

        # Generate updated kafka solution. No space after FILE.
        content_read = {
            'fb657e3b49deb5b8': copy.deepcopy(Solution.DEFAULTS[Solution.KAFKA])
        }
        content_read['fb657e3b49deb5b8']['data'] = tuple([w.replace('## FILE   : kubernetes-docker-log-driver-kafka.txt', '## FILE   :') for w in content_read['fb657e3b49deb5b8']['data']])  # pylint: disable=line-too-long
        content_read['fb657e3b49deb5b8']['filename'] = Const.EMPTY
        content_read['fb657e3b49deb5b8']['digest'] = 'fb657e3b49deb5b8e55bb2aa3e81aef4fe54a161a26be728791fb6d4a423f560'

        return content_read

    @staticmethod
    def updated_kafka3():
        """Return updated kafka solution."""

        # Generate updated kafka solution. Spaces around filename.
        content_read = {
            '21c1d813c414aec8': copy.deepcopy(Solution.DEFAULTS[Solution.KAFKA])
        }
        content_read['21c1d813c414aec8']['data'] = tuple([w.replace('## FILE   : kubernetes-docker-log-driver-kafka.txt', '## FILE   :  kubernetes-docker-log-driver-kafka.txt ') for w in content_read['21c1d813c414aec8']['data']])  # pylint: disable=line-too-long
        content_read['21c1d813c414aec8']['filename'] = Const.EMPTY

        return content_read

    @staticmethod
    def updated_gitlog():
        """Return updated gitlog reference."""

        # Generate updated nginx solution.
        content_read = {
            Reference.GITLOG_DIGEST: copy.deepcopy(Reference.DEFAULTS[Reference.GITLOG])
        }
        content_read[Reference.GITLOG_DIGEST]['data'] = tuple([w.replace('# Instructions how to debug nginx', '# Changed instruction set') for w in content_read[Reference.GITLOG_DIGEST]['data']])  # pylint: disable=line-too-long

        return content_read

    @classmethod
    def _mask_uuid(cls, content):
        """Mask UUID from given content.

        See description for assert_storage method.

        Args:
            content (dict): Reference content.

        Returns:
            content (dict): Reference content with constant UUDI.
        """

        content = cls.deepcopy(content)
        for data in content['data']:
            data['uuid'] = Database.VALID_UUID

        return content

    @staticmethod
    def _read_dict(content_format, mock_object):
        """Return dictionary from mock.

        See description for assert_storage method.

        Args:
            content_format (str): Content format stored in mock.
            mock_object (obj): Mock object where content was stored.

        Returns:
            dict: Dictinary from the mocked object.
        """

        dictionary = {}
        if content_format == Const.CONTENT_FORMAT_JSON:
            dictionary = mock_object.dump.mock_calls[0][1][0]
        elif content_format == Const.CONTENT_FORMAT_YAML:
            dictionary = mock_object.safe_dump.mock_calls[0][1][0]

        for data in dictionary['data']:
            data['uuid'] = Database.VALID_UUID

        return dictionary

    @staticmethod
    def _read_mock(content_format, mock_object):
        """Return collection from mock.

        See description for assert_storage method.

        Args:
            content_format (str): Content format stored in mock.
            mock_object (obj): Mock object where content was stored.

        Returns:
            Collection(): Collection of resources read from the file.
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
    def _read_refs(content_format, content):
        """Return collection from content.

        See description for assert_storage method.

        Args:
            content_format (str): Content format stored in mock.
            content (dict): Reference content.

        Returns:
            Collection(): Collection of resources read from content.
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
    def _sorter(json):
        """Sort nested JSON to allow comparison."""

        if isinstance(json, dict):
            return sorted((k, Content._sorter(v)) for k, v in json.items())
        if isinstance(json, (list, tuple)):
            return sorted(Content._sorter(x) for x in json)

        return json

    @staticmethod
    def _is_valid_uuid(content):
        """Test if content UUID is valid.

        UUID can be any of the UUID's allocated for testing. Because the test
        case can contain contentn in any order, the test UUID's can be used in
        random order. Therefore the content UUID must be checked from list of
        valid UUID's.

        It may be that the UUDI field is not returned by a server for example
        when user limits the returned fields. Because of this, missing field is
        considered valid.
        """

        if 'uuid' not in content:
            return True

        if content['uuid'] in Database.TEST_UUIDS_STR:
            return True

        return False

    @staticmethod
    def _print_assert(expect, actual):
        """Find and print differences between expected and actual values.

        Args:
            expect: Expected value.
            actual: Actual value
        """

        print("=" * 120)
        if type(expect) is not type(actual):
            print("Cannot compare different types.")

            return

        if expect == actual:
            print("Comparing expexted and actual types of {} which are equal.".format(type(expect)))

            return

        if isinstance(expect, Collection):
            if expect.keys() != actual.keys():
                print("Asserted collections do not have same resources.")
                print("expect")
                for digest in expect.keys():
                    pprintpp.pprint(expect[digest].dump_dict([]))
                print("actual")
                for digest in actual.keys():
                    pprintpp.pprint(actual[digest].dump_dict([]))
                print("=" * 120)

                return

            for digest in expect.keys():
                content1 = expect[digest].dump_dict([])
                content2 = actual[digest].dump_dict([]) if digest in actual.keys() else {}
                pprintpp.pprint(content1)
                pprintpp.pprint(content2)
                fields = [field for field in content1 if content1[field] != content2[field]]
                print("Differences in resource: {:.16}".format(digest))
                print("=" * 120)
                for field in fields:
                    print("expect[{:.16}].{}:".format(digest, field))
                    pprintpp.pprint(content1[field])
                    print("actual[{:.16}].{}:".format(digest, field))
                    pprintpp.pprint(content2[field])
        elif isinstance(expect, dict):
            print("Comparing expexted and actual types of {} which are different.".format(type(expect)))
            pprintpp.pprint(expect)
            pprintpp.pprint(actual)
            fields = [field for field in expect if expect[field] != actual[field]]
            print("=" * 120)
            for field in fields:
                print("expect {}:".format(field))
                pprintpp.pprint(expect[field])
                print("actual {}:".format(field))
                pprintpp.pprint(expect[field])
        elif isinstance(expect, str):
            print("Comparing expexted and actual types of {} which are different.".format(type(expect)))
            print(expect)
            print(actual)
        print("=" * 120)

    @staticmethod
    def _print_compare(mock_file, mock_calls, references, filename):  # pylint: disable=too-many-locals
        """Print comparison data.

        Compare mock and references so that the first difference is searched
        and then add few extra lines after first failure. The failure and all
        following lines are colored differently from standard line color.

        The comparing output is printed side by side from mock and references.
        """

        # Color code lengths must be equal to align output correctly. Also when
        # the failure colors are added, the normal coloring is removed in order
        # to maintain correct text alignment.
        fail = '\033[1m'
        succ = '\x1b[2m'
        endc = '\x1b[0m'
        references = references[0].splitlines()
        if mock_calls:
            mock_calls = mock_calls[0].splitlines()
        else:
            mock_calls = [Const.EMPTY] * len(references)
        references = [succ + line + endc for line in references]
        mock_calls = [succ + line + endc for line in mock_calls]
        idx = 0
        failure = False
        for idx, line in enumerate(references):
            if line != mock_calls[idx]:
                failure = True
                break
        if failure:
            references = references[0:idx+5]
            mock_calls = mock_calls[0:idx+5]
            for i in range(idx, len(references)):
                references[i] = fail + Const.RE_MATCH_ANSI_ESCAPE_SEQUENCES.sub('', references[i]) + endc
                mock_calls[i] = fail + Const.RE_MATCH_ANSI_ESCAPE_SEQUENCES.sub('', mock_calls[i]) + endc
        max_len = len(max(references+mock_calls, key=len))
        compare = Const.NEWLINE.join("| {:<{len}} | {:{len}}".format(x, y, len=max_len) for x, y in zip(references, mock_calls))

        print('+' + "=" *(max_len*2))
        reference_file = filename + ' - w'
        mock_call_file = mock_file.mock_calls[0][1][0] + ' - ' + mock_file.mock_calls[0][1][1]
        max_len_header = max_len-len(succ)-len(endc)- len('references: ')
        print("| references: {:<{len}} | mock calls: {:{len}}".format(reference_file, mock_call_file, len=max_len_header))
        print('+' + "=" *(max_len*2))
        print(compare)
        print('+' + "=" *(max_len*2))


class Field(object):  # pylint: disable=too-few-public-methods
    """Helper methods for content field testing."""

    @staticmethod
    def is_iso8601(timestamp):
        """Test if timestamp is in ISO8601 format."""

        # Python 2 does not support timezone parsing. The %z directive is
        # available only from Python 3.2 onwards.
        if not Const.PYTHON2:
            try:
                datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%f%z')
            except ValueError:
                return False
        else:
            timestamp = timestamp[:-5]  # Remove last '+0000'.
            try:
                datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%f')
            except ValueError:
                return False

        return True
