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

import ansible_inventory_server.jujurest as juju
import ansible_inventory_server.maasrest as maas
from ansible_inventory_server.utils import ApiRequestHandler


def _has_cluster_relations(relations):
    return any(x in relations for x in [
        'ha', 'cluster', 'peer', 'compute-peer', 'replica-set'])


class AisInventoryHandler(ApiRequestHandler):
    async def get(self):
        self.machines = []
        if not await self.scrape_juju() or not await self.scrape_maas():
            self.api_error(400)
            return

        self.json_response(self.machines)

    def _new_machine(self, data):
        machine = dict(data)
        self.machines.append(machine)

        return machine

    def get_machine(self, data: dict):
        for m in self.machines:
            matches = all(m.get(key) == value for key, value in data.items())
            if matches:
                return m

        return self._new_machine(data)

    async def scrape_juju(self):
        juju_status = await juju.get_juju_status(self.json)
        if not juju_status:
            return False

        self.machines = list(
            juju.get_juju_machines(juju_status, self.json).values())

        return True

    async def scrape_maas(self):
        session = await maas.get_maas_session(self.json)
        if session is None:
            return False

        machines = await maas.get_maas_machines(session)

        for maas_machine in machines:
            m = self.get_machine({'instance_id': maas_machine['system_id']})
            m.update(maas.filter_maas_machine_info(maas_machine, self.json))

        return True
