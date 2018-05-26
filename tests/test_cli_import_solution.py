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

"""test_cli_import_solution: Test workflows for importing solutions."""

import json
import pkg_resources

import mock
import pytest
import yaml

from snippy.cause import Cause
from snippy.config.constants import Constants as Const
from tests.testlib.content import Content
from tests.testlib.solution_helper import SolutionHelper as Solution
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database


class TestCliImportSolution(object):  # pylint: disable=too-many-public-methods
    """Test workflows for importing solutions."""

    def test_cli_import_solution_001(self, snippy, yaml_load, mocker):
        """Import all solutions."""

        ## Brief: Import all solutions. File name is not defined in command
        ##        line. This should result tool internal default file name and
        ##        format being used.
        content_read = {
            Solution.BEATS_DIGEST: Solution.DEFAULTS[Solution.BEATS],
            Solution.KAFKA_DIGEST: Solution.DEFAULTS[Solution.KAFKA]
        }
        yaml.safe_load.return_value = Content.imported_dict(content_read)
        cause = snippy.run(['snippy', 'import', '--solution'])
        assert cause == Cause.ALL_OK
        assert len(Database.get_solutions()) == 2
        yaml_load.assert_called_once_with('./solutions.yaml', 'r')
        Content.verified(mocker, snippy, content_read)

    def test_cli_import_solution_002(self, snippy, yaml_load, mocker):
        """Import all solutions."""

        ## Brief: Import all solutions from yaml file. File name and format
        ##        are extracted from command line option -f|--file.
        content_read = {
            Solution.BEATS_DIGEST: Solution.DEFAULTS[Solution.BEATS],
            Solution.KAFKA_DIGEST: Solution.DEFAULTS[Solution.KAFKA]
        }
        yaml.safe_load.return_value = Content.imported_dict(content_read)
        cause = snippy.run(['snippy', 'import', '--solution', '-f', './all-solutions.yaml'])
        assert cause == Cause.ALL_OK
        assert len(Database.get_solutions()) == 2
        yaml_load.assert_called_once_with('./all-solutions.yaml', 'r')
        Content.verified(mocker, snippy, content_read)

    def test_cli_import_solution_003(self, snippy, yaml_load, mocker):
        """Import all solutions."""

        ## Brief: Import all solutions from yaml file without specifying the
        ##        solution category. File name and format are extracted from
        ##        command line option -f|--file.
        content_read = {
            Solution.BEATS_DIGEST: Solution.DEFAULTS[Solution.BEATS],
            Solution.KAFKA_DIGEST: Solution.DEFAULTS[Solution.KAFKA]
        }
        yaml.safe_load.return_value = Content.imported_dict(content_read)
        cause = snippy.run(['snippy', 'import', '-f', './all-solutions.yaml'])
        assert cause == Cause.ALL_OK
        assert len(Database.get_solutions()) == 2
        assert not Database.get_snippets()
        yaml_load.assert_called_once_with('./all-solutions.yaml', 'r')
        Content.verified(mocker, snippy, content_read)

    def test_cli_import_solution_004(self, snippy, json_load, mocker):
        """Import all solutions."""

        ## Brief: Import all solutions from json file. File name and format
        ##        are extracted from command line option -f|--file.
        content_read = {
            Solution.BEATS_DIGEST: Solution.DEFAULTS[Solution.BEATS],
            Solution.KAFKA_DIGEST: Solution.DEFAULTS[Solution.KAFKA]
        }
        json.load.return_value = Content.imported_dict(content_read)
        cause = snippy.run(['snippy', 'import', '--solution', '-f', './all-solutions.json'])
        assert cause == Cause.ALL_OK
        assert len(Database.get_solutions()) == 2
        json_load.assert_called_once_with('./all-solutions.json', 'r')
        Content.verified(mocker, snippy, content_read)

    def test_cli_import_solution_005(self, snippy, json_load, mocker):
        """Import all solutions."""

        ## Brief: Import all solutions from json file without specifying the
        ##        solution category. File name and format are extracted from
        ##        command line option -f|--file.
        content_read = {
            Solution.BEATS_DIGEST: Solution.DEFAULTS[Solution.BEATS],
            Solution.KAFKA_DIGEST: Solution.DEFAULTS[Solution.KAFKA]
        }
        json.load.return_value = Content.imported_dict(content_read)
        cause = snippy.run(['snippy', 'import', '-f', './all-solutions.json'])
        assert cause == Cause.ALL_OK
        assert len(Database.get_solutions()) == 2
        assert not Database.get_snippets()
        json_load.assert_called_once_with('./all-solutions.json', 'r')
        Content.verified(mocker, snippy, content_read)

    def test_cli_import_solution_006(self, snippy, mocker):
        """Import all solutions."""

        ## Brief: Import all solutions from txt file. File name and format are
        ##        extracted from command line option -f|--file. File extension
        ##        is '*.txt' in this case.
        content_read = {
            Solution.BEATS_DIGEST: Solution.DEFAULTS[Solution.BEATS],
            Solution.KAFKA_DIGEST: Solution.DEFAULTS[Solution.KAFKA]
        }
        mocked_open = Content.mocked_open(content_read)
        with mock.patch('snippy.migrate.migrate.open', mocked_open, create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '--solution', '-f', './all-solutions.txt'])
            assert cause == Cause.ALL_OK
            assert len(Database.get_solutions()) == 2
            mock_file.assert_called_once_with('./all-solutions.txt', 'r')
            Content.verified(mocker, snippy, content_read)

    def test_cli_import_solution_007(self, snippy, mocker):
        """Import all solutions."""

        ## Brief: Import all solutions from txt file without specifying the
        ##        solution category. File name and format are extracted from
        ##        command line option -f|--file. File extension is '*.txt'
        ##        in this case.
        content_read = {
            Solution.BEATS_DIGEST: Solution.DEFAULTS[Solution.BEATS],
            Solution.KAFKA_DIGEST: Solution.DEFAULTS[Solution.KAFKA]
        }
        mocked_open = Content.mocked_open(content_read)
        with mock.patch('snippy.migrate.migrate.open', mocked_open, create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '-f', './all-solutions.txt'])
            assert cause == Cause.ALL_OK
            assert len(Database.get_solutions()) == 2
            mock_file.assert_called_once_with('./all-solutions.txt', 'r')
            Content.verified(mocker, snippy, content_read)

    def test_cli_import_solution_008(self, snippy, mocker):
        """Import all solutions."""

        ## Brief: Import all solutions from txt file. File name and format are
        ##        extracted from command line option -f|--file. File extension
        ##        is '*.text' in this case.
        content_read = {
            Solution.BEATS_DIGEST: Solution.DEFAULTS[Solution.BEATS],
            Solution.KAFKA_DIGEST: Solution.DEFAULTS[Solution.KAFKA]
        }
        mocked_open = Content.mocked_open(content_read)
        with mock.patch('snippy.migrate.migrate.open', mocked_open, create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '--solution', '-f', './all-solutions.text'])
            assert cause == Cause.ALL_OK
            assert len(Database.get_solutions()) == 2
            mock_file.assert_called_once_with('./all-solutions.text', 'r')
            Content.verified(mocker, snippy, content_read)

    def test_cli_import_solution_009(self, snippy, mocker):
        """Import all solutions."""

        ## Brief: Import all solutions from txt file without specifying the
        ##        solution category. File name and format are extracted from
        ##        command line option -f|--file. File extension is '*.text'
        ##        in this case.
        content_read = {
            Solution.BEATS_DIGEST: Solution.DEFAULTS[Solution.BEATS],
            Solution.KAFKA_DIGEST: Solution.DEFAULTS[Solution.KAFKA]
        }
        mocked_open = Content.mocked_open(content_read)
        with mock.patch('snippy.migrate.migrate.open', mocked_open, create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '-f', './all-solutions.text'])
            assert cause == Cause.ALL_OK
            assert len(Database.get_solutions()) == 2
            mock_file.assert_called_once_with('./all-solutions.text', 'r')
            Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('import-beats', 'import-beats-utc', 'import-kafka-utc')
    def test_cli_import_solution_010(self, snippy, yaml_load, mocker):
        """Import all solutions."""

        ## Brief: Import solutions from yaml file when all but one of the
        ##        solutions in the file is already stored. Because one
        ##        solution was stored successfully, the return cause is OK.
        content_read = {
            Solution.BEATS_DIGEST: Solution.DEFAULTS[Solution.BEATS],
            Solution.KAFKA_DIGEST: Solution.DEFAULTS[Solution.KAFKA]
        }
        yaml.safe_load.return_value = Content.imported_dict(content_read)
        assert len(Database.get_solutions()) == 1
        cause = snippy.run(['snippy', 'import', '--solution', '--file', './all-solutions.yaml'])
        assert cause == Cause.ALL_OK
        assert len(Database.get_solutions()) == 2
        yaml_load.assert_called_once_with('./all-solutions.yaml', 'r')
        Content.verified(mocker, snippy, content_read)

    def test_cli_import_solution_011(self, snippy):
        """Import all solutions."""

        ## Brief: Try to import empty solution template. The operation will
        ##        fail because content templates without any modifications
        ##        cannot be imported.
        mocked_open = mock.mock_open(read_data=Const.NEWLINE.join(Solution.TEMPLATE))
        with mock.patch('snippy.migrate.migrate.open', mocked_open, create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '--solution', '-f', './solution-template.txt'])
            assert cause == 'NOK: content was not stored because it was matching to an empty template'
            assert not Database.get_contents()
            mock_file.assert_called_once_with('./solution-template.txt', 'r')

    def test_cli_import_solution_012(self, snippy):
        """Import all solutions."""

        ## Brief: Try to import solution from file which file format is not
        ##        supported. This should result error text for end user and
        ##        no files should be read.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '--solution', '-f', './foo.bar'])
            assert cause == 'NOK: cannot identify file format for file ./foo.bar'
            assert not Database.get_contents()
            mock_file.assert_not_called()

    @pytest.mark.usefixtures('import-nginx', 'import-nginx-utc')
    def test_cli_import_solution_013(self, snippy, yaml_load, mocker):
        """Import solution based on message digest."""

        ## Brief: Import defined solution based on message digest. File name
        ##        is defined from command line as yaml file which contain one
        ##        solution. One line in the solution data was updated.
        content_read = Content.updated_nginx()
        yaml.safe_load.return_value = Content.imported_dict(content_read)
        cause = snippy.run(['snippy', 'import', '--solution', '-d', '61a24a156f5e9d2d', '-f', 'one-solution.yaml'])
        assert cause == Cause.ALL_OK
        assert len(Database.get_solutions()) == 1
        yaml_load.assert_called_once_with('one-solution.yaml', 'r')
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('import-nginx', 'import-nginx-utc')
    def test_cli_import_solution_014(self, snippy, yaml_load, mocker):
        """Import solution based on message digest."""

        ## Brief: Import defined solution based on message digest without
        ##        specifying the content category explicitly. One line in
        ##        the solution data was updated.
        content_read = Content.updated_nginx()
        yaml.safe_load.return_value = Content.imported_dict(content_read)
        cause = snippy.run(['snippy', 'import', '-d', '61a24a156f5e9d2d', '-f', 'one-solution.yaml'])
        assert cause == Cause.ALL_OK
        assert len(Database.get_solutions()) == 1
        assert not Database.get_snippets()
        yaml_load.assert_called_once_with('one-solution.yaml', 'r')
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('import-nginx', 'import-nginx-utc')
    def test_cli_import_solution_015(self, snippy, json_load, mocker):
        """Import solution based on message digest."""

        ## Brief: Import defined solution based on message digest. File name
        ##        is defined from command line as json file which contain one
        ##        solution. One line in the content data was updated.
        content_read = Content.updated_nginx()
        json.load.return_value = Content.imported_dict(content_read)
        cause = snippy.run(['snippy', 'import', '--solution', '-d', '61a24a156f5e9d2d', '-f', 'one-solution.json'])
        assert cause == Cause.ALL_OK
        assert len(Database.get_solutions()) == 1
        json_load.assert_called_once_with('one-solution.json', 'r')
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('import-nginx', 'import-nginx-utc')
    def test_cli_import_solution_016(self, snippy, mocker):
        """Import solution based on message digest."""

        ## Brief: Import defined solution based on message digest. File name
        ##        is defined from command line as text file which contain one
        ##        solution. One line in the content data was updated. The file
        ##        extension is '*.txt' in this case.
        content_read = Content.updated_nginx()
        mocked_open = Content.mocked_open(content_read)
        with mock.patch('snippy.migrate.migrate.open', mocked_open, create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '--solution', '-d', '61a24a156f5e9d2d', '-f', 'one-solution.txt'])
            assert cause == Cause.ALL_OK
            assert len(Database.get_solutions()) == 1
            mock_file.assert_called_once_with('one-solution.txt', 'r')
            Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('import-nginx', 'import-nginx-utc')
    def test_cli_import_solution_017(self, snippy, mocker):
        """Import solution based on message digest."""

        ## Brief: Import defined solution based on message digest. File name
        ##        is defined from command line as text file which contain one
        ##        solution. One line in the content data was updated. The file
        ##        extension is '*.text' in this case.
        content_read = Content.updated_nginx()
        mocked_open = Content.mocked_open(content_read)
        with mock.patch('snippy.migrate.migrate.open', mocked_open, create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '--solution', '-d', '61a24a156f5e9d2d', '-f', 'one-solution.text'])
            assert cause == Cause.ALL_OK
            assert len(Database.get_solutions()) == 1
            mock_file.assert_called_once_with('one-solution.text', 'r')
            Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('import-nginx', 'import-nginx-utc')
    def test_cli_import_solution_018(self, snippy, mocker):
        """Import solution based on message digest."""

        ## Brief: Import defined solution based on message digest. In this
        ##        case the content category is accidentally specified as
        ##        'snippet'. This should still import the content in solution.
        ##        category
        content_read = Content.updated_nginx()
        mocked_open = Content.mocked_open(content_read)
        with mock.patch('snippy.migrate.migrate.open', mocked_open, create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '--snippet', '-d', '61a24a156f5e9d2d', '-f', 'one-solution.text'])
            assert cause == Cause.ALL_OK
            assert len(Database.get_solutions()) == 1
            assert not Database.get_snippets()
            mock_file.assert_called_once_with('one-solution.text', 'r')
            Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('import-nginx', 'import-nginx-utc')
    def test_cli_import_solution_019(self, snippy, mocker):
        """Import solution based on message digest."""

        ## Brief: Try to import defined solution with message digest that
        ##        cannot be found. In this case there is one solution stored.
        content_read = Content.updated_nginx()
        mocked_open = Content.mocked_open(content_read)
        with mock.patch('snippy.migrate.migrate.open', mocked_open, create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '--solution', '-d', '123456789abcdef0', '-f', 'one-solution.text'])
            assert cause == 'NOK: cannot find solution identified with digest 123456789abcdef0'
            assert len(Database.get_solutions()) == 1
            assert not Database.get_snippets()
            mock_file.assert_not_called()
            Content.verified(mocker, snippy, {Solution.NGINX_DIGEST: Solution.DEFAULTS[Solution.NGINX]})

    def test_cli_import_solution_020(self, snippy, yaml_load, mocker):
        """Import solution."""

        ## Brief: Import new solution from yaml file.
        content_read = {
            Solution.NGINX_DIGEST: Solution.DEFAULTS[Solution.NGINX]
        }
        yaml.safe_load.return_value = Content.imported_dict(content_read)
        cause = snippy.run(['snippy', 'import', '--solution', '-f', 'one-solution.yaml'])
        assert cause == Cause.ALL_OK
        assert len(Database.get_solutions()) == 1
        yaml_load.assert_called_once_with('one-solution.yaml', 'r')
        Content.verified(mocker, snippy, content_read)

    def test_cli_import_solution_021(self, snippy, json_load, mocker):
        """Import solution."""

        ## Brief: Import new solution from json file.
        content_read = {
            Solution.NGINX_DIGEST: Solution.DEFAULTS[Solution.NGINX]
        }
        json.load.return_value = Content.imported_dict(content_read)
        cause = snippy.run(['snippy', 'import', '--solution', '-f', 'one-solution.json'])
        assert cause == Cause.ALL_OK
        assert len(Database.get_solutions()) == 1
        json_load.assert_called_once_with('one-solution.json', 'r')
        Content.verified(mocker, snippy, content_read)

    def test_cli_import_solution_022(self, snippy, mocker):
        """Import solution."""

        ## Brief: Import new solution from text file. In this case the file
        ##        extension is '*.txt'.
        content_read = {
            Solution.NGINX_DIGEST: Solution.DEFAULTS[Solution.NGINX]
        }
        mocked_open = Content.mocked_open(content_read)
        with mock.patch('snippy.migrate.migrate.open', mocked_open, create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '--solution', '-f', 'one-solution.txt'])
            assert cause == Cause.ALL_OK
            assert len(Database.get_solutions()) == 1
            mock_file.assert_called_once_with('one-solution.txt', 'r')
            Content.verified(mocker, snippy, content_read)

    def test_cli_import_solution_023(self, snippy, mocker):
        """Import solution."""

        ## Brief: Import new solution from text file without specifying the
        ##        content category explicitly. In this case the file extension
        ##        is '*.txt'.
        content_read = {
            Solution.NGINX_DIGEST: Solution.DEFAULTS[Solution.NGINX]
        }
        mocked_open = Content.mocked_open(content_read)
        with mock.patch('snippy.migrate.migrate.open', mocked_open, create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '-f', 'one-solution.txt'])
            assert cause == Cause.ALL_OK
            assert len(Database.get_solutions()) == 1
            assert not Database.get_snippets()
            mock_file.assert_called_once_with('one-solution.txt', 'r')
            Content.verified(mocker, snippy, content_read)

    def test_cli_import_solution_024(self, snippy, mocker):
        """Import solution."""

        ## Brief: Import new solution from text file. In this case the file
        ##        extension is '*.text'.
        content_read = {
            Solution.NGINX_DIGEST: Solution.DEFAULTS[Solution.NGINX]
        }
        mocked_open = Content.mocked_open(content_read)
        with mock.patch('snippy.migrate.migrate.open', mocked_open, create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '--solution', '-f', 'one-solution.text'])
            assert cause == Cause.ALL_OK
            assert len(Database.get_solutions()) == 1
            mock_file.assert_called_once_with('one-solution.text', 'r')
            Content.verified(mocker, snippy, content_read)

    def test_cli_import_solution_025(self, snippy, yaml_load, mocker):
        """Import solutions defaults."""

        ## Brief: Import solution defaults. All solutions should be imported
        ##        from predefined file location under tool data folder from
        ##        yaml format.
        content_read = {
            Solution.BEATS_DIGEST: Solution.DEFAULTS[Solution.BEATS],
            Solution.NGINX_DIGEST: Solution.DEFAULTS[Solution.NGINX]
        }
        yaml.safe_load.return_value = Content.imported_dict(content_read)
        cause = snippy.run(['snippy', 'import', '--solution', '--defaults'])
        assert cause == Cause.ALL_OK
        assert len(Database.get_solutions()) == 2
        defaults_solutions = pkg_resources.resource_filename('snippy', 'data/default/solutions.yaml')
        yaml_load.assert_called_once_with(defaults_solutions, 'r')
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('default-solutions', 'import-beats-utc', 'import-nginx-utc')
    def test_cli_import_solution_026(self, snippy, yaml_load, mocker):
        """Import solutions defaults."""

        ## Brief: Try to import solution defaults again. The second import
        ##        should fail with an error because the content already exist.
        ##        The error text must be the same for all content categories.
        ##        Because of random order dictionary in the code, the reported
        ##        digest can vary if there are multiple failures.
        content_read = {
            Solution.BEATS_DIGEST: Solution.DEFAULTS[Solution.BEATS],
            Solution.NGINX_DIGEST: Solution.DEFAULTS[Solution.NGINX]
        }
        yaml.safe_load.return_value = Content.imported_dict(content_read)
        cause = snippy.run(['snippy', 'import', '--solution', '--defaults'])
        assert cause == 'NOK: content data already exist with digest 61a24a156f5e9d2d' or \
               cause == 'NOK: content data already exist with digest a96accc25dd23ac0'
        assert len(Database.get_solutions()) == 2
        defaults_solutions = pkg_resources.resource_filename('snippy', 'data/default/solutions.yaml')
        yaml_load.assert_called_once_with(defaults_solutions, 'r')
        Content.verified(mocker, snippy, content_read)

    def test_cli_import_solution_027(self, snippy, mocker):
        """Import solutions from text template.
        
        Import solution template that does not have any changes to file header
        located at the top of content data. This tests a scenario where user
        does not bother to do any changes to header which has the solution
        metadata. Because the content was changed the import operation must
        work.
        """

        template = Const.NEWLINE.join(Solution.TEMPLATE)
        template = template.replace('## description', '## description changed')
        content_read = {
            '2375b011459a4c17': Solution.get_dictionary(template)
        }
        mocked_open = mock.mock_open(read_data=template)
        with mock.patch('snippy.migrate.migrate.open', mocked_open, create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '-f', './solution-template.txt'])
            assert cause == Cause.ALL_OK
            assert len(Database.get_solutions()) == 1
            assert not Database.get_snippets()
            mock_file.assert_called_once_with('./solution-template.txt', 'r')
            Content.verified(mocker, snippy, content_read)

    def test_cli_import_solution_028(self, snippy):
        """Import solutions from text template.
        
        Try to import solution template without any changes. This should result
        error text for end user and no files should be read. The error text must
        be the same for all content types.
        """

        template = Const.NEWLINE.join(Solution.TEMPLATE)
        mocked_open = mock.mock_open(read_data=template)
        with mock.patch('snippy.migrate.migrate.open', mocked_open, create=True) as mock_file:
            cause = snippy.run(['snippy', 'import', '--solution', '--template'])
            assert cause == 'NOK: content was not stored because it was matching to an empty template'
            assert not Database.get_contents()
            mock_file.assert_called_once_with('./solution-template.txt', 'r')

    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        Database.delete_all_contents()
        Database.delete_storage()
