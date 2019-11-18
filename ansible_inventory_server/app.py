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

import logging

import tornado.web
import tornado.ioloop

from ansible_inventory_server import jujurest
from ansible_inventory_server import maasrest


def make_app():
    logging.basicConfig(level='INFO')
    return tornado.web.Application([
        (r'/juju/inventory', jujurest.JujuInventoryHandler),
        (r'/juju/status', jujurest.JujuStatusHandler),
        (r'/juju/machines', jujurest.JujuMachinesHandler),
        (r'/maas/machines', maasrest.MaasMachinesHandler),
        (r'/maas/inventory', maasrest.MaasInventoryHandler)
    ])


def main():
    app = make_app()
    app.listen(5000)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()
