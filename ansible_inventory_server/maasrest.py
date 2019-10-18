from collections import defaultdict
import json

from maas.client import connect

from ansible_inventory_server.utils import ApiRequestHandler
from ansible_inventory_server import settings


class MaasRequestHandler(ApiRequestHandler):
    """extend the base RequestHandler class to add code shared
    by our endpoints. Endpoints should extend this class and
    implement the create_response() method as needed."""

    async def get(self):
        credentials = self.get_basic_auth(self.request.headers)
        if credentials is None:
            return self.write('{}')

        client = await connect(settings.MAAS_ENDPOINT,
                               apikey=credentials.password)
        self.write(json.dumps(await self.create_response(client), indent=4))

    async def create_response(self, client):
        """endpoints will implement this"""
        raise NotImplementedError()


class MaasMachinesHandler(MaasRequestHandler):
    async def create_response(self, client):
        return [{
            'fqdn': m.fqdn,
            'hostname': m.hostname,
            'ip_addresses': m.ip_addresses,
            'tags': [t.name for t in m.tags],
        } for m in await client.machines.list()]


class MaasInventoryHandler(MaasRequestHandler):
    async def create_response(self, client):
        result = defaultdict(lambda: [])
        for m in await client.machines.list():
            for t in m.tags:
                result[t.name].append(m.fqdn)

        return result
