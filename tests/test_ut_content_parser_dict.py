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

"""test_ut_content_parser_parser_dict: Test ContentParserDict() class."""

from snippy.constants import Constants as Const
from snippy.content.collection import Collection
from snippy.content.parsers.dict import ContentParserDict as Parser


class TestUtContentParserDict(object):
    """Test ContentParserDict() class."""

    TIMESTAMP = '2018-09-09T14:44:00.000001+0000'

    def test_parser_snippet_001(self):
        """Test parsing snippet.

        Test case verifies that standard snippet is parsed correctly from
        dictionary. In this case the input is given in list context for
        data and links. For the groups and tags the input is give as a
        string. All of these cases must result tuple.

        The string fields contain errors like additional spaces that must
        be trimmed.
        """

        dictionary = {'data': [{
            'data': ['docker rm $(docker ps --all -q -f status=exited)'],
            'brief': ' strip spaces   ',
            'description': ' strip spaces   ',
            'groups': 'default',
            'tags': 'tag2,tag1',
            'links': [],
            'category': 'snippet',
            'name': '',
            'filename': '',
            'versions': '',
            'source': '',
            'uuid': '11cd5827-b6ef-4067-b5ac-3ceac07dde9f',
            'created': '2015-10-14T19:56:31.000001+0000',
            'updated': '2016-10-14T19:56:31.000001+0000',
            'digest': '3d855210284302d58cf383ea25d8abdea2f7c61c4e2198da01e2c0896b0268dd'
        }]}
        collection = Collection()
        Parser(self.TIMESTAMP, dictionary, collection).read_collection()
        resource = next(collection.resources())
        assert resource.category == Const.SNIPPET
        assert resource.data == ('docker rm $(docker ps --all -q -f status=exited)',)
        assert resource.brief == 'strip spaces'
        assert resource.description == 'strip spaces'
        assert resource.groups == ('default',)
        assert resource.tags == ('tag1', 'tag2')
        assert resource.links == ()
        assert resource.filename == ''
        assert resource.name == ''
        assert resource.versions == ''
        assert resource.source == ''
        assert resource.uuid == '11cd5827-b6ef-4067-b5ac-3ceac07dde9f'
        assert resource.created == '2015-10-14T19:56:31.000001+0000'
        assert resource.updated == '2016-10-14T19:56:31.000001+0000'
        assert resource.digest == '76257166ef4499ffbbf4036accd161184e9b91f326b0b6f3d5e7a1333b516713'

    def test_parser_snippet_002(self):
        """Test parsing unknown content.

        In this case the content category is incorrect.
        """

        dictionary = {'data': [{
            'data': ['ls -al .'],
            'brief': ' strip spaces   ',
            'description': ' strip spaces   ',
            'groups': 'default',
            'tags': 'tag2,tag1',
            'links': [],
            'category': 'failure',
            'name': '',
            'filename': '',
            'versions': '',
            'source': '',
            'uuid': '11cd5827-b6ef-4067-b5ac-3ceac07dde9f',
            'created': '2015-10-14T19:56:31.000001+0000',
            'updated': '2016-10-14T19:56:31.000001+0000',
            'digest': '3d855210284302d58cf383ea25d8abdea2f7c61c4e2198da01e2c0896b0268dd'
        }]}
        collection = Collection()
        Parser(self.TIMESTAMP, dictionary, collection).read_collection()
        assert not collection

    def test_parser_snippet_003(self):
        """Test incorrect dictionary structure.

        In this case the dictionay does not contain mandatory data key.
        """

        dictionary = {'failure': [{
            'data': ['ls -al .'],
            'brief': ' strip spaces   ',
            'description': ' strip spaces   ',
            'groups': 'default',
            'tags': 'tag2,tag1',
            'links': [],
            'category': 'failure',
            'name': '',
            'filename': '',
            'versions': '',
            'source': '',
            'uuid': '11cd5827-b6ef-4067-b5ac-3ceac07dde9f',
            'created': '2015-10-14T19:56:31.000001+0000',
            'updated': '2016-10-14T19:56:31.000001+0000',
            'digest': '3d855210284302d58cf383ea25d8abdea2f7c61c4e2198da01e2c0896b0268dd'
        }]}
        collection = Collection()
        Parser(self.TIMESTAMP, dictionary, collection).read_collection()
        assert not collection