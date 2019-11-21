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

from collections import defaultdict

from maas.client.bones import SessionAPI

from ansible_inventory_server.utils import (ApiRequestHandler,
                                            filter_ip_addresses)


def filter_maas_machine_info(machine, kwargs):
    """Keeps only useful machine information"""
    ip_addresses = filter_ip_addresses(machine['ip_addresses'], kwargs)

    return {
        'system_id': machine['system_id'],
        'fqdn': machine['fqdn'],
        'hostname': machine['hostname'],
        'ip_addresses': ip_addresses,
        'tags': machine['tag_names']
    }


async def get_maas_session(parameters):
    """Returns a new MaaS session, or None if credentials are invalid"""
    try:
        maas_url = parameters['maas']['url']
        maas_apikey = parameters['maas']['apikey']

        _, session = await SessionAPI.connect(maas_url, apikey=maas_apikey)

        return session
    except:
        return None


class MaasRequestHandler(ApiRequestHandler):
    """Extends ApiRequestHandler, adding common logic for all MaaS
    related endpoints."""

    machines = None

    async def get(self):
        session = await get_maas_session(self.json)
        if session is None:
            return self.api_error(400)

        response = await self.create_response(session)
        self.json_response(response)

    async def create_response(self, session):
        """endpoints will implement this"""
        raise NotImplementedError()

    async def get_machines(self, session):
        """Returns list of MaaS machines"""
        if MaasRequestHandler.machines is None:
            MaasRequestHandler.machines = await session.Machines.read()

        return MaasRequestHandler.machines


class MaasMachinesHandler(MaasRequestHandler):
    async def create_response(self, session):
        machines = await self.get_machines(session)
        result = []
        for machine in machines:
            result.append(filter_maas_machine_info(machine, self.json))

        return result


class MaasInventoryHandler(MaasRequestHandler):
    async def create_response(self, session):
        result = defaultdict(lambda: [])
        for m in await self.get_machines(session):
            ip_addresses = filter_ip_addresses(m['ip_addresses'], self.json)

            for t in m['tag_names']:
                result[t].append(ip_addresses[0])

        return result
