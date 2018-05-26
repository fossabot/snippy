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

"""test_ut_sqlite3db_insert.py: Test inserting content into sqlite."""

import mock

from snippy.cause import Cause
from snippy.config.config import Config
from snippy.storage.database.sqlite3db import Sqlite3Db
from tests.testlib.snippet_helper import SnippetHelper as Snippet
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database


class TestUtSqlite3dbInsert(object):
    """Testing inserting content into sqlite."""

    @mock.patch.object(Cause, 'push')
    @mock.patch.object(Config, 'storage_file', Database.get_storage())
    @mock.patch.object(Config, 'storage_schema', Database.get_schema())
    def test_insert_with_all_parameters(self, mock_cause_push):
        """Insert content into database.

        Insert content into database with all parameters.
        """

        sqlite = Sqlite3Db()
        sqlite.init()

        collection = Snippet.get_collection(snippet=Snippet.REMOVE)
        sqlite.insert(collection)
        mock_cause_push.assert_called_once_with('201 Created', 'content created')
        mock_cause_push.reset_mock()
        assert collection == Database.get_snippets()
        assert Database.get_snippets().size() == 1
        sqlite.disconnect()
        Database.delete_all_contents()
        Database.delete_storage()

    @mock.patch.object(Cause, 'push')
    @mock.patch.object(Config, 'storage_file', Database.get_storage())
    @mock.patch.object(Config, 'storage_schema', Database.get_schema())
    def test_insert_multiple_links(self, mock_cause_push):
        """Insert content with multiple links."""

        sqlite = Sqlite3Db()
        sqlite.init()

        collection = Snippet.get_collection(snippet=Snippet.FORCED)
        sqlite.insert(collection)
        mock_cause_push.assert_called_once_with('201 Created', 'content created')
        mock_cause_push.reset_mock()
        assert collection == Database.get_snippets()
        assert Database.get_snippets().size() == 1
        sqlite.disconnect()
        Database.delete_all_contents()
        Database.delete_storage()

    @classmethod
    def setup_class(cls):
        """Setup the test class."""

        Config.init(None)

    @classmethod
    def teardown_class(cls):
        """Teardown each test."""

        Database.delete_all_contents()
        Database.delete_storage()
