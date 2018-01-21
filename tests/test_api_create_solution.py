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
        """Create solution from API."""

        mock_isfile.return_value = True
        mock_get_utc_time.return_value = Solution.UTC1
        mock__caller.return_value = 'snippy.testing.testing:123'
        mock_get_db_location.return_value = Database.get_storage()

        ## Brief: Call POST /api/v1/solutions to create new solution.
        solution = Solution.DEFAULTS[Solution.BEATS]
        compare_content = {'a96accc25dd23ac': Solution.DEFAULTS[Solution.BEATS]}
        headers = {'content-type': 'application/json; charset=UTF-8', 'content-length': '2204'}
        body = [solution]
        sys.argv = ['snippy', '--server']
        snippy = Snippy()
        snippy.run()
        result = testing.TestClient(snippy.server.api).simulate_post(path='/api/v1/solutions',  ## apiflow
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

#        ## Brief: Call POST /api/v1/snippets to create new snippet. In this case the
#        ##        links and list are defined as list in the JSON message. Note that
#        ##        the default input for tags and links from Snippet.REMOVE maps to a
#        ##        string but the syntax in this case maps to lists with multiple items.
#        snippet = {'data': Const.NEWLINE.join(Snippet.DEFAULTS[Snippet.REMOVE]['data']),
#                   'brief': Snippet.DEFAULTS[Snippet.REMOVE]['brief'],
#                   'group': Snippet.DEFAULTS[Snippet.REMOVE]['group'],
#                   'tags': ['cleanup', 'container', 'docker', 'docker-ce', 'moby'],
#                   'links': ['https://docs.docker.com/engine/reference/commandline/rm/']}
#        compare_content = {'54e41e9b52a02b63': Snippet.DEFAULTS[Snippet.REMOVE]}
#        headers = {'content-type': 'application/json; charset=UTF-8', 'content-length': '450'}
#        body = [Snippet.DEFAULTS[Snippet.REMOVE]]
#        sys.argv = ['snippy', '--server']
#        snippy = Snippy()
#        snippy.run()
#        result = testing.TestClient(snippy.server.api).simulate_post(path='/api/v1/snippets',  ## apiflow
#                                                                     headers={'accept': 'application/json'},
#                                                                     body=json.dumps(snippet))
#        assert result.headers == headers
#        assert Snippet.sorted_json_list(result.json) == Snippet.sorted_json_list(body)
#        assert result.status == falcon.HTTP_201
#        assert len(Database.get_snippets()) == 1
#        Snippet.test_content2(compare_content)
#        snippy.release()
#        snippy = None
#        Database.delete_storage()
#
#        ## Brief: Call POST /api/v1/snippets to create new snippet. In this case the
#        ##        content data is defined in string context where each line is separated
#        ##        with a newlin.
#        mock_get_utc_time.return_value = Snippet.UTC2
#        snippet = {'data': Const.NEWLINE.join(Snippet.DEFAULTS[Snippet.EXITED]['data']),
#                   'brief': Snippet.DEFAULTS[Snippet.EXITED]['brief'],
#                   'group': Snippet.DEFAULTS[Snippet.EXITED]['group'],
#                   'tags': Const.DELIMITER_TAGS.join(Snippet.DEFAULTS[Snippet.EXITED]['tags']),
#                   'links': Const.DELIMITER_LINKS.join(Snippet.DEFAULTS[Snippet.EXITED]['links'])}
#        compare_content = {'49d6916b6711f13d': Snippet.DEFAULTS[Snippet.EXITED]}
#        headers = {'content-type': 'application/json; charset=UTF-8', 'content-length': '655'}
#        body = [Snippet.DEFAULTS[Snippet.EXITED]]
#        sys.argv = ['snippy', '--server']
#        snippy = Snippy()
#        snippy.run()
#        result = testing.TestClient(snippy.server.api).simulate_post(path='/api/v1/snippets',  ## apiflow
#                                                                     headers={'accept': 'application/json'},
#                                                                     body=json.dumps(snippet))
#        assert result.headers == headers
#        assert Snippet.sorted_json_list(result.json) == Snippet.sorted_json_list(body)
#        assert result.status == falcon.HTTP_201
#        assert len(Database.get_snippets()) == 1
#        Snippet.test_content2(compare_content)
#        snippy.release()
#        snippy = None
#        Database.delete_storage()
#        mock_get_utc_time.return_value = Snippet.UTC1
#
#        ## Brief: Call POST /api/v1/snippets to create new snippet. In this case the
#        ##        content data is defined in list context where each line is an item
#        ##        in a list.
#        mock_get_utc_time.return_value = Snippet.UTC2
#        snippet = {'data': ['docker rm $(docker ps --all -q -f status=exited)\n\n\n\n',
#                            'docker images -q --filter dangling=true | xargs docker rmi'],
#                   'brief': Snippet.DEFAULTS[Snippet.EXITED]['brief'],
#                   'group': Snippet.DEFAULTS[Snippet.EXITED]['group'],
#                   'tags': Const.DELIMITER_TAGS.join(Snippet.DEFAULTS[Snippet.EXITED]['tags']),
#                   'links': Const.DELIMITER_LINKS.join(Snippet.DEFAULTS[Snippet.EXITED]['links'])}
#        compare_content = {'49d6916b6711f13d': Snippet.DEFAULTS[Snippet.EXITED]}
#        headers = {'content-type': 'application/json; charset=UTF-8', 'content-length': '655'}
#        body = [Snippet.DEFAULTS[Snippet.EXITED]]
#        sys.argv = ['snippy', '--server']
#        snippy = Snippy()
#        snippy.run()
#        result = testing.TestClient(snippy.server.api).simulate_post(path='/api/v1/snippets',  ## apiflow
#                                                                     headers={'accept': 'application/json'},
#                                                                     body=json.dumps(snippet))
#        assert result.headers == headers
#        assert Snippet.sorted_json_list(result.json) == Snippet.sorted_json_list(body)
#        assert result.status == falcon.HTTP_201
#        assert len(Database.get_snippets()) == 1
#        Snippet.test_content2(compare_content)
#        snippy.release()
#        snippy = None
#        Database.delete_storage()
#        mock_get_utc_time.return_value = Snippet.UTC1
#
#        ## Brief: Call POST /api/v1/snippets to create new snippet with only data.
#        snippet = {'data': ['docker rm $(docker ps --all -q -f status=exited)\n']}
#        headers = {'content-type': 'application/json; charset=UTF-8', 'content-length': '301'}
#        body = [{'data': ['docker rm $(docker ps --all -q -f status=exited)'],
#                 'brief': '',
#                 'group':
#                 'default',
#                 'tags': [],
#                 'links': [],
#                 'category': 'snippet',
#                 'filename': '',
#                 'runalias': '',
#                 'versions': '',
#                 'utc': '2017-10-14 19:56:31',
#                 'digest': '3d855210284302d58cf383ea25d8abdea2f7c61c4e2198da01e2c0896b0268dd'}]
#        compare = {'3d855210284302d5': body[0]}
#        sys.argv = ['snippy', '--server']
#        snippy = Snippy()
#        snippy.run()
#        result = testing.TestClient(snippy.server.api).simulate_post(path='/api/v1/snippets',  ## apiflow
#                                                                     headers={'accept': 'application/json'},
#                                                                     body=json.dumps(snippet))
#        assert result.headers == headers
#        assert Snippet.sorted_json_list(result.json) == Snippet.sorted_json_list(body)
#        assert result.status == falcon.HTTP_201
#        assert len(Database.get_snippets()) == 1
#        Snippet.test_content2(compare)
#        snippy.release()
#        snippy = None
#        Database.delete_storage()
#
#    @mock.patch('snippy.server.server.SnippyServer')
#    @mock.patch('snippy.migrate.migrate.os.path.isfile')
#    @mock.patch.object(Cause, '_caller')
#    @mock.patch.object(Config, 'get_utc_time')
#    @mock.patch.object(Config, '_storage_file')
#    def test_api_create_snippets_from_api(self, mock_get_db_location, mock_get_utc_time, mock__caller, mock_isfile, _):
#        """Create snippets from API."""
#
#        mock_isfile.return_value = True
#        mock_get_utc_time.return_value = Snippet.UTC1
#        mock__caller.return_value = 'snippy.testing.testing:123'
#        mock_get_db_location.return_value = Database.get_storage()
#
#        ## Brief: Call POST /api/v1/snippets in list context to create new snippets.
#        snippets = [Snippet.DEFAULTS[Snippet.REMOVE], Snippet.DEFAULTS[Snippet.FORCED]]
#        compare_content = {'54e41e9b52a02b63': Snippet.DEFAULTS[Snippet.REMOVE]}
#        headers = {'content-type': 'application/json; charset=UTF-8', 'content-length': '969'}
#        body = snippets
#        sys.argv = ['snippy', '--server']
#        snippy = Snippy()
#        snippy.run()
#        result = testing.TestClient(snippy.server.api).simulate_post(path='/api/v1/snippets',  ## apiflow
#                                                                     headers={'accept': 'application/json'},
#                                                                     body=json.dumps(snippets))
#        assert result.headers == headers
#        assert Snippet.sorted_json_list(result.json) == Snippet.sorted_json_list(body)
#        assert result.status == falcon.HTTP_201
#        assert len(Database.get_snippets()) == 2
#        Snippet.test_content2(compare_content)
#        snippy.release()
#        snippy = None
#        Database.delete_storage()

    # pylint: disable=duplicate-code
    def teardown_class(self):
        """Teardown each test."""

        Database.delete_all_contents()
        Database.delete_storage()
