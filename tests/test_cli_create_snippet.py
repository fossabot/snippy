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

"""test_cli_create_snippet: Test workflows for creating snippets."""

import pytest

from snippy.cause import Cause
from snippy.constants import Constants as Const
from tests.testlib.content import Content
from tests.testlib.snippet_helper import SnippetHelper as Snippet
from tests.testlib.sqlitedb_helper import SqliteDbHelper as Database


class TestCliCreateSnippet(object):
    """Test workflows for creating snippets."""

    def test_cli_create_snippet_001(self, snippy, mocker):
        """Create snippet from CLI.

        Create new snippet by defining all content parameters from command
        line.
        """

        content_read = {Snippet.REMOVE_DIGEST: Snippet.DEFAULTS[Snippet.REMOVE]}
        data = Const.NEWLINE.join(Snippet.DEFAULTS[Snippet.REMOVE]['data'])
        brief = Snippet.DEFAULTS[Snippet.REMOVE]['brief']
        groups = Const.DELIMITER_GROUPS.join(Snippet.DEFAULTS[Snippet.REMOVE]['groups'])
        tags = Const.DELIMITER_TAGS.join(Snippet.DEFAULTS[Snippet.REMOVE]['tags'])
        links = Const.DELIMITER_LINKS.join(Snippet.DEFAULTS[Snippet.REMOVE]['links'])
        cause = snippy.run(['snippy', 'create', '--content', data, '--brief', brief, '--groups', groups, '--tags', tags, '--links', links])  # pylint: disable=line-too-long
        assert cause == Cause.ALL_OK
        assert Database.get_snippets().size() == 1
        Content.verified(mocker, snippy, content_read)

    def test_cli_create_snippet_002(self, snippy, mocker):
        """Create snippet from CLI.

        Create new snippet with all content parameters but only one tag.
        """

        snippet_remove = Snippet.DEFAULTS[Snippet.REMOVE].copy()
        snippet_remove['tags'] = [Snippet.DEFAULTS[Snippet.REMOVE]['tags'][0]]
        content_read = {'f94cf88b1546a8fd': snippet_remove}
        data = Const.NEWLINE.join(Snippet.DEFAULTS[Snippet.REMOVE]['data'])
        brief = Snippet.DEFAULTS[Snippet.REMOVE]['brief']
        groups = Const.DELIMITER_GROUPS.join(Snippet.DEFAULTS[Snippet.REMOVE]['groups'])
        tags = Snippet.DEFAULTS[Snippet.REMOVE]['tags'][0]
        links = Const.DELIMITER_LINKS.join(Snippet.DEFAULTS[Snippet.REMOVE]['links'])
        cause = snippy.run(['snippy', 'create', '--content', data, '--brief', brief, '--groups', groups, '--tags', tags, '--links', links])  # pylint: disable=line-too-long
        assert cause == Cause.ALL_OK
        assert Database.get_snippets().size() == 1
        Content.verified(mocker, snippy, content_read)

    def test_cli_create_snippet_003(self, snippy):
        """Try to create snippet from CLI.

        Try to create new snippet without defining mandatory content data.
        """

        brief = Snippet.DEFAULTS[Snippet.REMOVE]['brief']
        groups = Const.DELIMITER_GROUPS.join(Snippet.DEFAULTS[Snippet.REMOVE]['groups'])
        tags = Const.DELIMITER_TAGS.join(Snippet.DEFAULTS[Snippet.REMOVE]['tags'])
        links = Const.DELIMITER_LINKS.join(Snippet.DEFAULTS[Snippet.REMOVE]['links'])
        cause = snippy.run(['snippy', 'create', '--brief', brief, '--groups', groups, '--tags', tags, '--links', links])
        assert cause == 'NOK: content was not stored because mandatory content field data is empty'
        assert not Database.get_snippets().size()

    @pytest.mark.usefixtures('edit-snippet-template')
    def test_cli_create_snippet_004(self, snippy):
        """Try to create snippet from CLI.

        Try to create new snippet without any changes to snippet template.
        """

        cause = snippy.run(['snippy', 'create', '--editor'])
        assert cause == 'NOK: content was not stored because mandatory content field data is empty'
        assert not Database.get_snippets().size()

    @pytest.mark.usefixtures('edit-empty')
    def test_cli_create_snippet_005(self, snippy):
        """Try to create snippet from CLI.

        Try to create new snippet with empty data. In this case the whole
        template is deleted and the edited solution is an empty string.
        """

        cause = snippy.run(['snippy', 'create', '--editor'])
        assert cause == 'NOK: could not identify edited content category - please keep tags in place'
        assert not Database.get_snippets().size()

    @pytest.mark.usefixtures('default-snippets', 'edit-remove')
    def test_cli_create_snippet_006(self, snippy, mocker):
        """Try to create snippet from CLI.

        Try to create snippet again with exactly same content than already
        stored.
        """

        content_read = {
            Snippet.REMOVE_DIGEST: Snippet.DEFAULTS[Snippet.REMOVE],
            Snippet.FORCED_DIGEST: Snippet.DEFAULTS[Snippet.FORCED]
        }
        data = Const.NEWLINE.join(Snippet.DEFAULTS[Snippet.REMOVE]['data'])
        brief = Snippet.DEFAULTS[Snippet.REMOVE]['brief']
        groups = Const.DELIMITER_GROUPS.join(Snippet.DEFAULTS[Snippet.REMOVE]['groups'])
        tags = Const.DELIMITER_TAGS.join(Snippet.DEFAULTS[Snippet.REMOVE]['tags'])
        links = Const.DELIMITER_LINKS.join(Snippet.DEFAULTS[Snippet.REMOVE]['links'])
        cause = snippy.run(['snippy', 'create', '--content', data, '--brief', brief, '--groups', groups, '--tags', tags, '--links', links])  # pylint: disable=line-too-long
        assert cause == 'NOK: content data already exist with digest: 54e41e9b52a02b63'
        assert Database.get_snippets().size() == 2
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('create-remove-utc')
    def test_cli_create_snippet_007(self, snippy, mocker, capsys):
        """Create snippet with unicode characters from CLI.

        Every field that can be given from command line contains unicode
        characters. The same content must be found by searching it with
        keyword that contains unicode characters.
        """

        data = Const.DELIMITER_DATA.join(['Sîne klâwen durh die wolken sint geslagen', 'er stîget ûf mit grôzer kraft'])
        brief = 'Tagelied of Wolfram von Eschenbach Sîne klâwen'
        groups = 'Düsseldorf'
        tags = Const.DELIMITER_TAGS.join(['γλώσσα', 'έδωσαν', 'ελληνική'])
        links = Const.DELIMITER_LINKS.join(['http://www.чухонца.edu/~fdc/utf8/'])
        content_read = {
            'data': [u'Sîne klâwen durh die wolken sint geslagen', u'er stîget ûf mit grôzer kraft'],
            'brief': u'Tagelied of Wolfram von Eschenbach Sîne klâwen',
            'groups': [u'Düsseldorf'],
            'tags': [u'γλώσσα', u'έδωσαν', u'ελληνική'],
            'links': [u'http://www.чухонца.edu/~fdc/utf8/'],
            'category': 'snippet',
            'name': '',
            'filename': '',
            'versions': '',
            'created': Content.REMOVE_TIME,
            'updated': Content.REMOVE_TIME,
            'digest': 'a74d83df95d5729aceffc472433fea4d5e3fd2d87b510112fac264c741f20438'
        }
        content = {'a74d83df95d572': content_read}
        cause = snippy.run(['snippy', 'create', '--content', data, '--brief', brief, '--groups', groups, '--tags', tags, '--links', links])  # pylint: disable=line-too-long
        assert cause == Cause.ALL_OK
        assert Database.get_snippets().size() == 1
        Content.verified(mocker, snippy, content)

        output = (
            u'1. Tagelied of Wolfram von Eschenbach Sîne klâwen @Düsseldorf [a74d83df95d5729a]',
            u'',
            u'   $ Sîne klâwen durh die wolken sint geslagen',
            u'   $ er stîget ûf mit grôzer kraft',
            u'',
            u'   # έδωσαν,γλώσσα,ελληνική',
            u'   > http://www.чухонца.edu/~fdc/utf8/',
            u'',
            u'OK',
            u''
        )
        out, err = capsys.readouterr()  # Resets the previous output in the capture buffer.
        cause = snippy.run(['snippy', 'search', '--sall', 'klâwen', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    def test_cli_create_snippet_008(self, snippy, mocker, capsys):
        """Create snippet from CLI.

        Create new snippet with three groups. The groups must be sorted when
        they are printed.
        """

        snippet_remove = Snippet.DEFAULTS[Snippet.REMOVE].copy()
        snippet_remove['groups'] = ['docker', 'moby', 'dockerfile']
        content_read = {'03dc5d1629b25627': snippet_remove}
        content_read['03dc5d1629b25627']['groups'] = sorted(content_read['03dc5d1629b25627']['groups'])
        data = Const.NEWLINE.join(Snippet.DEFAULTS[Snippet.REMOVE]['data'])
        brief = Snippet.DEFAULTS[Snippet.REMOVE]['brief']
        groups = Const.DELIMITER_GROUPS.join(snippet_remove['groups'])
        tags = Const.DELIMITER_TAGS.join(Snippet.DEFAULTS[Snippet.REMOVE]['tags'])
        links = Const.DELIMITER_LINKS.join(Snippet.DEFAULTS[Snippet.REMOVE]['links'])
        cause = snippy.run(['snippy', 'create', '--content', data, '--brief', brief, '--groups', groups, '--tags', tags, '--links', links])  # pylint: disable=line-too-long
        assert cause == Cause.ALL_OK
        assert Database.get_snippets().size() == 1
        Content.verified(mocker, snippy, content_read)

        output = (
            '1. Remove all docker containers with volumes @docker,dockerfile,moby [03dc5d1629b25627]',
            '',
            '   $ docker rm --volumes $(docker ps --all --quiet)',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '',
            'OK',
            ''
        )
        out, err = capsys.readouterr()  # Resets the previous output in the capture buffer.
        cause = snippy.run(['snippy', 'search', '--sall', 'dockerfile', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        Database.delete_all_contents()
        Database.delete_storage()
