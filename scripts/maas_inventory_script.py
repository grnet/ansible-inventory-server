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

import json
import os
import sys
from urllib.request import urlopen, Request


DEFAULT_SUBNET = '10.0.0.0/16'


def main():
    try:
        # For no arguments, or just --list, just output the inventory.
        # This allows this script to be used as a dynamic inventory plugin.
        if not sys.argv[1:] or sys.argv[1] == '--list':
            # Build an Ansible inventory file from MaaS environment status
            params = {
                'maas': {
                    'url': os.getenv('MAAS_URL'),
                    'apikey': os.getenv('MAAS_APIKEY'),
                },
                'subnet': os.getenv('SUBNET', DEFAULT_SUBNET)
            }

            req = Request('{}/maas/inventory'.format(os.getenv('AIS_URL')),
                          method='GET')
            res = urlopen(req, data=json.dumps(params).encode()).read()

            inventory = json.loads(res.decode('utf-8'))
            print(json.dumps(inventory, indent=4))
            sys.exit(0)

        elif sys.argv[1] == '--host':
            # hostvars not supported yet, exit quickly to minimize the lookup
            # cost
            print(json.dumps({}))
            sys.exit(0)

        else:
            raise Exception(
                'Unknown argument. Please use either --list or --host')
    except Exception as e:
        print('Error: {}'.format(str(e)), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
