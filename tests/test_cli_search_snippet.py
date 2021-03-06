#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Snippy - command, solution, reference and code snippet manager.
#  Copyright 2017-2019 Heikki J. Laaksonen  <laaksonen.heikki.j@gmail.com>
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

"""test_cli_search_snippet: Test workflows for searching snippets."""

import pytest

from snippy.cause import Cause
from snippy.constants import Constants as Const
from tests.lib.content import Content
from tests.lib.helper import Helper


class TestCliSearchSnippet(object):  # pylint: disable=too-many-public-methods, too-many-lines
    """Test workflows for searching snippets."""

    @staticmethod
    @pytest.mark.usefixtures('default-snippets')
    def test_cli_search_snippet_001(snippy, capsys):
        """Search snippets with ``sall`` option.

        Search snippets from all fields. The match is made from one
        snippet content data.
        """

        output = (
            '1. Remove docker image with force @docker [53908d68425c61dc]',
            '',
            '   $ docker rm --force redis',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '   > https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes',
            '',
            'OK',
            ''
        )
        cause = snippy.run(['snippy', 'search', '--sall', 'redis', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    @staticmethod
    @pytest.mark.usefixtures('default-snippets')
    def test_cli_search_snippet_002(snippy, capsys):
        """Search snippets with ``sall`` option.

        Search snippets from all fields. The match is made from one snippet
        brief description.
        """

        output = (
            '1. Remove all docker containers with volumes @docker [54e41e9b52a02b63]',
            '',
            '   $ docker rm --volumes $(docker ps --all --quiet)',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '',
            'OK',
            ''
        )
        cause = snippy.run(['snippy', 'search', '--sall', 'all', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    @staticmethod
    @pytest.mark.usefixtures('default-snippets')
    def test_cli_search_snippet_003(snippy, capsys):
        """Search snippets with ``sall`` option.

        Search snippets from all fields. The match is made from two snippets
        group metadata.
        """

        output = (
            '1. Remove all docker containers with volumes @docker [54e41e9b52a02b63]',
            '',
            '   $ docker rm --volumes $(docker ps --all --quiet)',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '',
            '2. Remove docker image with force @docker [53908d68425c61dc]',
            '',
            '   $ docker rm --force redis',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '   > https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes',
            '',
            'OK',
            ''
        )
        cause = snippy.run(['snippy', 'search', '--sall', 'docker', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    @staticmethod
    @pytest.mark.usefixtures('default-snippets')
    def test_cli_search_snippet_004(snippy, capsys):
        """Search snippets with ``sall`` option.

        Search snippets from all fields. The match is made from two snippets
        tags metadata.
        """

        output = (
            '1. Remove all docker containers with volumes @docker [54e41e9b52a02b63]',
            '',
            '   $ docker rm --volumes $(docker ps --all --quiet)',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '',
            '2. Remove docker image with force @docker [53908d68425c61dc]',
            '',
            '   $ docker rm --force redis',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '   > https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes',
            '',
            'OK',
            ''
        )
        cause = snippy.run(['snippy', 'search', '--sall', 'moby', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    @staticmethod
    @pytest.mark.usefixtures('default-snippets')
    def test_cli_search_snippet_005(snippy, capsys):
        """Search snippets with ``sall`` option.

        Search snippets from all fields. The match is made from one snippet
        links metadata.
        """

        output = (
            '1. Remove docker image with force @docker [53908d68425c61dc]',
            '',
            '   $ docker rm --force redis',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '   > https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes',
            '',
            'OK',
            ''
        )
        cause = snippy.run(['snippy', 'search', '--sall', 'tutorials', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    @staticmethod
    @pytest.mark.usefixtures('default-snippets')
    def test_cli_search_snippet_006(snippy, capsys):
        """Search snippets with ``sall`` option.

        Search snippets from all fields. The match is made from one snippet
        digest.
        """

        output = (
            '1. Remove docker image with force @docker [53908d68425c61dc]',
            '',
            '   $ docker rm --force redis',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '   > https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes',
            '',
            'OK',
            ''
        )
        cause = snippy.run(['snippy', 'search', '--sall', '53908d68425c61dc', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    @staticmethod
    @pytest.mark.usefixtures('default-snippets')
    def test_cli_search_snippet_007(snippy, capsys):
        """Search snippets with ``sall`` option.

        Search snippets from all fields with two keywords. The match is made
        from two different snippets. In this search keywords are separated
        by comma.
        """

        output = (
            '1. Remove all docker containers with volumes @docker [54e41e9b52a02b63]',
            '',
            '   $ docker rm --volumes $(docker ps --all --quiet)',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '',
            '2. Remove docker image with force @docker [53908d68425c61dc]',
            '',
            '   $ docker rm --force redis',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '   > https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes',
            '',
            'OK',
            ''
        )
        cause = snippy.run(['snippy', 'search', '--sall', 'redis,--quiet', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    @staticmethod
    @pytest.mark.usefixtures('default-snippets', 'import-netcat')
    def test_cli_search_snippet_008(snippy, capsys):
        """Search snippets with ``sall`` option.

        Search snippets from all fields with three keywords. The match is made
        two different snippts. In this case search keywords are separated by
        spaces.
        """

        output = (
            '1. Remove all docker containers with volumes @docker [54e41e9b52a02b63]',
            '',
            '   $ docker rm --volumes $(docker ps --all --quiet)',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '',
            '2. Test if specific port is open @linux [f3fd167c64b6f97e]',
            '',
            '   $ nc -v 10.183.19.189 443',
            '   $ nmap 10.183.19.189',
            '',
            '   # linux,netcat,networking,port',
            '   > https://www.commandlinux.com/man-page/man1/nc.1.html',
            '',
            'OK',
            ''
        )
        cause = snippy.run(['snippy', 'search', '--sall', 'netcat --quiet all', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    @staticmethod
    @pytest.mark.usefixtures('default-snippets')
    def test_cli_search_snippet_009(snippy, capsys):
        """Search snippets with ``sall`` option.

        List all snippets by defining search criteria of search all to
        'match any'.
        """

        output = (
            '1. Remove all docker containers with volumes @docker [54e41e9b52a02b63]',
            '',
            '   $ docker rm --volumes $(docker ps --all --quiet)',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '',
            '2. Remove docker image with force @docker [53908d68425c61dc]',
            '',
            '   $ docker rm --force redis',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '   > https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes',
            '',
            'OK',
            ''
        )
        cause = snippy.run(['snippy', 'search', '--sall', '.', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    @staticmethod
    @pytest.mark.usefixtures('default-snippets')
    def test_cli_search_snippet_010(snippy, capsys):
        """Search snippets with ``sall`` option.

        List all snippets by leaving search criteria for 'search all fields'
        out completely. This is translated to 'match any'.
        """

        output = (
            '1. Remove all docker containers with volumes @docker [54e41e9b52a02b63]',
            '',
            '   $ docker rm --volumes $(docker ps --all --quiet)',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '',
            '2. Remove docker image with force @docker [53908d68425c61dc]',
            '',
            '   $ docker rm --force redis',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '   > https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes',
            '',
            'OK',
            ''
        )
        cause = snippy.run(['snippy', 'search', '--sall', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    @staticmethod
    @pytest.mark.usefixtures('default-snippets')
    def test_cli_search_snippet_011(snippy, capsys):
        """Search snippets with ``sall`` option.

        List all snippets by leaving search criteria of search all as empty.
        This is translated to 'match any'.
        """

        output = (
            '1. Remove all docker containers with volumes @docker [54e41e9b52a02b63]',
            '',
            '   $ docker rm --volumes $(docker ps --all --quiet)',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '',
            '2. Remove docker image with force @docker [53908d68425c61dc]',
            '',
            '   $ docker rm --force redis',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '   > https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes',
            '',
            'OK',
            ''
        )
        cause = snippy.run(['snippy', 'search', '--sall', '', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    @staticmethod
    @pytest.mark.usefixtures('snippy')
    def test_cli_search_snippet_012(snippy, capsys):
        """Search snippets with ``sall`` option.

        Try to search snippets when there are no content stored. The used
        search keyword matches to 'match any' that tries to list all the
        content.
        """

        output = 'NOK: cannot find content with given search criteria\n'
        cause = snippy.run(['snippy', 'search', '--sall', '.', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == 'NOK: cannot find content with given search criteria'
        assert out == output
        assert not err

    @staticmethod
    @pytest.mark.usefixtures('default-snippets')
    def test_cli_search_snippet_013(snippy, capsys):
        """Search snippets with ``sall`` option.

        Try to search snippets with keyword that cannot be found.
        """

        output = 'NOK: cannot find content with given search criteria\n'
        cause = snippy.run(['snippy', 'search', '--sall', 'not-found', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == 'NOK: cannot find content with given search criteria'
        assert out == output
        assert not err

    @staticmethod
    @pytest.mark.usefixtures('default-snippets', 'import-netcat')
    def test_cli_search_snippet_014(snippy, capsys):
        """Search snippets with ``stag`` option.

        Search snippets from tag field. The match is made from one snippet.
        """

        output = (
            '1. Test if specific port is open @linux [f3fd167c64b6f97e]',
            '',
            '   $ nc -v 10.183.19.189 443',
            '   $ nmap 10.183.19.189',
            '',
            '   # linux,netcat,networking,port',
            '   > https://www.commandlinux.com/man-page/man1/nc.1.html',
            '',
            'OK',
            ''
        )
        cause = snippy.run(['snippy', 'search', '--stag', 'netcat', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    @staticmethod
    @pytest.mark.usefixtures('default-snippets', 'import-netcat')
    def test_cli_search_snippet_015(snippy, capsys):
        """Search snippets with ``stag`` option.

        Search snippets from tag field. No matches are made.
        """

        output = 'NOK: cannot find content with given search criteria\n'
        cause = snippy.run(['snippy', 'search', '--stag', 'not-found', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == 'NOK: cannot find content with given search criteria'
        assert out == output
        assert not err

    @staticmethod
    @pytest.mark.usefixtures('default-snippets')
    def test_cli_search_snippet_016(snippy, capsys):
        """Search snippets with ``stag`` option.

        List all snippets by leaving search criteria for 'search tags' out
        completely. This is translated to 'match any'.
        """

        output = (
            '1. Remove all docker containers with volumes @docker [54e41e9b52a02b63]',
            '',
            '   $ docker rm --volumes $(docker ps --all --quiet)',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '',
            '2. Remove docker image with force @docker [53908d68425c61dc]',
            '',
            '   $ docker rm --force redis',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '   > https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes',
            '',
            'OK',
            ''
        )
        cause = snippy.run(['snippy', 'search', '--stag', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err


    @staticmethod
    @pytest.mark.usefixtures('default-snippets', 'import-netcat')
    def test_cli_search_snippet_017(snippy, capsys):
        """Search snippets with ``sgrp`` option.

        Search snippets from group field. The match is made from one snippet.
        """

        output = (
            '1. Test if specific port is open @linux [f3fd167c64b6f97e]',
            '',
            '   $ nc -v 10.183.19.189 443',
            '   $ nmap 10.183.19.189',
            '',
            '   # linux,netcat,networking,port',
            '   > https://www.commandlinux.com/man-page/man1/nc.1.html',
            '',
            'OK',
            ''
        )
        cause = snippy.run(['snippy', 'search', '--sgrp', 'linux', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    @staticmethod
    @pytest.mark.usefixtures('default-snippets', 'import-netcat')
    def test_cli_search_snippet_018(snippy, capsys):
        """Search snippets with ``sgrp`` option.

        Search snippets from group field. No matches are made.
        """

        output = 'NOK: cannot find content with given search criteria\n'
        cause = snippy.run(['snippy', 'search', '--sgrp', 'not-found', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == 'NOK: cannot find content with given search criteria'
        assert out == output
        assert not err

    @staticmethod
    @pytest.mark.usefixtures('default-snippets')
    def test_cli_search_snippet_019(snippy, capsys):
        """Search snippets with ``sgrp`` option.

        List all snippets by leaving search criteria for 'search groups' out
        completely. This is translated to 'match any'.
        """

        output = (
            '1. Remove all docker containers with volumes @docker [54e41e9b52a02b63]',
            '',
            '   $ docker rm --volumes $(docker ps --all --quiet)',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '',
            '2. Remove docker image with force @docker [53908d68425c61dc]',
            '',
            '   $ docker rm --force redis',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '   > https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes',
            '',
            'OK',
            ''
        )
        cause = snippy.run(['snippy', 'search', '--sgrp', '', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    @staticmethod
    @pytest.mark.usefixtures('default-snippets', 'default-solutions', 'import-netcat')
    def test_cli_search_snippet_020(snippy, capsys):
        """Search snippets with ``filter`` option.

        Search all content with a regexp filter. The filter removes all
        content from the search result returned with the `sall` option
        that do not match to the regexp in any of the resource field. In
        this case there are no regexp matches like '.*' included into the
        filter.
        """

        output = (
            '1. Remove all docker containers with volumes @docker [54e41e9b52a02b63]',
            '',
            '   $ docker rm --volumes $(docker ps --all --quiet)',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '',
            '2. Remove docker image with force @docker [53908d68425c61dc]',
            '',
            '   $ docker rm --force redis',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '   > https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes',
            '',
            'OK',
            ''
        )
        cause = snippy.run(['snippy', 'search', '--sall', '.', '--filter', 'engine', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    @staticmethod
    @pytest.mark.usefixtures('default-snippets', 'default-solutions', 'import-netcat')
    def test_cli_search_snippet_021(snippy, capsys):
        """Search snippets with ``filter`` option.

        Search all content with a regexp filter. The filter removes all
        content from the search result returned with the `sall` option
        that do not match to the regexp in any of the resource field. In
        this case there is a regexp match '.*' included into the filter.
        """

        output = (
            '1. Remove all docker containers with volumes @docker [54e41e9b52a02b63]',
            '',
            '   $ docker rm --volumes $(docker ps --all --quiet)',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '',
            '2. Remove docker image with force @docker [53908d68425c61dc]',
            '',
            '   $ docker rm --force redis',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '   > https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes',
            '',
            'OK',
            ''
        )
        cause = snippy.run(['snippy', 'search', '--scat', 'all', '--sall', '.', '--filter', '.*engine.*', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    @staticmethod
    @pytest.mark.usefixtures('default-snippets', 'default-solutions', 'import-netcat')
    def test_cli_search_snippet_022(snippy, capsys):
        """Search snippets with ``filter`` option.

        Search all content with a regexp filter. The filter removes all
        content from the search result returned with the `sall` option
        that do not match to the regexp in any of the resource field. In
        this case none of the resulting content match to the filter and
        no content is found.
        """

        output = 'NOK: cannot find content with given search criteria\n'
        cause = snippy.run(['snippy', 'search', '--sall', '.', '--filter', 'not-found'])
        out, err = capsys.readouterr()
        assert cause == 'NOK: cannot find content with given search criteria'
        assert out == output
        assert not err

    @staticmethod
    @pytest.mark.usefixtures('default-snippets', 'default-solutions')
    def test_cli_search_snippet_023(snippy, capsys):
        """Search snippets with ``filter`` option.

        Try to search snippets with a regexp filter that is not syntactically
        correct regular expression. In this case the filter must be excluded
        and all the results found with the `sall` search must be found.
        """

        output = (
            '1. Remove all docker containers with volumes @docker [54e41e9b52a02b63]',
            '',
            '   $ docker rm --volumes $(docker ps --all --quiet)',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '',
            '2. Remove docker image with force @docker [53908d68425c61dc]',
            '',
            '   $ docker rm --force redis',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '   > https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes',
            '',
            'NOK: listing matching content without filter because it was not syntactically correct regular expression',
            ''
        )
        cause = snippy.run(['snippy', 'search', '--sall', '.', '--filter', '[invalid(regexp', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == 'NOK: listing matching content without filter because it was not syntactically correct regular expression'
        assert out == Const.NEWLINE.join(output)
        assert not err

    @staticmethod
    @pytest.mark.usefixtures('default-snippets')
    def test_cli_search_snippet_024(snippy, capsys):
        """Search snippets with ``content`` option.

        Search snippets based on content data.
        """

        output = (
            '1. Remove all docker containers with volumes @docker [54e41e9b52a02b63]',
            '',
            '   $ docker rm --volumes $(docker ps --all --quiet)',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '',
            'OK',
            ''
        )
        cause = snippy.run(['snippy', 'search', '--content', 'docker rm --volumes $(docker ps --all --quiet)', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    @staticmethod
    @pytest.mark.usefixtures('default-snippets')
    def test_cli_search_snippet_025(snippy, capsys):
        """Search snippets with --content option.

        Search snippets based on content data that matches to beginnging
        of the content.
        """

        output = (
            '1. Remove all docker containers with volumes @docker [54e41e9b52a02b63]',
            '',
            '   $ docker rm --volumes $(docker ps --all --quiet)',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '',
            'OK',
            ''
        )
        cause = snippy.run(['snippy', 'search', '--content', 'docker rm --volumes', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    @staticmethod
    @pytest.mark.usefixtures('default-snippets')
    def test_cli_search_snippet_026(snippy, capsys):
        """Search snippets with ``content`` option.

        Search snippets based on content data that matches to a string in
        the middle of a content.
        """

        output = (
            '1. Remove all docker containers with volumes @docker [54e41e9b52a02b63]',
            '',
            '   $ docker rm --volumes $(docker ps --all --quiet)',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '',
            'OK',
            ''
        )
        cause = snippy.run(['snippy', 'search', '--content', 'volumes', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    @staticmethod
    @pytest.mark.usefixtures('default-snippets')
    def test_cli_search_snippet_027(snippy, capsys):
        """Search snippets with ``digest`` option.

        Search snippet by explicitly defining short message digest.
        """

        output = (
            '1. Remove docker image with force @docker [53908d68425c61dc]',
            '',
            '   $ docker rm --force redis',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '   > https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes',
            '',
            'OK',
            ''
        )
        cause = snippy.run(['snippy', 'search', '--digest', '53908d68425c61dc', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    @staticmethod
    @pytest.mark.usefixtures('default-snippets')
    def test_cli_search_snippet_028(snippy, capsys):
        """Search snippets with ``digest`` option.

        Search snippet by explicitly defining long message digest.
        """

        output = (
            '1. Remove docker image with force @docker [53908d68425c61dc]',
            '',
            '   $ docker rm --force redis',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '   > https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes',
            '',
            'OK',
            ''
        )
        cause = snippy.run(['snippy', 'search', '--digest', '53908d68425c61dc310c9ce49d530bd858c5be197990491ca20dbe888e6deac5', '--no-ansi'])  # pylint: disable=line-too-long
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    @staticmethod
    @pytest.mark.usefixtures('default-snippets')
    def test_cli_search_snippet_029(snippy, capsys):
        """Search snippets with ``digest`` option.

        Search snippets by defining one digit message digest. In this case
        the searched digit matches to two snippets.
        """

        output = (
            '1. Remove all docker containers with volumes @docker [54e41e9b52a02b63]',
            '',
            '   $ docker rm --volumes $(docker ps --all --quiet)',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '',
            '2. Remove docker image with force @docker [53908d68425c61dc]',
            '',
            '   $ docker rm --force redis',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '   > https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes',
            '',
            'OK',
            ''
        )
        cause = snippy.run(['snippy', 'search', '--digest', '5', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    @staticmethod
    @pytest.mark.usefixtures('default-snippets')
    def test_cli_search_snippet_030(snippy, capsys):
        """Search snippets with ``digest`` option.

        Search snippets by defining empty string as message digest. This
        matches to all content in all categories.
        """

        output = (
            '1. Remove all docker containers with volumes @docker [54e41e9b52a02b63]',
            '',
            '   $ docker rm --volumes $(docker ps --all --quiet)',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '',
            '2. Remove docker image with force @docker [53908d68425c61dc]',
            '',
            '   $ docker rm --force redis',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '   > https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes',
            '',
            'OK',
            ''
        )
        cause = snippy.run(['snippy', 'search', '--digest', '', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    @staticmethod
    @pytest.mark.usefixtures('default-snippets', 'import-netcat')
    def test_cli_search_snippet_031(snippy, capsys):
        """Search snippets with ``sall`` option.

        Search snippets from all fields of specific group. The match must not
        be made from other than defined group. In this case the list all must
        print the content of defined group.
        """

        output = (
            '1. Remove all docker containers with volumes @docker [54e41e9b52a02b63]',
            '',
            '   $ docker rm --volumes $(docker ps --all --quiet)',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '',
            '2. Remove docker image with force @docker [53908d68425c61dc]',
            '',
            '   $ docker rm --force redis',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '   > https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes',
            '',
            'OK',
            ''
        )
        cause = snippy.run(['snippy', 'search', '--sall', '.', '--sgrp', 'docker', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    @staticmethod
    @pytest.mark.usefixtures('default-snippets', 'import-netcat')
    def test_cli_search_snippet_032(snippy, capsys):
        """Search snippets with ``sall`` option.

        Search snippets from all fields of two different groups.
        """

        output = (
            '1. Remove all docker containers with volumes @docker [54e41e9b52a02b63]',
            '',
            '   $ docker rm --volumes $(docker ps --all --quiet)',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '',
            '2. Remove docker image with force @docker [53908d68425c61dc]',
            '',
            '   $ docker rm --force redis',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '   > https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes',
            '',
            '3. Test if specific port is open @linux [f3fd167c64b6f97e]',
            '',
            '   $ nc -v 10.183.19.189 443',
            '   $ nmap 10.183.19.189',
            '',
            '   # linux,netcat,networking,port',
            '   > https://www.commandlinux.com/man-page/man1/nc.1.html',
            '',
            'OK',
            ''
        )
        cause = snippy.run(['snippy', 'search', '--sall', '.', '--sgrp', 'docker,linux', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    @staticmethod
    @pytest.mark.usefixtures('default-snippets', 'import-netcat')
    def test_cli_search_snippet_033(snippy, capsys):
        """Search snippets with ``stag`` option.

        Search snippets from tag fields of specific group. The match must not
        be made from other than defined group. In this case the list all must
        print the content of defined group.
        """

        output = (
            '1. Remove all docker containers with volumes @docker [54e41e9b52a02b63]',
            '',
            '   $ docker rm --volumes $(docker ps --all --quiet)',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '',
            '2. Remove docker image with force @docker [53908d68425c61dc]',
            '',
            '   $ docker rm --force redis',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '   > https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes',
            '',
            'OK',
            ''
        )
        cause = snippy.run(['snippy', 'search', '--stag', 'docker-ce,moby', '--sgrp', 'docker', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    @staticmethod
    @pytest.mark.usefixtures('default-snippets', 'import-netcat')
    def test_cli_search_snippet_034(snippy, capsys):
        """Search snippets with ``stag`` option.

        Try to search snippets based on tag fields of specific group. In this
        case there are no matches made.
        """

        output = 'NOK: cannot find content with given search criteria\n'
        cause = snippy.run(['snippy', 'search', '--stag', 'docker-ce,moby', '--sgrp', 'linux', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == 'NOK: cannot find content with given search criteria'
        assert out == output
        assert not err

    @staticmethod
    @pytest.mark.usefixtures('default-snippets')
    def test_cli_search_snippet_035(snippy, capsys):
        """Search snippets with special failures.

        Try to search snippets without defining any search criteria.
        """

        output = 'NOK: please define keyword, uuid, digest or content data as search criteria\n'
        cause = snippy.run(['snippy', 'search'])
        out, err = capsys.readouterr()
        assert cause == 'NOK: please define keyword, uuid, digest or content data as search criteria'
        assert out == output
        assert not err

    @staticmethod
    @pytest.mark.usefixtures('default-snippets')
    def test_cli_search_snippet_036(snippy, capsys):
        """Search snippets with ``filter`` option.

        Try to search snippets defining filter but not any search criteria.
        In this case the filter cannot be applied because no search criteria
        is applied.
        """

        output = 'NOK: please define keyword, uuid, digest or content data as search criteria\n'
        cause = snippy.run(['snippy', 'search', '--filter', '.*(\\$\\s.*)'])
        out, err = capsys.readouterr()
        assert cause == 'NOK: please define keyword, uuid, digest or content data as search criteria'
        assert out == output
        assert not err

    @staticmethod
    @pytest.mark.usefixtures('default-snippets', 'import-netcat')
    def test_cli_search_snippet_037(snippy, capsys):
        """Limit number of search results.

        Search snippets from tag fields of specific group which would result
        two hits without limit. With the limit option set to one, there must
        be only one search result.
        """

        output = (
            '1. Remove all docker containers with volumes @docker [54e41e9b52a02b63]',
            '',
            '   $ docker rm --volumes $(docker ps --all --quiet)',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '',
            'OK',
            ''
        )
        cause = snippy.run(['snippy', 'search', '--stag', 'docker-ce,moby', '--sgrp', 'docker', '--no-ansi', '--limit', '1'])
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    @staticmethod
    def test_cli_search_snippet_038(snippy, capsys):
        """Print snippet with aligned comments.

        Print snippet which has commends on every command. In this case the
        comments must be all aligned evenly after each command.
        """

        Content.store({
            'category': Const.SNIPPET,
            'data': [
                'tar cvfz mytar.tar.gz --exclude="mytar.tar.gz" ./  #  Compress folder excluding the tar.',
                'tar tvf mytar.tar.gz  #  List content of compressed tar.',
                'tar xfO mytar.tar.gz manifest.json  #  Cat file in compressed tar.',
                'tar -zxvf mytar.tar.gz --exclude "./mytar.tar.gz"  #  Extract and exclude one file.',
                'tar -xf mytar.tar.gz manifest.json  #  Extract only one file.'],
            'brief': 'Manipulate compressed tar files',
            'groups': ['linux'],
            'tags': ['howto', 'linux', 'tar', 'untar']
        })
        output = (
            '1. Manipulate compressed tar files @linux [61014e2d1ec56a9a]',
            '',
            '   $ tar cvfz mytar.tar.gz --exclude="mytar.tar.gz" ./  #  Compress folder excluding the tar.',
            '   $ tar tvf mytar.tar.gz                               #  List content of compressed tar.',
            '   $ tar xfO mytar.tar.gz manifest.json                 #  Cat file in compressed tar.',
            '   $ tar -zxvf mytar.tar.gz --exclude "./mytar.tar.gz"  #  Extract and exclude one file.',
            '   $ tar -xf mytar.tar.gz manifest.json                 #  Extract only one file.',
            '',
            '   # howto,linux,tar,untar',
            '',
            'OK',
            ''
        )
        cause = snippy.run(['snippy', 'search', '--stag', 'tar', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    @staticmethod
    def test_cli_search_snippet_039(snippy, capsys):
        """Print snippet with aligned comments.

        Print snippet which do not have comments after every command. In
        this case the comments must be aligned only based on commands that
        have comments.
        """

        Content.store({
            'category': Const.SNIPPET,
            'data': [
                'tar cvfz mytar.tar.gz --exclude="mytar.tar.gz" ./',
                'tar tvf mytar.tar.gz  #  List content of compressed tar.',
                'tar xfO mytar.tar.gz manifest.json  #  Cat file in compressed tar.',
                'tar -zxvf mytar.tar.gz --exclude "./mytar.tar.gz"',
                'tar -xf mytar.tar.gz manifest.json'],
            'brief': 'Manipulate compressed tar files',
            'groups': ['linux'],
            'tags': ['howto', 'linux', 'tar', 'untar']
        })
        output = (
            '1. Manipulate compressed tar files @linux [c1b9987e1dbfd51d]',
            '',
            '   $ tar cvfz mytar.tar.gz --exclude="mytar.tar.gz" ./',
            '   $ tar tvf mytar.tar.gz                #  List content of compressed tar.',
            '   $ tar xfO mytar.tar.gz manifest.json  #  Cat file in compressed tar.',
            '   $ tar -zxvf mytar.tar.gz --exclude "./mytar.tar.gz"',
            '   $ tar -xf mytar.tar.gz manifest.json',
            '',
            '   # howto,linux,tar,untar',
            '',
            'OK',
            ''
        )
        cause = snippy.run(['snippy', 'search', '--stag', 'tar', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    @staticmethod
    def test_cli_search_snippet_040(snippy, capsys):
        """Print snippet with aligned comments.

        Print snippet with comments that must not trigger comment aligment
        because there is only one comment after one command. This verifies
        also that only one comment is aligned correctly.

        In this case, a colored print is used.
        """

        Content.store({
            'category': Const.SNIPPET,
            'data': [
                'tar cvfz mytar.tar.gz --exclude="mytar.tar.gz" ./',
                'tar tvf mytar.tar.gz # List content of compressed tar.',
                'tar xfO mytar.tar.gz manifest.json# Cat file in compressed tar.',
                't',
                '',
                'tar -xf mytar.tar.gz manifest.json'],
            'brief': 'Manipulate compressed tar files',
            'groups': ['linux'],
            'tags': ['howto', 'linux', 'tar', 'untar']
        })
        output = (
            '1. Manipulate compressed tar files @linux [0897e0e180afa68f]',
            '',
            '   $ tar cvfz mytar.tar.gz --exclude="mytar.tar.gz" ./',
            '   $ tar tvf mytar.tar.gz  #  List content of compressed tar.',
            '   $ tar xfO mytar.tar.gz manifest.json# Cat file in compressed tar.',
            '   $ t',
            '   $ ',
            '   $ tar -xf mytar.tar.gz manifest.json',
            '',
            '   # howto,linux,tar,untar',
            '',
            'OK',
            ''
        )
        cause = snippy.run(['snippy', 'search', '--stag', 'tar'])
        out, err = capsys.readouterr()
        out = Helper.remove_ansi(out)
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    @staticmethod
    @pytest.mark.usefixtures('import-interp')
    def test_cli_search_snippet_041(snippy, capsys):
        """Search snippets with special format and characters.

        Search a snippet which content data has a ASCII string that is a
        newline. This string in the command must not be interpolated to a
        newline but it must be printed "as is".
        """

        output = (
            '1. Perform recursive git status on subdirectories @git [9e1949c2810df2a5]',
            '',
            r'''   $ find . -type d -name '.git' | while read dir ; do sh -c "cd $dir/../ && echo -e \"\nGIT STATUS IN ${dir//\.git/}\" && git status -s" ; done''',  # noqa pylint: disable=line-too-long
            '',
            '   # git,status',
            '   > https://gist.github.com/tafkey/664266c00387c98631b3',
            '',
            'OK',
            ''
        )
        cause = snippy.run(['snippy', 'search', '--sall', 'git', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    @staticmethod
    @pytest.mark.usefixtures('default-snippets')
    def test_cli_search_snippet_042(snippy, capsys):
        """Search snippets with special format and characters.

        Search snippets and print the results in Markdown format.
        """

        output = (
            '# Remove all docker containers with volumes @docker',
            '',
            '> ',
            '',
            '> [1] https://docs.docker.com/engine/reference/commandline/rm/',
            '',
            '`$ docker rm --volumes $(docker ps --all --quiet)`',
            '',
            '## Meta',
            '',
            '> category : snippet  ',
            'created  : 2017-10-14T19:56:31.000001+00:00  ',
            'digest   : 54e41e9b52a02b631b5c65a6a053fcbabc77ccd42b02c64fdfbc76efdb18e319  ',
            'filename :  ',
            'name     :  ',
            'source   :  ',
            'tags     : cleanup,container,docker,docker-ce,moby  ',
            'updated  : 2017-10-14T19:56:31.000001+00:00  ',
            'uuid     : 11cd5827-b6ef-4067-b5ac-3ceac07dde9f  ',
            'versions :  ',
            '',
            '---',
            '',
            '# Remove docker image with force @docker',
            '',
            '> ',
            '',
            '> [1] https://docs.docker.com/engine/reference/commandline/rm/  ',
            '[2] https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes',
            '',
            '`$ docker rm --force redis`',
            '',
            '## Meta',
            '',
            '> category : snippet  ',
            'created  : 2017-10-14T19:56:31.000001+00:00  ',
            'digest   : 53908d68425c61dc310c9ce49d530bd858c5be197990491ca20dbe888e6deac5  ',
            'filename :  ',
            'name     :  ',
            'source   :  ',
            'tags     : cleanup,container,docker,docker-ce,moby  ',
            'updated  : 2017-10-14T19:56:31.000001+00:00  ',
            'uuid     : 12cd5827-b6ef-4067-b5ac-3ceac07dde9f  ',
            'versions :  ',
            '',
            'OK',
            ''
        )
        cause = snippy.run(['snippy', 'search', '--sall', '.', '--format', 'mkdn'])
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    @staticmethod
    @pytest.mark.usefixtures('default-snippets')
    def test_cli_search_snippet_043(snippy, capsys):
        """Search snippets with search shortcut.

        Search snippets with only the search operation followed by search
        keywords.
        """

        output = (
            '1. Remove docker image with force @docker [53908d68425c61dc]',
            '',
            '   $ docker rm --force redis',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '   > https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes',
            '',
            'OK',
            ''
        )
        cause = snippy.run(['snippy', 'search', 'redis', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    @staticmethod
    @pytest.mark.usefixtures('default-snippets')
    def test_cli_search_snippet_044(snippy, capsys):
        """Search snippets with search shortcut.

        Search snippets with the search shortcut. In this case the search
        matches to two resources but the ``--limit`` option limits printed
        resources to one.
        """

        output = (
            '1. Remove all docker containers with volumes @docker [54e41e9b52a02b63]',
            '',
            '   $ docker rm --volumes $(docker ps --all --quiet)',
            '',
            '   # cleanup,container,docker,docker-ce,moby',
            '   > https://docs.docker.com/engine/reference/commandline/rm/',
            '',
            'OK',
            ''
        )
        cause = snippy.run(['snippy', 'search', '.', '--limit', '1', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    @staticmethod
    @pytest.mark.usefixtures('default-snippets', 'import-netcat')
    def test_cli_search_snippet_045(snippy, capsys):
        """Search snippets with search shortcut.

        Search snippets with the search shortcut. In this case the search all
        is used but the ``--sgrp`` limits the search to a category that has
        only one resource.
        """

        output = (
            '1. Test if specific port is open @linux [f3fd167c64b6f97e]',
            '',
            '   $ nc -v 10.183.19.189 443',
            '   $ nmap 10.183.19.189',
            '',
            '   # linux,netcat,networking,port',
            '   > https://www.commandlinux.com/man-page/man1/nc.1.html',
            '',
            'OK',
            ''
        )
        cause = snippy.run(['snippy', 'search', '.', '--sgrp', 'linux', '--no-ansi'])
        out, err = capsys.readouterr()
        assert cause == Cause.ALL_OK
        assert out == Const.NEWLINE.join(output)
        assert not err

    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        Content.delete()
