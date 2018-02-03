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

"""test_wf_create_solution.py: Test workflows for creating solutions."""

import mock

from snippy.cause.cause import Cause
from snippy.config.config import Config
from snippy.config.constants import Constants as Const
from snippy.config.source.editor import Editor
from snippy.snip import Snippy
from tests.testlib.solution_helper import SolutionHelper as Solution
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database


class TestWfCreateSolution(object):
    """Test workflows for creating solutions."""

    @mock.patch.object(Editor, 'call_editor')
    @mock.patch.object(Config, '_storage_file')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    def test_create_solution_from_console(self, mock_isfile, mock_storage_file, mock_call_editor):
        """Create solution from console."""

        mock_isfile.return_value = True
        mock_storage_file.return_value = Database.get_storage()

        ## Brief: Create new solution by defining all content parameters from command line.
        ##        Creating solution from command line will always use editor to create the
        ##        content.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Snippy()
            template = Solution.get_template(Solution.DEFAULTS[Solution.BEATS])
            mock_call_editor.return_value = template
            data = Const.NEWLINE.join(Solution.DEFAULTS[Solution.BEATS]['data'])
            brief = Solution.DEFAULTS[Solution.BEATS]['brief']
            group = Solution.DEFAULTS[Solution.BEATS]['group']
            tags = Const.DELIMITER_TAGS.join(Solution.DEFAULTS[Solution.BEATS]['tags'])
            links = Const.DELIMITER_LINKS.join(Solution.DEFAULTS[Solution.BEATS]['links'])
            compare_content = {'a96accc25dd23ac0': Solution.DEFAULTS[Solution.BEATS]}
            cause = snippy.run_cli(['snippy', 'create', '--solution', '--content', data, '--brief', brief, '--group', group, '--tags', tags, '--links', links])  ## workflow # pylint: disable=line-too-long
            assert cause == Cause.ALL_OK
            assert len(Database.get_solutions()) == 1
            Solution.test_content(snippy, mock_file, compare_content)
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Try to create same solution again with exactly the same content data.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Solution.add_defaults()
            template = Solution.get_template(Solution.DEFAULTS[Solution.BEATS])
            mock_call_editor.return_value = template
            compare_content = {'a96accc25dd23ac0': Solution.DEFAULTS[Solution.BEATS],
                               '61a24a156f5e9d2d': Solution.DEFAULTS[Solution.NGINX]}
            cause = snippy.run_cli(['snippy', 'create', '--solution'])  ## workflow
            assert cause == 'NOK: content data already exist with digest a96accc25dd23ac0'
            assert len(Database.get_solutions()) == 2
            Solution.test_content(snippy, mock_file, compare_content)
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Try to create new solution without any changes to template.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            template = Const.NEWLINE.join(Solution.TEMPLATE)
            mock_call_editor.return_value = template
            compare_content = {'a96accc25dd23ac0': Solution.DEFAULTS[Solution.BEATS]}
            snippy = Snippy()
            cause = snippy.run_cli(['snippy', 'create', '--solution'])  ## workflow
            assert cause == 'NOK: no content was stored because solution is an empty template'
            assert not Database.get_solutions()
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Try to create new solution with empty data. In this case the whole template
        ##        is deleted and the edited solution is an empty string.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            mock_call_editor.return_value = Const.EMPTY
            compare_content = {'a96accc25dd23ac0': Solution.DEFAULTS[Solution.BEATS]}
            snippy = Snippy()
            cause = snippy.run_cli(['snippy', 'create', '--solution'])  ## workflow
            assert cause == 'NOK: could not identify edited content category - please keep tags in place'
            assert not Database.get_solutions()
            snippy.release()
            snippy = None
            Database.delete_storage()

        ## Brief: Try to create new solution with a template that cannot be identified. In this case
        ##        the user has changed the input template completely and it has lost tags that identify
        ##        it as a solution content.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            template = ('################################################################################',
                        '## description',
                        '################################################################################',
                        '',
                        '################################################################################',
                        '## solutions',
                        '################################################################################',
                        '',
                        '################################################################################',
                        '## configurations',
                        '################################################################################',
                        '',
                        '################################################################################',
                        '## whiteboard',
                        '################################################################################',
                        '')
            mock_call_editor.return_value = Const.NEWLINE.join(template)
            compare_content = {'a96accc25dd23ac0': Solution.DEFAULTS[Solution.BEATS]}
            snippy = Snippy(['snippy', 'create', '--solution'])  ## workflow
            cause = snippy.run_cli()
            assert cause == 'NOK: could not identify edited content category - please keep tags in place'
            assert not Database.get_solutions()
            snippy.release()
            snippy = None
            Database.delete_storage()

    @mock.patch.object(Editor, 'call_editor')
    @mock.patch.object(Config, '_storage_file')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    def test_create_solution_from_editor(self, mock_isfile, mock_storage_file, mock_call_editor):
        """Create solution from editor."""

        mock_isfile.return_value = True
        mock_storage_file.return_value = Database.get_storage()

        ## Brief: Create new solution by defining all values from editor.
        with mock.patch('snippy.migrate.migrate.open', mock.mock_open(), create=True) as mock_file:
            snippy = Snippy()
            template = Solution.get_template(Solution.DEFAULTS[Solution.BEATS])
            mock_call_editor.return_value = template
            compare_content = {'a96accc25dd23ac0': Solution.DEFAULTS[Solution.BEATS]}
            cause = snippy.run_cli(['snippy', 'create', '--solution', '--editor'])  ## workflow
            assert cause == Cause.ALL_OK
            assert len(Database.get_solutions()) == 1
            Solution.test_content(snippy, mock_file, compare_content)
            snippy.release()
            snippy = None
            Database.delete_storage()

    # pylint: disable=duplicate-code
    def teardown_class(self):
        """Teardown each test."""

        Database.delete_all_contents()
        Database.delete_storage()
