#!/usr/bin/env python3

"""test_wf_import_solution.py: Test workflows for importing solutions."""

import sys
import unittest
import mock
import yaml
from snippy.config.constants import Constants as Const
from snippy.cause.cause import Cause
from snippy.storage.database.sqlite3db import Sqlite3Db
from tests.testlib.snippet_helper import SnippetHelper as Snippet
from tests.testlib.solution_helper import SolutionHelper as Solution
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database


class TestWfImportSolution(unittest.TestCase):
    """Test workflows for importing solutions."""

    @mock.patch.object(yaml, 'safe_load')
    @mock.patch.object(Sqlite3Db, '_get_db_location')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    def test_import_all_solutions(self, mock_isfile, mock_get_db_location, mock_yaml_load):
        """Import all solutions."""

        mock_get_db_location.return_value = Database.get_storage()
        mock_isfile.return_value = True
        import_dict = {'content': [{'data': tuple(Solution.SOLUTIONS_TEXT[0]),
                                    'brief': 'Debugging Elastic Beats',
                                    'group': 'beats',
                                    'tags': ('Elastic', 'beats', 'debug', 'filebeat', 'howto'),
                                    'links': ('https://www.elastic.co/guide/en/beats/filebeat/master/enable-filebeat-debugging.html',),
                                    'category': 'solution',
                                    'filename': 'howto-debug-elastic-beats.txt',
                                    'utc': None,
                                    'digest': 'a96accc25dd23ac0554032e25d773f3931d70b1d986664b13059e5e803df6da8'},
                                   {'data': tuple(Solution.SOLUTIONS_TEXT[2]),
                                    'brief': 'Testing docker log driver',
                                    'group': 'docker',
                                    'tags': ('docker', 'driver', 'kafka', 'kubernetes', 'logging', 'logs2kafka', 'moby', 'plugin'),
                                    'links': ('https://github.com/MickayG/moby-kafka-logdriver',
                                              'https://github.com/garo/logs2kafka',
                                              'https://groups.google.com/forum/#!topic/kubernetes-users/iLDsG85exRQ'),
                                    'category': 'solution',
                                    'filename': 'kubernetes-docker-log-driver-kafka.txt',
                                    'utc': '2017-10-12 11:53:17',
                                    'digest': '50249fd7264a8af3580aa684ad98b64180ca8c58b2217af91d1c4569e80c7046'}]}
        mock_yaml_load.return_value = import_dict
        snippy = Snippet.add_snippets(self)

        ## Brief: Import all solutions. File name is not defined in commmand line. This should
        ##        result tool internal default file name ./solutions.yaml being used by default.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            sys.argv = ['snippy', 'import', '--solution']  ## workflow
            snippy.reset()
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            assert len(Database.get_contents()) == 4
            mock_file.assert_called_once_with('./solutions.yaml', 'r')

            # Verify one of the imported solution by exporting it again to text file.
            mock_file.reset_mock()
            sys.argv = ['snippy', 'export', '-d', '50249fd7264a8af3', '-f', 'defined-solution.txt']
            snippy.reset()
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('defined-solution.txt', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_has_calls([mock.call(Const.NEWLINE.join(Solution.SOLUTIONS_TEXT[2])),
                                                mock.call(Const.NEWLINE)])

        ## Brief: Import all solutions from yaml file. File name or format defined from command
        ##        line option -f|--file.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            Database.delete_solutions()
            sys.argv = ['snippy', 'import', '-f', './solutions.yaml']  ## workflow
            snippy.reset()
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('./solutions.yaml', 'r')
            assert len(Database.get_contents()) == 4

            # Verify one of the imported solution by exporting it again to text file.
            mock_file.reset_mock()
            sys.argv = ['snippy', 'export', '-d', '50249fd7264a8af3', '-f', 'defined-solution.txt']
            snippy.reset()
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('defined-solution.txt', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_has_calls([mock.call(Const.NEWLINE.join(Solution.SOLUTIONS_TEXT[2])),
                                                mock.call(Const.NEWLINE)])

        # Release all resources
        snippy.release()

    @mock.patch.object(Sqlite3Db, '_get_db_location')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    def test_import_empty_solution_template(self, mock_isfile, mock_get_db_location):
        """Import solution from template.

        Expected results:
            1 Solution template that is not changed at all cannot be imported.
            2 Exit cause is NOK.
        """

        mock_get_db_location.return_value = Database.get_storage()
        mock_isfile.return_value = True

        ## Brief: Try to import empty solution template. The operation will fail because
        ##        content templates without any modifications cannot be imported.
        mocked_open = mock.mock_open(read_data=Const.NEWLINE.join(Solution.TEMPLATE))
        with mock.patch('snippy.migrate.migrate.open', mocked_open, create=True) as mock_file:
            from snippy.snip import Snippy

            sys.argv = ['snippy', 'import', '-f', './solution-template.txt']  ## workflow
            snippy = Snippy()
            cause = snippy.run_cli()
            assert cause == 'NOK: content data is not valid - content template cannot be inserted'
            snippy.storage.search(Const.SOLUTION, digest='7d989ed7aca34708')
            mock_file.assert_called_once_with('./solution-template.txt', 'r')
            assert not Database.get_contents()

        # Release all resources
        snippy.release()

    @mock.patch.object(Sqlite3Db, '_get_db_location')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    def test_import_solution_template(self, mock_isfile, mock_get_db_location):
        """Import solution from template.

        Expected results:
            1 Template is imported even though the header part is not changed.
            2 Exit cause is OK.
        """

        mock_get_db_location.return_value = Database.get_storage()
        mock_isfile.return_value = True

        ## Brief: Import solution template that does not have any changes to file header.
        template = Const.NEWLINE.join(Solution.TEMPLATE)
        template = template.replace('## description', '## description changed')
        mocked_open = mock.mock_open(read_data=template)
        with mock.patch('snippy.migrate.migrate.open', mocked_open, create=True) as mock_file:
            from snippy.snip import Snippy
            from snippy.content.content import Content

            content = Content((tuple(template.split(Const.NEWLINE)),
                               Const.EMPTY,
                               'default',
                               (Const.EMPTY,),
                               (Const.EMPTY,),
                               Const.SOLUTION,
                               Const.EMPTY,
                               None,
                               '63f2007703d70c8f211c1eed7b0b388977e02f7861f208494066e53c7311b5b7',
                               None,
                               1))
            sys.argv = ['snippy', 'import', '-f', './solution-template.txt']  ## workflow
            snippy = Snippy()
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            snippy.storage.search(Const.SOLUTION, digest='63f2007703d70c8f')
            mock_file.assert_called_once_with('./solution-template.txt', 'r')
            assert len(Database.get_contents()) == 1
            Snippet().compare(self, snippy.storage.search(Const.SOLUTION, digest='63f2007703d70c8f')[0], content)

            # Verify the imported solution by exporting it again to text file.
            mock_file.reset_mock()
            sys.argv = ['snippy', 'export', '-d', '63f2007703d70c8f', '-f', 'defined-solution.txt']
            snippy.reset()
            cause = snippy.run_cli()
            assert cause == Cause.ALL_OK
            mock_file.assert_called_once_with('defined-solution.txt', 'w')
            file_handle = mock_file.return_value.__enter__.return_value
            file_handle.write.assert_has_calls([mock.call(template),
                                                mock.call(Const.NEWLINE)])

        # Release all resources
        snippy.release()

    # pylint: disable=duplicate-code
    def tearDown(self):
        """Teardown each test."""

        Database.delete_all_contents()
        Database.delete_storage()
