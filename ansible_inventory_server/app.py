import logging

import tornado.web
import tornado.ioloop

from ansible_inventory_server import jujurest
from ansible_inventory_server import maasrest


def make_app():
    logging.basicConfig(level='INFO')
    return tornado.web.Application([
        (r'/juju/inventory', jujurest.JujuInventoryHandler),
        (r'/juju/hosts', jujurest.JujuHostsHandler),
        (r'/juju/status', jujurest.JujuStatusHandler),
        (r'/juju/nrpemachines', jujurest.JujuNrpeMachinesHandler),
        (r'/maas/machines', maasrest.MaasMachinesHandler),
        (r'/maas/inventory', maasrest.MaasInventoryHandler)
    ])


def main():
    app = make_app()
    app.listen(5000)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()
