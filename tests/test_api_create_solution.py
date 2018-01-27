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

"""test_api_create_solution.py: Test POST /solutions API."""

import json
import sys

import mock
import falcon
from falcon import testing

from snippy.cause.cause import Cause
from snippy.config.config import Config
from snippy.metadata import __homepage__
from snippy.metadata import __version__
from snippy.snip import Snippy
from tests.testlib.solution_helper import SolutionHelper as Solution
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database


class TestApiCreateSolution(object):
    """Test POST /solutions API."""

    @mock.patch('snippy.server.server.SnippyServer')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    @mock.patch.object(Cause, '_caller')
    @mock.patch.object(Config, 'get_utc_time')
    @mock.patch.object(Config, '_storage_file')
    def test_api_create_solution_from_api(self, mock_get_db_location, mock_get_utc_time, mock__caller, mock_isfile, _):
        """Create one solution from API."""

        mock_isfile.return_value = True
        mock_get_utc_time.return_value = Solution.UTC1
        mock__caller.return_value = 'snippy.testing.testing:123'
        mock_get_db_location.return_value = Database.get_storage()

        ## Brief: Call POST /snippy/api/v1/solutions to create new solution.
        solution = Solution.DEFAULTS[Solution.BEATS]
        compare_content = {'a96accc25dd23ac': Solution.DEFAULTS[Solution.BEATS]}
        headers = {'content-type': 'application/json; charset=UTF-8', 'content-length': '2204'}
        body = [solution]
        sys.argv = ['snippy', '--server']
        snippy = Snippy()
        snippy.run()
        result = testing.TestClient(snippy.server.api).simulate_post(path='/snippy/api/v1/solutions',  ## apiflow
                                                                     headers={'accept': 'application/json'},
                                                                     body=json.dumps(solution))
        assert result.headers == headers
        assert Solution.sorted_json_list(result.json) == Solution.sorted_json_list(body)
        assert result.status == falcon.HTTP_201
        assert len(Database.get_solutions()) == 1
        Solution.test_content2(compare_content)
        snippy.release()
        snippy = None
        Database.delete_storage()

    @mock.patch('snippy.server.server.SnippyServer')
    @mock.patch('snippy.migrate.migrate.os.path.isfile')
    @mock.patch.object(Cause, '_caller')
    @mock.patch.object(Config, 'get_utc_time')
    @mock.patch.object(Config, '_storage_file')
    def test_api_create_solutions_from_api(self, mock_get_db_location, mock_get_utc_time, mock__caller, mock_isfile, _):
        """Create list of solutions from API."""

        mock_isfile.return_value = True
        mock_get_utc_time.side_effect = (Solution.UTC1,)*2 + (Solution.UTC3,)*2 + (Solution.UTC1,)*1 + (None,)  # [REF_UTC]
        mock__caller.return_value = 'snippy.testing.testing:123'
        mock_get_db_location.return_value = Database.get_storage()

        ## Brief: Call POST /snippy/api/v1/solutions in list context to create new
        ##        solutions.
        solutions = [Solution.DEFAULTS[Solution.BEATS], Solution.DEFAULTS[Solution.KAFKA]]
        compare_content = {'a96accc25dd23ac': Solution.DEFAULTS[Solution.BEATS],
                           'eeef5ca': Solution.DEFAULTS[Solution.KAFKA]}
        headers = {'content-type': 'application/json; charset=UTF-8', 'content-length': '6618'}
        body = solutions
        sys.argv = ['snippy', '--server']
        snippy = Snippy()
        snippy.run()
        result = testing.TestClient(snippy.server.api).simulate_post(path='/snippy/api/v1/solutions',  ## apiflow
                                                                     headers={'accept': 'application/json'},
                                                                     body=json.dumps(solutions))
        assert result.headers == headers
        assert Solution.sorted_json_list(result.json) == Solution.sorted_json_list(body)
        assert result.status == falcon.HTTP_201
        assert len(Database.get_solutions()) == 2
        Solution.test_content2(compare_content)
        snippy.release()
        snippy = None
        Database.delete_storage()

    # pylint: disable=duplicate-code
    def teardown_class(self):
        """Teardown each test."""

        Database.delete_all_contents()
        Database.delete_storage()