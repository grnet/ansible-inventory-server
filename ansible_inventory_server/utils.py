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

import json

import tornado.web


class ApiRequestHandler(tornado.web.RequestHandler):
    """Common logic for all endpoint handlers"""

    @property
    def json(self):
        """Parses request body as JSON and returns as dictionary."""
        if not hasattr(self, '_json'):
            try:
                self._json = json.loads(self.request.body)
            except json.JSONDecodeError:
                self._json = {}

        return self._json

    def api_error(self, status_code):
        """Returns error response with specified status code"""
        self.set_status(status_code)
        self.json_response({'status': status_code})

    def json_response(self, data):
        """Sends :param data: as JSON response"""
        kwargs = self.json.get('response', {})
        try:
            response = json.dumps(data, **kwargs)
        except (ValueError, TypeError):
            response = json.dumps(data)

        self.write(response)
