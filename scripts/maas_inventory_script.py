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


def maas_inventory(args):
    """Fetches the MaaS inventory from the GRNet Ansible Inventory Server
    and prints it to stdout"""

    params = {
        'maas': {
            'url': args.maas_url,
            'apikey': args.maas_apikey,
        }
    }

    url = '{}/maas/inventory'.format(args.server)
    res = urlopen(
        Request(url, method='GET'), data=json.dumps(params).encode()).read()
    print(res.decode())


def main():
    parser = argparse.ArgumentParser(
        description='Script to retrieve MaaS Ansible inventory')
    parser.add_argument('--server', required=False,
                        default=os.getenv('GRNET_AIS_URL'))
    parser.add_argument('--maas-url', required=False,
                        default=os.getenv('MAAS_URL'))
    parser.add_argument('--maas-apikey', required=False,
                        default=os.getenv('MAAS_APIKEY'))
    parser.add_argument('--response-params', required=False,
                        default='{"indent": 4}')

    maas_inventory(parser.parse_args())


if __name__ == '__main__':
    main()
