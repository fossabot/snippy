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

"""test_api_delete_references: Test DELETE references API."""

from falcon import testing
import falcon
import pytest

from tests.testlib.content import Content
from tests.testlib.reference import Reference

pytest.importorskip('gunicorn')


class TestApiDeleteReference(object):
    """Test DELETE references API."""

    @staticmethod
    @pytest.mark.usefixtures('default-references', 'import-pytest')
    def test_api_delete_reference_001(server):
        """Delete reference with digest.

        Send DELETE /references/{id} to remove a reference. The ``digest``
        matches to one resource that is deleted.
        """

        content = {
            'data': [
                Reference.GITLOG,
                Reference.REGEXP
            ]
        }
        expect_headers = {}
        result = testing.TestClient(server.server.api).simulate_delete(
            path='/snippy/api/app/v1/references/1f9d9496005736ef',
            headers={'accept': 'application/json'})
        assert result.status == falcon.HTTP_204
        assert result.headers == expect_headers
        assert not result.text
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('default-references', 'import-pytest', 'caller')
    def test_api_delete_reference_002(server):
        """Try to delete reference.

        Try to send DELETE /reference with resource URI that does not exist.
        """

        content = {
            'data': [
                Reference.PYTEST,
                Reference.GITLOG,
                Reference.REGEXP
            ]
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '367'
        }
        expect_body = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '404',
                'statusString': '404 Not Found',
                'module': 'snippy.testing.testing:123',
                'title': 'cannot find content with content identity: beefbeef'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_delete(
            path='/snippy/api/app/v1/references/beefbeef',
            headers={'accept': 'application/json'})
        assert result.status == falcon.HTTP_404
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('default-references', 'caller')
    def test_api_delete_reference_003(server):
        """Try to delete reference.

        Try to send DELETE /references without digest identifying deleted
        reource.
        """

        content = {
            'data': [
                Reference.GITLOG,
                Reference.REGEXP
            ]
        }
        expect_headers = {
            'content-type': 'application/vnd.api+json; charset=UTF-8',
            'content-length': '365'
        }
        expect_body = {
            'meta': Content.get_api_meta(),
            'errors': [{
                'status': '404',
                'statusString': '404 Not Found',
                'module': 'snippy.testing.testing:123',
                'title': 'cannot delete content without identified resource'
            }]
        }
        result = testing.TestClient(server.server.api).simulate_delete(
            path='/snippy/api/app/v1/references',
            headers={'accept': 'application/vnd.api+json'})
        assert result.status == falcon.HTTP_404
        assert result.headers == expect_headers
        Content.assert_restapi(result.json, expect_body)
        Content.assert_storage(content)

    @staticmethod
    @pytest.mark.usefixtures('default-references', 'import-pytest')
    def test_api_delete_reference_004(server):
        """Delete reference with UUID.

        Send DELETE /references/{id} to remove one resource. The UUID matches
        to one reference that is deleted.
        """

        content = {
            'data': [
                Reference.PYTEST,
                Reference.REGEXP
            ]
        }
        expect_headers = {}
        result = testing.TestClient(server.server.api).simulate_delete(
            path='/snippy/api/app/v1/references/' + Reference.GITLOG_UUID,
            headers={'accept': 'application/json'})
        assert result.status == falcon.HTTP_204
        assert result.headers == expect_headers
        assert not result.text
        Content.assert_storage(content)

    @classmethod
    def teardown_class(cls):
        """Teardown class."""

        Content.delete()
