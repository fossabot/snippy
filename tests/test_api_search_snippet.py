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

"""test_api_search_snippet: Test GET /snippy/api/snippets API."""

from falcon import testing
import falcon
import pytest

from tests.testlib.content import Content
from tests.testlib.snippet_helper import SnippetHelper as Snippet
from tests.testlib.sqlitedb_helper import SqliteDbHelper as Database

pytest.importorskip('gunicorn')


class TestApiSearchSnippet(object):  # pylint: disable=too-many-public-methods
    """Test GET /snippy/api/snippets API."""

    @pytest.mark.usefixtures('default-snippets')
    def test_api_search_snippet_001(self, server):
        """Search snippets with GET.

        Call GET /v1/snippets and search keywords from all fields. The search
        query matches to two snippets and both of them are returned. The
        search is sorted based on one field. The limit defined in the search
        query is not exceeded.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '1381'
        }
        result_json = {
            'meta': {
                'count': 2,
                'limit': 20,
                'offset': 0,
                'total': 2
            },
            'data': [{
                'type': 'snippet',
                'id': '54e41e9b52a02b631b5c65a6a053fcbabc77ccd42b02c64fdfbc76efdb18e319',
                'attributes': Snippet.DEFAULTS[Snippet.REMOVE]
            }, {
                'type': 'snippet',
                'id': '53908d68425c61dc310c9ce49d530bd858c5be197990491ca20dbe888e6deac5',
                'attributes': Snippet.DEFAULTS[Snippet.FORCED]
            }]
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/snippets',
            headers={'accept': 'application/vnd.api+json'},
            query_string='sall=docker%2Cswarm&limit=20&sort=brief')
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

    @pytest.mark.usefixtures('default-snippets', 'import-netcat', 'import-exited')
    def test_api_search_snippet_002(self, server):
        """Search snippets with GET.

        Call GET /v1/snippets and search keywords from all fields. The search
        query matches to four snippets but limit defined in search query
        results only two of them sorted by the brief field. The sorting must
        be applied before limit is applied.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '1516'
        }
        result_json = {
            'meta': {
                'count': 2,
                'limit': 2,
                'offset': 0,
                'total': 4
            },
            'data': [{
                'type': 'snippet',
                'id': '54e41e9b52a02b631b5c65a6a053fcbabc77ccd42b02c64fdfbc76efdb18e319',
                'attributes': Snippet.DEFAULTS[Snippet.REMOVE]
            }, {
                'type': 'snippet',
                'id': '49d6916b6711f13d67960905c4698236d8a66b38922b04753b99d42a310bcf73',
                'attributes': Snippet.DEFAULTS[Snippet.EXITED]
            }]
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/snippets',
            headers={'accept': 'application/json'},
            query_string='sall=docker%2Cnmap&limit=2&sort=brief')
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

    @pytest.mark.usefixtures('default-snippets')
    def test_api_search_snippet_003(self, server):
        """Search snippets with GET.

        Call GET /v1/snippets and search keywords from all fields. The search
        query matches to two snippets but only one of them is returned
        because the limit parameter was set to one. In this case the sort is
        descending and the last match must be returned. The resulting fields
        are limited only to brief and category.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '246'
        }
        result_json = {
            'meta': {
                'count': 1,
                'limit': 1,
                'offset': 0,
                'total': 2
            },
            'data': [{
                'type': 'snippet',
                'id': '53908d68425c61dc310c9ce49d530bd858c5be197990491ca20dbe888e6deac5',
                'attributes': {field: Snippet.DEFAULTS[Snippet.FORCED][field] for field in ['brief', 'category']}
            }]
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/snippets',
            headers={'accept': 'application/json'},
            query_string='sall=docker&limit=1&sort=-brief&fields=brief,category')
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

    @pytest.mark.usefixtures('default-snippets')
    def test_api_search_snippet_004(self, server):
        """Search snippets with GET.

        Call GET /v1/snippets and search keywords from all fields but return
        only two fields. This syntax that separates the sorted fields causes
        the parameter to be processed in string context which must handle
        multiple fields.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '246'
        }
        result_json = {
            'meta': {
                'count': 1,
                'limit': 1,
                'offset': 0,
                'total': 2
            },
            'data': [{
                'type': 'snippet',
                'id': '53908d68425c61dc310c9ce49d530bd858c5be197990491ca20dbe888e6deac5',
                'attributes': {field: Snippet.DEFAULTS[Snippet.FORCED][field] for field in ['brief', 'category']}
            }]
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/snippets',
            headers={'accept': 'application/json'},
            query_string='sall=docker&limit=1&sort=-brief&fields=brief%2Ccategory')
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

    @pytest.mark.usefixtures('default-snippets', 'import-netcat', 'import-exited')
    def test_api_search_snippet_005(self, server):
        """Search snippets with GET.

        Call GET /v1/snippets and search keywords from all fields. The search
        query matches to four snippets but limit defined in search query
        results only two of them sorted by the utc field in descending order.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '1484'
        }
        result_json = {
            'meta': {
                'count': 2,
                'limit': 2,
                'offset': 0,
                'total': 4
            },
            'data': [{
                'type': 'snippet',
                'id': 'f3fd167c64b6f97e5dab4a3aebef678ef7361ba8c4a5acbc1d3faff968d4402d',
                'attributes': Snippet.DEFAULTS[Snippet.NETCAT]
            }, {
                'type': 'snippet',
                'id': '49d6916b6711f13d67960905c4698236d8a66b38922b04753b99d42a310bcf73',
                'attributes': Snippet.DEFAULTS[Snippet.EXITED]
            }]
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/snippets',
            headers={'accept': 'application/json'},
            query_string='sall=docker%2Cnmap&limit=2&sort=-created,-brief')
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

    @pytest.mark.usefixtures('default-snippets', 'import-netcat', 'import-exited')
    def test_api_search_snippet_006(self, server):
        """Search snippets with GET.

        Call GET /v1/snippets and search keywords from all fields sorted with
        two fields. This syntax that separates the sorted fields causes the
        parameter to be processed in string context which must handle multiple
        fields.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '1484'
        }
        result_json = {
            'meta': {
                'count': 2,
                'limit': 2,
                'offset': 0,
                'total': 4
            },
            'data': [{
                'type': 'snippet',
                'id': 'f3fd167c64b6f97e5dab4a3aebef678ef7361ba8c4a5acbc1d3faff968d4402d',
                'attributes': Snippet.DEFAULTS[Snippet.NETCAT]
            }, {
                'type': 'snippet',
                'id': '49d6916b6711f13d67960905c4698236d8a66b38922b04753b99d42a310bcf73',
                'attributes': Snippet.DEFAULTS[Snippet.EXITED]
            }]
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/snippets',
            headers={'accept': 'application/json'},
            query_string='sall=docker%2Cnmap&limit=2&sort=-created%2C-brief')
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

    @pytest.mark.usefixtures('default-snippets', 'caller')
    def test_api_search_snippet_007(self, server):
        """Search snippets with GET.

        Try to call GET /v1/snippets with sort parameter set to field name
        that does not exist. In this case sorting must fall to default
        sorting.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '380'}
        result_json = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '400',
                'statusString': '400 Bad Request',
                'module': 'snippy.testing.testing:123',
                'title': 'sort option validation failed for non existent field=notexisting'
            }]
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/snippets',
            headers={'accept': 'application/json'},
            query_string='sall=docker%2Cswarm&limit=20&sort=notexisting')
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_400

    @pytest.mark.usefixtures('default-snippets')
    def test_api_search_snippet_008(self, server):
        """Search snippets with GET.

        Call GET /v1/snippets to return only defined fields. In this case the
        fields are defined by setting the 'fields' parameter multiple times.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '246'
        }
        result_json = {
            'meta': {
                'count': 1,
                'limit': 1,
                'offset': 0,
                'total': 2
            },
            'data': [{
                'type': 'snippet',
                'id': '53908d68425c61dc310c9ce49d530bd858c5be197990491ca20dbe888e6deac5',
                'attributes': {field: Snippet.DEFAULTS[Snippet.FORCED][field] for field in ['brief', 'category']}
            }]
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/snippets',
            headers={'accept': 'application/json'},
            query_string='sall=docker&limit=1&sort=-brief&fields=brief&fields=category')
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

    @pytest.mark.usefixtures('default-snippets', 'caller')
    def test_api_search_snippet_009(self, server):
        """Search snippets with GET.

        Try to call GET /v1/snippets with search keywords that do not result
        any matches.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '335'
        }
        result_json = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '404',
                'statusString': '404 Not Found',
                'module': 'snippy.testing.testing:123',
                'title': 'cannot find resources'
            }]
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/snippets',
            headers={'accept': 'application/json'},
            query_string='sall=notfound&limit=10&sort=-brief&fields=brief,category')
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_404

    @pytest.mark.usefixtures('default-snippets', 'caller')
    def test_api_search_snippet_010(self, server):
        """Search snippets with GET from tag fields.

        Try to call GET /v1/snippets with search tag keywords that do not
        result any matches.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '335'
        }
        result_json = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '404',
                'statusString': '404 Not Found',
                'module': 'snippy.testing.testing:123',
                'title': 'cannot find resources'
            }]
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/snippets',
            headers={'accept': 'application/json'},
            query_string='stag=notfound&limit=10&sort=-brief&fields=brief,category')
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_404

    @pytest.mark.usefixtures('default-snippets', 'caller')
    def test_api_search_snippet_011(self, server):
        """Search snippet from group fields.

        Call GET /v1/snippets with search group keywords that do not result
        any matches.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '335'
        }
        result_json = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '404',
                'statusString': '404 Not Found',
                'module': 'snippy.testing.testing:123',
                'title': 'cannot find resources'
            }]
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/snippets',
            headers={'accept': 'application/json'},
            query_string='sgrp=notfound&limit=10&sort=-brief&fields=brief,category')
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_404

    @pytest.mark.usefixtures('default-snippets')
    def test_api_search_snippet_012(self, server):
        """Search snippet with digets.

        Call GET /v1/snippets/{digest} to get explicit snippet based on
        digest. In this case the snippet is found. In this case the URI
        path contains 15 digit digest. The returned self link must contain
        the default 16 digit digest.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '782'
        }
        result_json = {
            'meta': {
                'count': 1,
                'limit': 20,
                'offset': 0,
                'total': 1
            },
            'data': {
                'type': 'snippet',
                'id': '54e41e9b52a02b631b5c65a6a053fcbabc77ccd42b02c64fdfbc76efdb18e319',
                'attributes': Snippet.DEFAULTS[Snippet.REMOVE]
            },
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/snippets/54e41e9b52a02b63'
            }
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/snippets/54e41e9b52a02b6',
            headers={'accept': 'application/json'})
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

    @pytest.mark.usefixtures('default-snippets', 'caller')
    def test_api_search_snippet_013(self, server):
        """Search snippet with digets.

        Try to call GET /v1/snippets/{digest} with digest that cannot be
        found. In this case the JSON 'null' is converted to Python None.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '334'
        }
        result_json = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '404',
                'statusString': '404 Not Found',
                'module': 'snippy.testing.testing:123',
                'title': 'cannot find resource'
            }]
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/snippets/101010101010101',
            headers={'accept': 'application/json'})
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_404

    @pytest.mark.usefixtures('default-snippets')
    def test_api_search_snippet_014(self, server):
        """Search snippet without search parameters.

        Call GET /v1/snippets without defining search parameters. In this
        case all content should be returned based on filtering parameters.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '1381'
        }
        result_json = {
            'meta': {
                'count': 2,
                'limit': 20,
                'offset': 0,
                'total': 2
            },
            'data': [{
                'type': 'snippet',
                'id': '54e41e9b52a02b631b5c65a6a053fcbabc77ccd42b02c64fdfbc76efdb18e319',
                'attributes': Snippet.DEFAULTS[Snippet.REMOVE]
            }, {
                'type': 'snippet',
                'id': '53908d68425c61dc310c9ce49d530bd858c5be197990491ca20dbe888e6deac5',
                'attributes': Snippet.DEFAULTS[Snippet.FORCED]
            }]
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/snippets',
            headers={'accept': 'application/json'},
            query_string='limit=20&sort=brief')
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

    @pytest.mark.usefixtures('default-snippets')
    def test_api_search_snippet_015(self, server):
        """Search snippet without search parameters.

        Call GET /v1/snippets without defining search parameters. In this
        case only one snippet must be returned because the limit is set to
        one. Also the sorting based on brief field causes the last snippet
        to be returned.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '759'
        }
        result_json = {
            'meta': {
                'count': 1,
                'limit': 1,
                'offset': 0,
                'total': 2
            },
            'data': [{
                'type': 'snippet',
                'id': '53908d68425c61dc310c9ce49d530bd858c5be197990491ca20dbe888e6deac5',
                'attributes': Snippet.DEFAULTS[Snippet.FORCED]
            }]
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/snippets',
            headers={'accept': 'application/json'},
            query_string='limit=1&sort=-brief')
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

    @pytest.mark.parametrize('server', [['--server', '-q']], indirect=True)
    @pytest.mark.usefixtures('default-snippets')
    def test_api_search_snippet_016(self, server):
        """Search snippets with GET.

        Call GET /v1/snippets and search keywords from all attributes. The
        search query matches to two snippets and both of them are returned.
        The response JSON is sent as pretty printed.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '2363'
        }
        result_json = {
            'meta': {
                'count': 2,
                'limit': 20,
                'offset': 0,
                'total': 2
            },
            'data': [{
                'type': 'snippet',
                'id': '54e41e9b52a02b631b5c65a6a053fcbabc77ccd42b02c64fdfbc76efdb18e319',
                'attributes': Snippet.DEFAULTS[Snippet.REMOVE]
            }, {
                'type': 'snippet',
                'id': '53908d68425c61dc310c9ce49d530bd858c5be197990491ca20dbe888e6deac5',
                'attributes': Snippet.DEFAULTS[Snippet.FORCED]
            }]
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/snippets',
            headers={'accept': 'application/vnd.api+json'},
            query_string='sall=docker%2Cswarm&limit=20&sort=brief')
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

    @pytest.mark.usefixtures('default-snippets', 'import-netcat', 'import-exited')
    def test_api_search_snippet_paginate_001(self, server):
        """Search snippets with GET.

        Call GET /v1/snippets so that pagination is applied. The offset is
        zero and limit is bigger that the amount of search results so that
        all results fit into one response. Because all results fit into the
        same response, there is no need for next and prev links and those
        must not be set.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '3147'
        }
        result_json = {
            'meta': {
                'count': 4,
                'limit': 10,
                'offset': 0,
                'total': 4
            },
            'data': [{
                'type': 'snippet',
                'id': '54e41e9b52a02b631b5c65a6a053fcbabc77ccd42b02c64fdfbc76efdb18e319',
                'attributes': Snippet.DEFAULTS[Snippet.REMOVE]
            }, {
                'type': 'snippet',
                'id': '49d6916b6711f13d67960905c4698236d8a66b38922b04753b99d42a310bcf73',
                'attributes': Snippet.DEFAULTS[Snippet.EXITED]
            }, {
                'type': 'snippet',
                'id': '53908d68425c61dc310c9ce49d530bd858c5be197990491ca20dbe888e6deac5',
                'attributes': Snippet.DEFAULTS[Snippet.FORCED]
            }, {
                'type': 'snippet',
                'id': 'f3fd167c64b6f97e5dab4a3aebef678ef7361ba8c4a5acbc1d3faff968d4402d',
                'attributes': Snippet.DEFAULTS[Snippet.NETCAT]
            }],
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/snippets?limit=10&offset=0&sall=docker%2Cnmap&sort=brief',
                'first': 'http://falconframework.org/snippy/api/app/v1/snippets?limit=10&offset=0&sall=docker%2Cnmap&sort=brief',
                'last': 'http://falconframework.org/snippy/api/app/v1/snippets?limit=10&offset=0&sall=docker%2Cnmap&sort=brief'
            }
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/snippets',
            headers={'accept': 'application/json'},
            query_string='sall=docker%2Cnmap&offset=0&limit=10&sort=brief')
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

    @pytest.mark.usefixtures('default-snippets', 'import-netcat', 'import-exited')
    def test_api_search_snippet_paginate_002(self, server):
        """Search snippets with GET.

        Call GET /v1/snippets so that pagination is applied. The offset is
        zero and limit is smaller that the amount of search results so that
        all results do not fit into one response. Because this is the first
        page, the prev link must not be set.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '1976'
        }
        result_json = {
            'meta': {
                'count': 2,
                'limit': 2,
                'offset': 0,
                'total': 4
            },
            'data': [{
                'type': 'snippet',
                'id': '54e41e9b52a02b631b5c65a6a053fcbabc77ccd42b02c64fdfbc76efdb18e319',
                'attributes': Snippet.DEFAULTS[Snippet.REMOVE]
            }, {
                'type': 'snippet',
                'id': '49d6916b6711f13d67960905c4698236d8a66b38922b04753b99d42a310bcf73',
                'attributes': Snippet.DEFAULTS[Snippet.EXITED]
            }],
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/snippets?limit=2&offset=0&sall=docker%2Cnmap&sort=brief',
                'first': 'http://falconframework.org/snippy/api/app/v1/snippets?limit=2&offset=0&sall=docker%2Cnmap&sort=brief',
                'next': 'http://falconframework.org/snippy/api/app/v1/snippets?limit=2&offset=2&sall=docker%2Cnmap&sort=brief',
                'last': 'http://falconframework.org/snippy/api/app/v1/snippets?limit=2&offset=2&sall=docker%2Cnmap&sort=brief'
            }
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/snippets',
            headers={'accept': 'application/json'},
            query_string='sall=docker%2Cnmap&offset=0&limit=2&sort=brief')
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

    @pytest.mark.usefixtures('default-snippets', 'import-netcat', 'import-exited')
    def test_api_search_snippet_paginate_003(self, server):
        """Search snippets with GET.

        Call GET /v1/snippets so that pagination is applied. The offset is
        non zero and second page is requested. The requested second page is
        the last page. Because of this, there next link must not be set.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '1808'
        }
        result_json = {
            'meta': {
                'count': 2,
                'limit': 2,
                'offset': 2,
                'total': 4
            },
            'data': [{
                'type': 'snippet',
                'id': '53908d68425c61dc310c9ce49d530bd858c5be197990491ca20dbe888e6deac5',
                'attributes': Snippet.DEFAULTS[Snippet.FORCED]
            }, {
                'type': 'snippet',
                'id': 'f3fd167c64b6f97e5dab4a3aebef678ef7361ba8c4a5acbc1d3faff968d4402d',
                'attributes': Snippet.DEFAULTS[Snippet.NETCAT]
            }],
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/snippets?limit=2&offset=2&sall=docker%2Cnmap&sort=brief',
                'first': 'http://falconframework.org/snippy/api/app/v1/snippets?limit=2&offset=0&sall=docker%2Cnmap&sort=brief',
                'prev': 'http://falconframework.org/snippy/api/app/v1/snippets?limit=2&offset=0&sall=docker%2Cnmap&sort=brief',
                'last': 'http://falconframework.org/snippy/api/app/v1/snippets?limit=2&offset=2&sall=docker%2Cnmap&sort=brief'
            }
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/snippets',
            headers={'accept': 'application/json'},
            query_string='sall=docker%2Cnmap&offset=2&limit=2&sort=brief')
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

    @pytest.mark.usefixtures('default-snippets', 'import-netcat', 'import-exited')
    def test_api_search_snippet_paginate_004(self, server):
        """Search snippets with GET.

        Call GET /v1/snippets so that pagination is applied. The offset is
        non zero and second page is requested. The requested second page is
        not the last page. In this case the last page has as many hits that
        will fit into one page (even last page). All pagination links must
        be set.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '1467'
        }
        result_json = {
            'meta': {
                'count': 1,
                'limit': 1,
                'offset': 1,
                'total': 4
            },
            'data': [{
                'type': 'snippet',
                'id': '49d6916b6711f13d67960905c4698236d8a66b38922b04753b99d42a310bcf73',
                'attributes': Snippet.DEFAULTS[Snippet.EXITED]
            }],
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/snippets?limit=1&offset=1&sall=docker%2Cnmap&sort=brief',
                'first': 'http://falconframework.org/snippy/api/app/v1/snippets?limit=1&offset=0&sall=docker%2Cnmap&sort=brief',
                'next': 'http://falconframework.org/snippy/api/app/v1/snippets?limit=1&offset=2&sall=docker%2Cnmap&sort=brief',
                'prev': 'http://falconframework.org/snippy/api/app/v1/snippets?limit=1&offset=0&sall=docker%2Cnmap&sort=brief',
                'last': 'http://falconframework.org/snippy/api/app/v1/snippets?limit=1&offset=3&sall=docker%2Cnmap&sort=brief'
            }
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/snippets',
            headers={'accept': 'application/json'},
            query_string='sall=docker%2Cnmap&offset=1&limit=1&sort=brief')
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

    @pytest.mark.usefixtures('default-snippets', 'import-netcat', 'import-exited')
    def test_api_search_snippet_paginate_005(self, server):
        """Search snippets with GET.

        Call GET /v1/snippets so that pagination is applied. The offset is
        non zero and second page is requested. The requested second page is
        not the last page. In this case the last page has less items than
        will fit to last page (uneven last page). Also the first page is
        not even and must be correctly set to zero. All pagination links must
        be set.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '2157'
        }
        result_json = {
            'meta': {
                'count': 2,
                'limit': 2,
                'offset': 1,
                'total': 4
            },
            'data': [{
                'type': 'snippet',
                'id': '49d6916b6711f13d67960905c4698236d8a66b38922b04753b99d42a310bcf73',
                'attributes': Snippet.DEFAULTS[Snippet.EXITED]
            }, {
                'type': 'snippet',
                'id': '53908d68425c61dc310c9ce49d530bd858c5be197990491ca20dbe888e6deac5',
                'attributes': Snippet.DEFAULTS[Snippet.FORCED]
            }],
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/snippets?limit=2&offset=1&sall=docker%2Cnmap&sort=brief',
                'first': 'http://falconframework.org/snippy/api/app/v1/snippets?limit=2&offset=0&sall=docker%2Cnmap&sort=brief',
                'next': 'http://falconframework.org/snippy/api/app/v1/snippets?limit=2&offset=3&sall=docker%2Cnmap&sort=brief',
                'prev': 'http://falconframework.org/snippy/api/app/v1/snippets?limit=2&offset=0&sall=docker%2Cnmap&sort=brief',
                'last': 'http://falconframework.org/snippy/api/app/v1/snippets?limit=2&offset=3&sall=docker%2Cnmap&sort=brief'
            }
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/snippets',
            headers={'accept': 'application/json'},
            query_string='sall=docker%2Cnmap&offset=1&limit=2&sort=brief')
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

    @pytest.mark.usefixtures('default-snippets', 'import-netcat', 'import-exited')
    def test_api_search_snippet_paginate_006(self, server):
        """Search snippets with GET.

        Call GET /v1/snippets so that pagination is applied. The offset is
        non zero and the last page is requested. Because original request
        was not started with  offset zero, the first and prev pages are not
        having offset based on limit. In here the offset is also exactly
        the same as total amount of hits.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '1118'
        }
        result_json = {
            'meta': {
                'count': 1,
                'limit': 2,
                'offset': 3,
                'total': 4
            },
            'data': [{
                'type': 'snippet',
                'id': 'f3fd167c64b6f97e5dab4a3aebef678ef7361ba8c4a5acbc1d3faff968d4402d',
                'attributes': Snippet.DEFAULTS[Snippet.NETCAT]
            }],
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/snippets?limit=2&offset=3&sall=docker%2Cnmap&sort=brief',
                'first': 'http://falconframework.org/snippy/api/app/v1/snippets?limit=2&offset=0&sall=docker%2Cnmap&sort=brief',
                'prev': 'http://falconframework.org/snippy/api/app/v1/snippets?limit=2&offset=1&sall=docker%2Cnmap&sort=brief',
                'last': 'http://falconframework.org/snippy/api/app/v1/snippets?limit=2&offset=3&sall=docker%2Cnmap&sort=brief'
            }
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/snippets',
            headers={'accept': 'application/json'},
            query_string='sall=docker%2Cnmap&offset=3&limit=2&sort=brief')
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

    @pytest.mark.usefixtures('default-snippets', 'import-netcat', 'import-exited', 'import-umount')
    def test_api_search_snippet_paginate_007(self, server):
        """Search snippets with GET.

        Call GET /v1/snippets so that pagination is applied. The offset and
        limit are set so that the last page contains less hits than the limit
        and the requested page is not the last or the second last page.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '2012'
        }
        result_json = {
            'meta': {
                'count': 2,
                'limit': 2,
                'offset': 0,
                'total': 5
            },
            'data': [{
                'type': 'snippet',
                'id': '54e41e9b52a02b631b5c65a6a053fcbabc77ccd42b02c64fdfbc76efdb18e319',
                'attributes': Snippet.DEFAULTS[Snippet.REMOVE]
            }, {
                'type': 'snippet',
                'id': '49d6916b6711f13d67960905c4698236d8a66b38922b04753b99d42a310bcf73',
                'attributes': Snippet.DEFAULTS[Snippet.EXITED]
            }],
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/snippets?limit=2&offset=0&sall=docker%2Cumount%2Cnmap&sort=brief',
                'next': 'http://falconframework.org/snippy/api/app/v1/snippets?limit=2&offset=2&sall=docker%2Cumount%2Cnmap&sort=brief',
                'first': 'http://falconframework.org/snippy/api/app/v1/snippets?limit=2&offset=0&sall=docker%2Cumount%2Cnmap&sort=brief',
                'last': 'http://falconframework.org/snippy/api/app/v1/snippets?limit=2&offset=4&sall=docker%2Cumount%2Cnmap&sort=brief'
            }
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/snippets',
            headers={'accept': 'application/json'},
            query_string='sall=docker%2Cumount%2Cnmap&offset=0&limit=2&sort=brief')
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

    @pytest.mark.usefixtures('default-snippets', 'import-netcat', 'import-exited', 'caller')
    def test_api_search_snippet_paginate_008(self, server):
        """Search snippets with GET.

        Try to call GET /v1/snippets with pagination offset that is the same
        as the amount of snippets stored into the database.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '335'
        }
        result_json = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '404',
                'statusString': '404 Not Found',
                'module': 'snippy.testing.testing:123',
                'title': 'cannot find resources'
            }]
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/snippets',
            headers={'accept': 'application/json'},
            query_string='sall=docker%2Cnmap&offset=4&limit=2&sort=brief')
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_404

    @pytest.mark.usefixtures('default-snippets', 'import-netcat', 'import-exited', 'caller')
    def test_api_search_snippet_paginate_009(self, server):
        """Search snippets with GET.

        Try to call GET /v1/snippets with pagination offset that is one bigger
        than the maximum amount of hits.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '335'
        }
        result_json = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '404',
                'statusString': '404 Not Found',
                'module': 'snippy.testing.testing:123',
                'title': 'cannot find resources'
            }]
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/snippets',
            headers={'accept': 'application/json'},
            query_string='sall=docker%2Cnmap&offset=10&limit=10&sort=brief')
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_404

    @pytest.mark.usefixtures('default-snippets', 'import-netcat', 'import-exited')
    def test_api_search_snippet_paginate_010(self, server):
        """Search snippets with GET.

        Call GET /v1/snippets so that pagination is applied with limit zero.
        This is a special case that returns the metadata but the data list
        is empty.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '71'
        }
        result_json = {
            'meta': {
                'count': 0,
                'limit': 0,
                'offset': 0,
                'total': 4
            },
            'data': [],
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/snippets',
            headers={'accept': 'application/json'},
            query_string='sall=docker%2Cnmap&offset=0&limit=0&sort=brief')
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

    @pytest.mark.usefixtures('default-snippets', 'import-netcat', 'import-exited', 'caller')
    def test_api_search_snippet_paginate_011(self, server):
        """Search snippets with GET.

        Try to call GET /v1/snippets with negative offset.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '359'
        }
        result_json = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '400',
                'statusString': '400 Bad Request',
                'module': 'snippy.testing.testing:123',
                'title': 'search result limit is not a positive integer: -4'
            }]
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/snippets',
            headers={'accept': 'application/json'},
            query_string='sall=docker%2Cnmap&offset=-4&limit=2&sort=brief')
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_400

    @pytest.mark.usefixtures('default-snippets', 'import-netcat', 'import-exited', 'caller')
    def test_api_search_snippet_paginate_012(self, server):
        """Search snippets with GET.

        Try to call GET /v1/snippets with negative offset and limit.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '515'
        }
        result_json = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '400',
                'statusString': '400 Bad Request',
                'module': 'snippy.testing.testing:123',
                'title': 'search result limit is not a positive integer: -2'
            }, {
                'status': '400',
                'statusString': '400 Bad Request',
                'module': 'snippy.testing.testing:123',
                'title': 'search offset is not a positive integer: -4'
            }]
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/snippets',
            headers={'accept': 'application/json'},
            query_string='sall=docker%2Cnmap&offset=-4&limit=-2&sort=brief')
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_400

    @pytest.mark.usefixtures('default-snippets', 'import-netcat', 'import-exited', 'caller')
    def test_api_search_snippet_paginate_013(self, server):
        """Search snippets with GET.

        Try to call GET /v1/snippets when offset and limit are not numbers.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '528'
        }
        result_json = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '400',
                'statusString': '400 Bad Request',
                'module': 'snippy.testing.testing:123',
                'title': 'search result limit is not a positive integer: 0xdeadbeef'
            }, {
                'status': '400',
                'statusString': '400 Bad Request',
                'module': 'snippy.testing.testing:123',
                'title': 'search offset is not a positive integer: ABCDEFG'
            }]
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/snippets',
            headers={'accept': 'application/json'},
            query_string='sall=docker%2Cnmap&offset=ABCDEFG&limit=0xdeadbeef&sort=brief')
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_400

    @pytest.mark.usefixtures('default-snippets')
    def test_api_search_snippet_field_001(self, server):
        """Get specific snippet field.

        Call GET /v1/snippets/<digest>/data for existing snippet.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '277'
        }
        result_json = {
            'data': {
                'type': 'snippet',
                'id': '54e41e9b52a02b631b5c65a6a053fcbabc77ccd42b02c64fdfbc76efdb18e319',
                'attributes': {
                    'data': Snippet.DEFAULTS[Snippet.REMOVE]['data']
                }
            },
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/snippets/54e41e9b52a02b63/data'
            }
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/snippets/54e41e9b52a02b63/data',
            headers={'accept': 'application/vnd.api+json'})
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

    @pytest.mark.usefixtures('default-snippets')
    def test_api_search_snippet_field_002(self, server):
        """Get specific snippet field.

        Call GET /v1/snippets/<digest>/brief for existing snippet. In this
        case the URI digest is only 10 octets. The returned link must contain
        16 octet digest in the link.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '272'
        }
        result_json = {
            'data': {
                'type': 'snippet',
                'id': '54e41e9b52a02b631b5c65a6a053fcbabc77ccd42b02c64fdfbc76efdb18e319',
                'attributes': {
                    'brief': Snippet.DEFAULTS[Snippet.REMOVE]['brief']
                }
            },
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/snippets/54e41e9b52a02b63/brief'
            }
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/snippets/54e41e9b52/brief',
            headers={'accept': 'application/vnd.api+json'})
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

    @pytest.mark.usefixtures('default-snippets')
    def test_api_search_snippet_field_003(self, server):
        """Get specific snippet field.

        Call GET /v1/snippets/<digest>/group for existing snippet.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '237'
        }
        result_json = {
            'data': {
                'type': 'snippet',
                'id': '54e41e9b52a02b631b5c65a6a053fcbabc77ccd42b02c64fdfbc76efdb18e319',
                'attributes': {
                    'group': Snippet.DEFAULTS[Snippet.REMOVE]['group']
                }
            },
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/snippets/54e41e9b52a02b63/group'
            }
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/snippets/54e41e9b52/group',
            headers={'accept': 'application/vnd.api+json'})
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

    @pytest.mark.usefixtures('default-snippets')
    def test_api_search_snippet_field_004(self, server):
        """Get specific snippet field.

        Call GET /v1/snippets/<digest>/tags for existing snippet.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '282'
        }
        result_json = {
            'data': {
                'type': 'snippet',
                'id': '54e41e9b52a02b631b5c65a6a053fcbabc77ccd42b02c64fdfbc76efdb18e319',
                'attributes': {
                    'tags': Snippet.DEFAULTS[Snippet.REMOVE]['tags']
                }
            },
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/snippets/54e41e9b52a02b63/tags'
            }
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/snippets/54e41e9b52/tags',
            headers={'accept': 'application/vnd.api+json'})
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

    @pytest.mark.usefixtures('default-snippets')
    def test_api_search_snippet_field_005(self, server):
        """Get specific snippet field.

        Call GET /v1/snippets/<digest>/links for existing snippet.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '289'
        }
        result_json = {
            'data': {
                'type': 'snippet',
                'id': '54e41e9b52a02b631b5c65a6a053fcbabc77ccd42b02c64fdfbc76efdb18e319',
                'attributes': {
                    'links': Snippet.DEFAULTS[Snippet.REMOVE]['links']
                }
            },
            'links': {
                'self': 'http://falconframework.org/snippy/api/app/v1/snippets/54e41e9b52a02b63/links'
            }
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/snippets/54e41e9b52/links',
            headers={'accept': 'application/vnd.api+json'})
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200


    @pytest.mark.usefixtures('default-snippets', 'caller')
    def test_api_search_snippet_field_006(self, server):
        """Get specific snippet field.

        Try to call GET /v1/snippets/<digest>/notexist for existing snippet.
        In this case the field name does not exist.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '355'
        }
        result_json = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '400',
                'statusString': '400 Bad Request',
                'module': 'snippy.testing.testing:123',
                'title': 'resource field does not exist: notexist'
            }]
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/snippets/54e41e9b52/notexist',
            headers={'accept': 'application/vnd.api+json'})
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_400

    @pytest.mark.usefixtures('default-snippets', 'caller')
    def test_api_search_snippet_field_007(self, server):
        """Get specific snippet field.

        Try to call GET /v1/snippets/0101010101/brief for non existing
        snippet with valid field.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '334'
        }
        result_json = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '404',
                'statusString': '404 Not Found',
                'module': 'snippy.testing.testing:123',
                'title': 'cannot find resources'
            }]
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/snippets/0101010101/brief',
            headers={'accept': 'application/vnd.api+json'})
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_404

    @pytest.mark.usefixtures('default-snippets')
    def test_pytest_fixtures(self, server):
        """Test pytest fixtures with pytest specific mocking.

        Call GET /v1/snippets and search keywords from all fields. The search
        query matches to two snippets and both of them are returned. The
        search is sorted based on one field. The limit defined in the search
        query is not exceeded.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '1381'
        }
        result_json = {
            'meta': {
                'count': 2,
                'limit': 20,
                'offset': 0,
                'total': 2
            },
            'data': [{
                'type': 'snippet',
                'id': '54e41e9b52a02b631b5c65a6a053fcbabc77ccd42b02c64fdfbc76efdb18e319',
                'attributes': Snippet.DEFAULTS[Snippet.REMOVE]
            }, {
                'type': 'snippet',
                'id': '53908d68425c61dc310c9ce49d530bd858c5be197990491ca20dbe888e6deac5',
                'attributes': Snippet.DEFAULTS[Snippet.FORCED]
            }]
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/snippets',
            headers={'accept': 'application/json'},
            query_string='sall=docker%2Cswarm&limit=20&sort=brief')
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

    @pytest.mark.usefixtures('import-remove', 'import-forced', 'import-exited', 'import-netcat')
    def test_pytest_fixtures2(self, server):
        """Test pytest fixtures with pytest specific mocking.

        Call GET /v1/snippets and search keywords from all fields. The search
        query matches to four snippets but limit defined in search query
        results only two of them sorted by the brief field. The sorting must
        be applied before limit is applied.
        """

        result_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '1516'
        }
        result_json = {
            'meta': {
                'count': 2,
                'limit': 2,
                'offset': 0,
                'total': 4
            },
            'data': [{
                'type': 'snippet',
                'id': '54e41e9b52a02b631b5c65a6a053fcbabc77ccd42b02c64fdfbc76efdb18e319',
                'attributes': Snippet.DEFAULTS[Snippet.REMOVE]
            }, {
                'type': 'snippet',
                'id': '49d6916b6711f13d67960905c4698236d8a66b38922b04753b99d42a310bcf73',
                'attributes': Snippet.DEFAULTS[Snippet.EXITED]
            }]
        }
        server.run()
        result = testing.TestClient(server.server.api).simulate_get(
            path='/snippy/api/app/v1/snippets',
            headers={'accept': 'application/json'},
            query_string='sall=docker%2Cnmap&limit=2&sort=brief')
        assert result.headers == result_headers
        assert Content.ordered(result.json) == Content.ordered(result_json)
        assert result.status == falcon.HTTP_200

    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        Database.delete_all_contents()
        Database.delete_storage()
