#!/usr/bin/env python3.6

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

import base64
import json
import os
import sys
import urllib.request

inventory_url = 'http://hostname:5000/maas/inventory'


def main():
    try:
        # For no arguments, or just --list, just output the inventory.
        # This allows this script to be used as a dynamic inventory plugin.
        if not sys.argv[1:] or sys.argv[1] == '--list':
            # Get API key from AWX credentials
            apikey = os.getenv('MAAS_APIKEY')

            req = urllib.request.Request(inventory_url)
            credentials = ':{0}'.format(apikey)
            encoded_credentials = base64.b64encode(credentials.encode('ascii'))
            req.add_header(
                'Authorization',
                'Basic {}'.format(encoded_credentials.decode('ascii')))
            res = urllib.request.urlopen(req).read()

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
