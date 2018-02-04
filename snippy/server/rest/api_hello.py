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

"""api_hello.py - JSON REST API hello."""

import json
import falcon
from snippy.metadata import __version__


class ApiHello(object):  # pylint: disable=too-few-public-methods
    """Hello API."""

    @staticmethod
    def on_get(_, response):
        """Get Hello!"""

        hello = {'snippy': __version__}
        response.content_type = falcon.MEDIA_JSON
        response.body = json.dumps(hello)
        response.status = falcon.HTTP_200