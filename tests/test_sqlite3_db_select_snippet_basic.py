#!/usr/bin/env python3

"""test_sqlite3_db_select_snippet_basic.py: Test selecting snippets from the sqlite3 database."""

import unittest
import mock
from snippy.config import Config
from snippy.storage.database import Sqlite3Db
from tests.testlib.constant_helper import * # pylint: disable=wildcard-import,unused-wildcard-import
from tests.testlib.snippet_helper import SnippetHelper as Snippet
from tests.testlib.sqlite3_db_helper import Sqlite3DbHelper as Database


class TestSqlite3DbSelectSnippetBasic(unittest.TestCase):
    """Testing selecting of snippets from database with basic tests."""

    @mock.patch.object(Config, 'is_search_all')
    def test_select_keyword_matching_links_column(self, mock_is_search_all):
        """Test that snippet can be selected with regexp keywords. In this
        case only the last keyword matches to links column."""

        mock_is_search_all.return_value = True

        references = Snippet().get_references(1)
        keywords = ['foo', 'bar', 'digitalocean']
        self.sqlite.insert_content('snippets', references[0][CONTENT:TESTING], references[0][DIGEST], references[0][METADATA])
        Snippet().compare_db(self, (self.sqlite.select_content('snippets', keywords))[0], references[0])
        assert len(self.sqlite.select_content('snippets', keywords)) == 1
        self.sqlite.disconnect()

    # pylint: disable=duplicate-code
    @mock.patch.object(Sqlite3Db, '_get_db_location')
    @mock.patch.object(Config, 'get_storage_schema')
    def setUp(self, mock_get_storage_schema, mock__get_db_location): # pylint: disable=arguments-differ
        """Setup each test."""

        mock_get_storage_schema.return_value = Database.get_schema()
        mock__get_db_location.return_value = Database.get_storage()

        self.sqlite = Sqlite3Db().init()

    def tearDown(self):
        """Teardown each test."""

        Database.delete_all_snippets()
        self.sqlite.disconnect()
        Database.delete_storage()
