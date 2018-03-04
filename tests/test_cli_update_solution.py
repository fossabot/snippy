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

"""test_cli_update_solution: Test workflows for updating solutions."""

import pytest

from snippy.cause import Cause
from tests.testlib.content import Content
from tests.testlib.solution_helper import SolutionHelper as Solution
from tests.testlib.sqlite3db_helper import Sqlite3DbHelper as Database


class TestCliUpdateSolution(object):
    """Test workflows for updating solutions."""

    @pytest.mark.usefixtures('snippy', 'default-solutions')
    def test_cli_update_solution_001(self, snippy, edited_beats, mocker):
        """Update solution with digest."""

        ## Brief: Update solution based on short message digest. Only the
        ##        content data is updated.
        template = Solution.get_template(Solution.DEFAULTS[Solution.BEATS])
        template = template.replace('## description', '## updated content description')
        content_read = {
            'f8ded660166ebeef': Solution.get_dictionary(template),
            Solution.NGINX_DIGEST: Solution.DEFAULTS[Solution.NGINX]
        }
        edited_beats.return_value = template
        cause = snippy.run_cli(['snippy', 'update', '--solution', '-d', 'a96accc25dd23ac0'])  ## workflow
        assert cause == Cause.ALL_OK
        assert len(Database.get_solutions()) == 2
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('snippy', 'default-solutions')
    def test_cli_update_solution_002(self, snippy, edited_beats, mocker):
        """Update solution with digest."""

        ## Brief: Update solution based on very short message digest. This
        ##        must match to a single solution that must be updated.
        template = Solution.get_template(Solution.DEFAULTS[Solution.BEATS])
        template = template.replace('## description', '## updated content description')
        content_read = {
            'f8ded660166ebeef': Solution.get_dictionary(template),
            Solution.NGINX_DIGEST: Solution.DEFAULTS[Solution.NGINX]
        }
        edited_beats.return_value = template
        cause = snippy.run_cli(['snippy', 'update', '--solution', '--digest', 'a96ac'])  ## workflow
        assert cause == Cause.ALL_OK
        assert len(Database.get_solutions()) == 2
        Content.verified(mocker, snippy, content_read)


    @pytest.mark.usefixtures('snippy', 'default-solutions')
    def test_cli_update_solution_003(self, snippy, edited_beats, mocker):
        """Update solution with digest."""

        ## Brief: Update solution based on long message digest. Only the
        ##        content data is updated.
        template = Solution.get_template(Solution.DEFAULTS[Solution.BEATS])
        template = template.replace('## description', '## updated content description')
        content_read = {
            'f8ded660166ebeef': Solution.get_dictionary(template),
            Solution.NGINX_DIGEST: Solution.DEFAULTS[Solution.NGINX]
        }
        edited_beats.return_value = template
        cause = snippy.run_cli(['snippy', 'update', '--solution', '-d', 'a96accc25dd23ac0554032e25d773f3931d70b1d986664b13059e5e803df6da8'])  ## workflow # pylint: disable=line-too-long
        assert cause == Cause.ALL_OK
        assert len(Database.get_solutions()) == 2
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('snippy', 'default-solutions')
    def test_cli_update_solution_004(self, snippy, edited_beats, mocker):
        """Update solution with digest."""

        ## Brief: Update solution based on message digest and accidentally
        ##        define snippet category explicitly from command line. In
        ##        this case the solution is updated properly regardless of
        ##        incorrect category.
        template = Solution.get_template(Solution.DEFAULTS[Solution.BEATS])
        template = template.replace('## description', '## updated content description')
        content_read = {
            'f8ded660166ebeef': Solution.get_dictionary(template),
            Solution.NGINX_DIGEST: Solution.DEFAULTS[Solution.NGINX]
        }
        edited_beats.return_value = template
        cause = snippy.run_cli(['snippy', 'update', '--snippet', '-d', 'a96accc25dd23ac0'])  ## workflow
        assert cause == Cause.ALL_OK
        assert len(Database.get_solutions()) == 2
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('snippy', 'default-solutions')
    def test_cli_update_solution_005(self, snippy, edited_beats, mocker):
        """Update solution with digest."""

        ## Brief: Update solution based on message digest and accidentally
        ##        implicitly use snippet category by not using content
        ##        category option that defaults to snippet category. In this
        ##        case the solution is updated properly regardless of
        ##        incorrect category.
        template = Solution.get_template(Solution.DEFAULTS[Solution.BEATS])
        template = template.replace('## description', '## updated content description')
        content_read = {
            'f8ded660166ebeef': Solution.get_dictionary(template),
            Solution.NGINX_DIGEST: Solution.DEFAULTS[Solution.NGINX]
        }
        edited_beats.return_value = template
        cause = snippy.run_cli(['snippy', 'update', '-d', 'a96accc25dd23ac0'])  ## workflow
        assert cause == Cause.ALL_OK
        assert len(Database.get_solutions()) == 2
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('snippy', 'default-solutions')
    def test_cli_update_solution_006(self, snippy, edited_beats, mocker):
        """Update solution with digest."""

        ## Brief: Try to update solution with message digest that cannot be
        ##        found. No changes must be made to stored content.
        template = Solution.get_template(Solution.DEFAULTS[Solution.BEATS])
        template = template.replace('## description', '## updated content description')
        content_read = {
            Solution.BEATS_DIGEST: Solution.DEFAULTS[Solution.BEATS],
            Solution.NGINX_DIGEST: Solution.DEFAULTS[Solution.NGINX]
        }
        edited_beats.return_value = template
        cause = snippy.run_cli(['snippy', 'update', '--solution', '-d', '123456789abcdef0'])  ## workflow
        assert cause == 'NOK: cannot find content with message digest 123456789abcdef0'
        assert len(Database.get_solutions()) == 2
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('snippy', 'default-solutions')
    def test_cli_update_solution_007(self, snippy, edited_beats, mocker):
        """Update solution with digest."""

        ## Brief: Try to update solution with empty message digest. Nothing
        ##        should be updated in this case because the empty digest
        ##        matches to more than one solution. Only one content can be
        ##        updated at the time.
        template = Solution.get_template(Solution.DEFAULTS[Solution.BEATS])
        template = template.replace('## description', '## updated content description')
        content_read = {
            Solution.BEATS_DIGEST: Solution.DEFAULTS[Solution.BEATS],
            Solution.NGINX_DIGEST: Solution.DEFAULTS[Solution.NGINX]
        }
        edited_beats.return_value = template
        cause = snippy.run_cli(['snippy', 'update', '--solution', '-d', ''])  ## workflow
        assert cause == 'NOK: cannot use empty message digest to update content'
        assert len(Database.get_solutions()) == 2
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('snippy', 'default-solutions')
    def test_cli_update_solution_008(self, snippy, edited_beats, mocker):
        """Update solution with data."""

        ## Brief: Update solution based on content data.
        template = Solution.get_template(Solution.DEFAULTS[Solution.BEATS])
        template = template.replace('## description', '## updated content description')
        content_read = {
            'f8ded660166ebeef': Solution.get_dictionary(template),
            Solution.NGINX_DIGEST: Solution.DEFAULTS[Solution.NGINX]
        }
        edited_beats.return_value = template
        data = Solution.get_template(Solution.DEFAULTS[Solution.BEATS])
        cause = snippy.run_cli(['snippy', 'update', '--solution', '-c', data])  ## workflow
        assert cause == Cause.ALL_OK
        assert len(Database.get_solutions()) == 2
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('snippy', 'default-solutions')
    def test_cli_update_solution_009(self, snippy, edited_beats, mocker):
        """Update solution with data."""

        ## Brief: Try to update solution based on content data that is not
        ##        found.
        template = Solution.get_template(Solution.DEFAULTS[Solution.BEATS])
        template = template.replace('## description', '## updated content description')
        content_read = {
            Solution.BEATS_DIGEST: Solution.DEFAULTS[Solution.BEATS],
            Solution.NGINX_DIGEST: Solution.DEFAULTS[Solution.NGINX]
        }
        edited_beats.return_value = template
        cause = snippy.run_cli(['snippy', 'update', '--solution', '--content', 'solution not existing'])  ## workflow
        assert cause == 'NOK: cannot find content with content data \'solution not existing\''
        assert len(Database.get_solutions()) == 2
        Content.verified(mocker, snippy, content_read)

    @pytest.mark.usefixtures('snippy', 'default-solutions')
    def test_cli_update_solution_010(self, snippy, edited_beats, mocker):
        """Update solution with data."""

        ## Brief: Try to update solution with empty content data. Nothing must
        ##        be updatedin this case because there is more than one content
        ##        stored.
        template = Solution.get_template(Solution.DEFAULTS[Solution.BEATS])
        template = template.replace('## description', '## updated content description')
        content_read = {
            Solution.BEATS_DIGEST: Solution.DEFAULTS[Solution.BEATS],
            Solution.NGINX_DIGEST: Solution.DEFAULTS[Solution.NGINX]
        }
        edited_beats.return_value = template
        cause = snippy.run_cli(['snippy', 'update', '--solution', '-c', ''])  ## workflow
        assert cause == 'NOK: cannot use empty content data to update content'
        assert len(Database.get_solutions()) == 2
        Content.verified(mocker, snippy, content_read)

    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        Database.delete_all_contents()
        Database.delete_storage()