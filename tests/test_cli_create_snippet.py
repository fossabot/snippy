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

"""test_cli_create_snippet: Test workflows for creating snippets."""

import pytest

from snippy.cause import Cause
from snippy.constants import Constants as Const
from tests.testlib.content import Content
from tests.testlib.snippet import Snippet


class TestCliCreateSnippet(object):
    """Test workflows for creating snippets."""

    @pytest.mark.usefixtures('create-remove-utc')
    def test_cli_create_snippet_001(self, snippy):
        """Create snippet from CLI.

        Create new snippet by defining all content parameters from command
        line.
        """

        content = {
            'data': [
                Snippet.REMOVE
            ]
        }
        data = Const.DELIMITER_DATA.join(content['data'][0]['data'])
        brief = content['data'][0]['brief']
        groups = Const.DELIMITER_GROUPS.join(content['data'][0]['groups'])
        tags = Const.DELIMITER_TAGS.join(content['data'][0]['tags'])
        links = Const.DELIMITER_LINKS.join(content['data'][0]['links'])
        cause = snippy.run(['snippy', 'create', '--content', data, '--brief', brief, '--groups', groups, '--tags', tags, '--links', links])  # pylint: disable=line-too-long
        assert cause == Cause.ALL_OK
        Content.assert_storage(content)

    @pytest.mark.usefixtures('create-remove-utc')
    def test_cli_create_snippet_002(self, snippy):
        """Create snippet from CLI.

        Create new snippet with all content parameters but only one tag.
        """

        content = {
            'data': [
                Content.deepcopy(Snippet.REMOVE)
            ]
        }
        content['data'][0]['tags'] = (content['data'][0]['tags'][0],)
        content['data'][0]['digest'] = 'f94cf88b1546a8fd5cb442d39f5d598cee6db666a0577de3c6e046782b339a59'
        data = Const.DELIMITER_DATA.join(content['data'][0]['data'])
        brief = content['data'][0]['brief']
        groups = Const.DELIMITER_GROUPS.join(content['data'][0]['groups'])
        tags = Const.DELIMITER_TAGS.join(content['data'][0]['tags'])
        links = Const.DELIMITER_LINKS.join(content['data'][0]['links'])
        cause = snippy.run(['snippy', 'create', '--content', data, '--brief', brief, '--groups', groups, '--tags', tags, '--links', links])  # pylint: disable=line-too-long
        assert cause == Cause.ALL_OK
        Content.assert_storage(content)

    def test_cli_create_snippet_003(self, snippy):
        """Try to create snippet from CLI.

        Try to create new snippet without defining mandatory content data.
        """

        content = {
            'data': [
                Snippet.REMOVE
            ]
        }
        brief = content['data'][0]['brief']
        groups = content['data'][0]['groups']
        tags = content['data'][0]['tags']
        links = content['data'][0]['links']
        cause = snippy.run(['snippy', 'create', '--brief', brief, '--groups', groups, '--tags', tags, '--links', links, '--no-editor'])
        assert cause == 'NOK: content was not stored because mandatory content field data is empty'
        Content.assert_storage(None)

    @pytest.mark.usefixtures('edit-snippet-template')
    def test_cli_create_snippet_004(self, snippy):
        """Try to create snippet from CLI.

        Try to create new snippet without any changes to snippet template.
        """

        cause = snippy.run(['snippy', 'create', '--editor', '--format', 'text'])
        assert cause == 'NOK: content was not stored because it was matching to an empty template'
        Content.assert_storage(None)

    @pytest.mark.usefixtures('edit-empty')
    def test_cli_create_snippet_005(self, snippy):
        """Try to create snippet from CLI.

        Try to create new snippet with empty data. In this case the whole
        template is deleted and the edited solution is an empty string.
        """

        cause = snippy.run(['snippy', 'create', '--editor', '--format', 'text'])
        assert cause == 'NOK: could not identify content category - please keep template tags in place'
        Content.assert_storage(None)

    @pytest.mark.usefixtures('default-snippets', 'edit-remove')
    def test_cli_create_snippet_006(self, snippy):
        """Try to create snippet from CLI.

        Try to create snippet again with exactly same content than already
        stored.
        """

        content = {
            'data': [
                Snippet.REMOVE,
                Snippet.FORCED
            ]
        }
        data = Const.DELIMITER_DATA.join(content['data'][0]['data'])
        brief = content['data'][0]['brief']
        groups = content['data'][0]['groups']
        tags = content['data'][0]['tags']
        links = content['data'][0]['links']
        cause = snippy.run(['snippy', 'create', '--content', data, '--brief', brief, '--groups', groups, '--tags', tags, '--links', links])  # pylint: disable=line-too-long
        assert cause == 'NOK: content data already exist with digest 54e41e9b52a02b63'
        Content.assert_storage(content)

    @pytest.mark.usefixtures('create-remove-utc')
    def test_cli_create_snippet_007(self, snippy, capsys):
        """Create snippet with unicode characters from CLI.

        Every field that can be given from command line contains unicode
        characters. The same content must be found by searching it with
        keyword that contains unicode characters.
        """

        content = {
            'data': [{
                'data': (u'Sîne klâwen durh die wolken sint geslagen', u'er stîget ûf mit grôzer kraft'),
                'brief': u'Tagelied of Wolfram von Eschenbach Sîne klâwen',
                'description': '',
                'groups': (u'Düsseldorf',),
                'tags': (u'έδωσαν', u'γλώσσα', u'ελληνική'),
                'links': (u'http://www.чухонца.edu/~fdc/utf8/',),
                'category': 'snippet',
                'name': '',
                'filename': '',
                'versions': (),
                'source': '',
                'created': Content.REMOVE_TIME,
                'updated': Content.REMOVE_TIME,
                'digest': 'a74d83df95d5729aceffc472433fea4d5e3fd2d87b510112fac264c741f20438'
            }]
        }
        data = Const.DELIMITER_DATA.join(content['data'][0]['data'])
        brief = content['data'][0]['brief']
        groups = Const.DELIMITER_GROUPS.join(content['data'][0]['groups'])
        tags = Const.DELIMITER_TAGS.join(content['data'][0]['tags'])
        links = Const.DELIMITER_LINKS.join(content['data'][0]['links'])
        cause = snippy.run(['snippy', 'create', '--content', data, '--brief', brief, '--groups', groups, '--tags', tags, '--links', links])  # pylint: disable=line-too-long
        assert cause == Cause.ALL_OK
        Content.assert_storage(content)

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
        out, err = capsys.readouterr()
        cause = snippy.run(['snippy', 'search', '--sall', 'klâwen', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    @pytest.mark.usefixtures('create-remove-utc')
    def test_cli_create_snippet_008(self, snippy, capsys):
        """Create snippet from CLI.

        Create new snippet with three groups. The groups must be sorted when
        they are printed.
        """

        content = {
            'data': [
                Content.deepcopy(Snippet.REMOVE)
            ]
        }
        content['data'][0]['groups'] = ('docker', 'dockerfile', 'moby')
        content['data'][0]['digest'] = '03dc5d1629b256271a6f2bf16abdc8f5d6f4f94f6deef9e79288792e41e32fe7'
        data = Const.DELIMITER_DATA.join(content['data'][0]['data'])
        brief = content['data'][0]['brief']
        groups = content['data'][0]['groups']
        tags = Const.DELIMITER_TAGS.join(content['data'][0]['tags'])
        links = Const.DELIMITER_LINKS.join(content['data'][0]['links'])
        cause = snippy.run(['snippy', 'create', '--content', data, '--brief', brief, '--groups', groups, '--tags', tags, '--links', links])  # pylint: disable=line-too-long
        assert cause == Cause.ALL_OK
        Content.assert_storage(content)

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
        out, err = capsys.readouterr()
        cause = snippy.run(['snippy', 'search', '--sall', 'dockerfile', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    @pytest.mark.usefixtures('create-remove-utc')
    def test_cli_create_snippet_009(self, snippy, editor_data):
        """Create snippet with editor.

        Create new snippet by using the default Markdown template. All values
        are set with editor. The template is defined in this on purpose. This
        tries to make sure that the testing framework does not hide possible
        problems if the template would be generated automatically.
        """

        content = {
            'data': [
                Snippet.REMOVE
            ]
        }
        template = (
            '# Add brief title for content @groups',
            '',
            '> Add a description that defines the content in one chapter.',
            '',
            '> [1] https://www.example.com/add-links-here.html',
            '',
            '`$ commands between backtics and prefixed by dollar sign`',
            '',
            '## Meta',
            '',
            '> category : snippet  ',
            'created  : 2017-10-14T19:56:31.000001+00:00  ',
            'digest   : ' + Snippet.TEMPLATE_DIGEST_MKDN + '  ',
            'filename :   ',
            'name     :   ',
            'source   :   ',
            'tags     : comma,separated,tags  ',
            'updated  : 2017-10-14T19:56:31.000001+00:00  ',
            'uuid     : 11cd5827-b6ef-4067-b5ac-3ceac07dde9f  ',
            'versions : ',
            ''
        )
        edited = (
            '# Remove all docker containers with volumes @docker',
            '',
            '> ',
            '',
            '> [1] https://docs.docker.com/engine/reference/commandline/rm/',
            '',
            '`$ docker rm --volumes $(docker ps --all --quiet)`',
            '',
            '## Meta',
            '',
            '> category : snippet  ',
            'created  : 2017-10-14T19:56:31.000001+00:00  ',
            'digest   : 18473ec207798670c302fb711a40df6555e8973e26481e4cd6b2ed205f5e633c  ',
            'filename :   ',
            'name     :   ',
            'source   :   ',
            'tags     : cleanup,container,docker,docker-ce,moby  ',
            'updated  : 2017-10-14T19:56:31.000001+00:00  ',
            'uuid     : 24cd5827-b6ef-4067-b5ac-3ceac07dde9f  ',
            'versions : ',
            '')
        editor_data.return_value = '\n'.join(edited)
        cause = snippy.run(['snippy', 'create', '--editor'])
        assert cause == Cause.ALL_OK
        editor_data.assert_called_with('\n'.join(template))
        Content.assert_storage(content)

    @pytest.mark.usefixtures('create-remove-utc')
    def test_cli_create_snippet_010(self, snippy, editor_data):
        """Try to create snippet with editor.

        Try to create new snippet by using the default Markdown template. In
        this case there are no any changes to the template.
        """

        template = (
            '# Add brief title for content @groups',
            '',
            '> Add a description that defines the content in one chapter.',
            '',
            '> [1] https://www.example.com/add-links-here.html',
            '',
            '`$ commands between backtics and prefixed by dollar sign`',
            '',
            '## Meta',
            '',
            '> category : snippet  ',
            'created  : 2017-10-14T19:56:31.000001+00:00  ',
            'digest   : ' + Snippet.TEMPLATE_DIGEST_MKDN + '  ',
            'filename :   ',
            'name     :   ',
            'source   :   ',
            'tags     : comma,separated,tags  ',
            'updated  : 2017-10-14T19:56:31.000001+00:00  ',
            'uuid     : 11cd5827-b6ef-4067-b5ac-3ceac07dde9f  ',
            'versions : ',
            ''
        )
        edited = template
        editor_data.return_value = '\n'.join(edited)
        cause = snippy.run(['snippy', 'create', '--editor'])
        assert cause == 'NOK: content was not stored because it was matching to an empty template'
        editor_data.assert_called_with('\n'.join(template))
        Content.assert_storage(None)

    @pytest.mark.usefixtures('create-remove-utc')
    def test_cli_create_snippet_011(self, snippy):
        """Try to create snippet from CLI.

        Try to create new snippet by from command line with --no-editor option
        when the mandatory data is not defined.
        """

        cause = snippy.run(['snippy', 'create', '--brief', 'Short brief', '--no-editor'])
        assert cause == 'NOK: content was not stored because mandatory content field data is empty'
        Content.assert_storage(None)

    @pytest.mark.usefixtures('create-remove-utc')
    def test_cli_create_snippet_012(self, snippy, editor_data):
        """Create snippet with editor.

        Create new snippet and define tags and brief already from command line.
        Other fields must have the default template content that is normally
        presented for the user when content is created with editor.

        User adds the content data from editor.

        Editor must be used by default.
        """

        content = {
            'data': [{
                'brief': 'Brief from cli',
                'category': 'snippet',
                'created': '2017-10-14T19:56:31.000001+00:00',
                'data': ('docker rm --volumes $(docker ps --all --quiet)', ),
                'description': 'Add a description that defines the content in one chapter.',
                'digest': '7c6c1d7b742581d056508d67046e5852e738f2f90fa982b1bd3fa695b9e231eb',
                'filename': '',
                'groups': ('groups', ),
                'links': ('https://www.example.com/add-links-here.html', ),
                'name': '',
                'source': '',
                'tags': ('cli', 'from', 'tags'),
                'updated': '2017-10-14T19:56:31.000001+00:00',
                'uuid': '11cd5827-b6ef-4067-b5ac-3ceac07dde9f',
                'versions': (),
            }]
        }
        template = (
            '# Brief from cli @groups',
            '',
            '> Add a description that defines the content in one chapter.',
            '',
            '> [1] https://www.example.com/add-links-here.html',
            '',
            '`$ commands between backtics and prefixed by dollar sign`',
            '',
            '## Meta',
            '',
            '> category : snippet  ',
            'created  : 2017-10-14T19:56:31.000001+00:00  ',
            'digest   : fdbf285d091a8c46cf491da675ecfeda38f7796ef034124b357f49737963cd19  ',
            'filename :   ',
            'name     :   ',
            'source   :   ',
            'tags     : cli,from,tags  ',
            'updated  : 2017-10-14T19:56:31.000001+00:00  ',
            'uuid     : 11cd5827-b6ef-4067-b5ac-3ceac07dde9f  ',
            'versions : ',
            ''
        )
        edited = (
            '# Brief from cli @groups',
            '',
            '> Add a description that defines the content in one chapter.',
            '',
            '> [1] https://www.example.com/add-links-here.html',
            '',
            '`$ docker rm --volumes $(docker ps --all --quiet)`',
            '',
            '## Meta',
            '',
            '> category : snippet  ',
            'created  : 2017-10-14T19:56:31.000001+00:00  ',
            'digest   : fdbf285d091a8c46cf491da675ecfeda38f7796ef034124b357f49737963cd19  ',
            'filename :   ',
            'name     :   ',
            'source   :   ',
            'tags     : cli,from,tags  ',
            'updated  : 2017-10-14T19:56:31.000001+00:00  ',
            'uuid     : 11cd5827-b6ef-4067-b5ac-3ceac07dde9f  ',
            'versions : ',
            ''
        )
        editor_data.return_value = '\n'.join(edited)
        cause = snippy.run(['snippy', 'create', '-t', 'tags,from,cli', '-b', 'Brief from cli'])
        assert cause == Cause.ALL_OK
        editor_data.assert_called_with('\n'.join(template))
        Content.assert_storage(content)

    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        Content.delete()
