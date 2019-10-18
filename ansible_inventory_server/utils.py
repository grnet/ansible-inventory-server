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
