# Copyright (C) 2019  GRNET S.A.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from base64 import b64decode
from collections import namedtuple

import tornado.web


Credentials = namedtuple('Credentials', ['username', 'password'])


class ApiRequestHandler(tornado.web.RequestHandler):
    """extend the base RequestHandler class to add code shared
    by our endpoints. Endpoints should extend this class and
    implement the create_response() method as needed."""

    @staticmethod
    def get_basic_auth(headers):
        auth_header = headers.get('Authorization')
        if auth_header:
            auth_type, credentials_b64 = auth_header.split()
            if auth_type == 'Basic':
                credentials = b64decode(credentials_b64).decode().split(':', 1)
                return Credentials(credentials[0], credentials[1])

        return None
