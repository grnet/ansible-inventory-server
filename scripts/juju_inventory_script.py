#!/usr/bin/env python3

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

import argparse
import json
import os
from urllib.request import urlopen, Request


def juju_inventory(args):
    """Fetches the Juju inventory from the GRNet Ansible Inventory Server
    and prints it to stdout"""

    params = {
        'juju': {
            'username': args.juju_username,
            'password': args.juju_password,
            'model_uuid': args.juju_model_uuid,
            'cacert': args.juju_cacert.replace(r'\n', '\n'),
            'endpoint': args.juju_endpoint,
        }
    }

    url = '{}/juju/inventory'.format(args.server)
    res = urlopen(
        Request(url, method='GET'), data=json.dumps(params).encode()).read()
    print(res.decode())


def main():
    parser = argparse.ArgumentParser(
        description='Script to retrieve Juju Ansible inventory')
    parser.add_argument('--server', required=False,
                        default=os.getenv('GRNET_AIS_URL'))
    parser.add_argument('--juju-username', required=False,
                        default=os.getenv('JUJU_USERNAME'))
    parser.add_argument('--juju-password', required=False,
                        default=os.getenv('JUJU_PASSWORD'))
    parser.add_argument('--juju-endpoint', required=False,
                        default=os.getenv('JUJU_ENDPOINT'))
    parser.add_argument('--juju-model-uuid', required=False,
                        default=os.getenv('JUJU_MODEL_UUID'))
    parser.add_argument('--juju-cacert', required=False,
                        default=os.getenv('JUJU_CACERT'))
    parser.add_argument('--response-params', required=False,
                        default='{"indent": 4}')

    juju_inventory(parser.parse_args())


if __name__ == '__main__':
    main()
