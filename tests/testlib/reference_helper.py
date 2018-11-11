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

"""reference_helper: Helper methods for reference testing."""

from snippy.config.config import Config
from snippy.config.source.parser import Parser
from snippy.constants import Constants as Const
from snippy.content.collection import Collection
from tests.testlib.helper import Helper


class ReferenceHelper(object):
    """Helper methods for reference testing."""

    GITLOG = 0
    REGEXP = 1
    PYTEST = 2

    # Default content must be always set so that it reflects content stored
    # into a database. For example the tags must be sorted correct here. This
    # forces creating special error cases in each test case and enforces more
    # controlled failure testing.
    GITLOG_DIGEST = '5c2071094dbfaa33'
    REGEXP_DIGEST = 'cb9225a81eab8ced'
    PYTEST_DIGEST = '1f9d9496005736ef'
    DEFAULTS = ({
        'data': ('', ),
        'brief': 'How to write commit messages',
        'description': '',
        'groups': ('git',),
        'tags': ('commit', 'git', 'howto'),
        'links': ('https://chris.beams.io/posts/git-commit/', ),
        'category': 'reference',
        'name': '',
        'filename': '',
        'versions': '',
        'source': '',
        'uuid': '31cd5827-b6ef-4067-b5ac-3ceac07dde9f',
        'created': '2018-06-22T13:11:13.678729+0000',
        'updated': '2018-06-22T13:11:13.678729+0000',
        'digest': '5c2071094dbfaa33787064a6669e1fdfe49a86d07e58f12fffa0780eecdb227f'
    }, {
        'data': ('', ),
        'brief': 'Python regular expression',
        'description': '',
        'groups': ('python',),
        'tags': (' python ', ' regexp  ', '  online   ', 'howto'),
        'links': ('https://www.cheatography.com/davechild/cheat-sheets/regular-expressions/',
                  'https://pythex.org/'),
        'category': 'reference',
        'name': '',
        'filename': '',
        'versions': '',
        'source': '',
        'uuid': '32cd5827-b6ef-4067-b5ac-3ceac07dde9f',
        'created': '2018-05-21T13:11:13.678729+0000',
        'updated': '2018-05-21T13:11:13.678729+0000',
        'digest': 'cb9225a81eab8ced090649f795001509b85161246b46de7d12ab207698373832'
    }, {
        'data': ('', ),
        'brief': 'Python pytest framework',
        'description': '',
        'groups': ('python',),
        'tags': ('python', 'pytest', 'docs'),
        'links': ('https://docs.pytest.org/en/latest/skipping.html', ),
        'category': 'reference',
        'name': '',
        'filename': '',
        'versions': '',
        'source': '',
        'uuid': '33cd5827-b6ef-4067-b5ac-3ceac07dde9f',
        'created': '2016-04-21T12:10:11.678729+0000',
        'updated': '2016-04-21T12:10:11.678729+0000',
        'digest': '1f9d9496005736efe321d44a28c05ca9ed0e53f7170743df361ddcd7b884455e'
    })

    TEMPLATE = Helper.read_template('reference.txt').split(Const.NEWLINE)

    @staticmethod
    def get_dictionary(template):
        """Transform template to dictinary."""

        collection = ReferenceHelper._get_content(template)
        resource = next(collection.resources())

        return resource.dump_dict(Config.remove_fields)

    @staticmethod
    def dump(content, content_format):
        """Dump content in requested format.

        Args:
            content (dict): Content in dictionary.
            content_format (str): Content format.

        Returns:
            str: Content in requested format.
        """

        dump = Const.EMPTY
        resource = Collection.get_resource(content['category'], '2018-10-20T06:16:27.000001+0000')
        resource.load_dict(content)
        if content_format == Const.CONTENT_FORMAT_TEXT:
            dump = resource.dump_text(Config.templates)
        elif content_format == Const.CONTENT_FORMAT_MKDN:
            dump = resource.dump_mkdn(Config.templates)

        return dump

    @staticmethod
    def _get_content(text):
        """Transform text template to content."""

        collection = Parser(Const.CONTENT_FORMAT_TEXT, Config.utcnow(), text).read()

        return collection
