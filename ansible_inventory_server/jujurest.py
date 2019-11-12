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

from juju.model import Model

from ansible_inventory_server.utils import ApiRequestHandler
from ansible_inventory_server import settings


async def get_juju_model(parameters):
    """Returns a new juju.model.Model(), using the specified connection
    parameters. Returns None on error"""
    cacert = parameters.get('juju', {}).get('cacert')
    if cacert is None:
        with open(settings.CACERT_PATH, 'r') as fin:
            cacert = fin.read()

    model = Model()
    try:
        await model.connect(
            cacert=cacert,
            username=parameters['juju']['username'],
            password=parameters['juju']['password'],
            uuid=parameters.get('juju', {}).get(
                'model_uuid', settings.MODEL_UUID),
            endpoint=parameters.get('juju', {}).get(
                'endpoint', settings.JUJU_ENDPOINT)
        )
        return model
    except:
        return None


async def get_juju_status(parameters):
    """Connects to a Juju model and returns status"""
    model = await get_juju_model(parameters)
    if model is None:
        return None

    status = await model.get_status(parameters.get('juju', {}).get('filters'))
    return status


def juju_filter_machine_info(machine, data):
    """Keeps only useful machine information"""
    return {
        'id': machine,
        'name': data.get('display-name') or data.get('instance-id'),
        'instance_id': data.get('instance-id'),
        'ip_addresses': data.get('ip-addresses', []),
        'apps': [],
        'subordinates': [],
        'containers': [],
        'parent': None
    }


def get_juju_machines(status):
    """Get dictionary of Juju machines."""
    result = {}
    for machine, machine_data in status.machines.items():
        result[machine] = juju_filter_machine_info(
            machine, machine_data)

        containers = machine_data.get('containers', {})
        for lxd, lxd_data in containers.items():
            result[lxd] = juju_filter_machine_info(
                lxd, lxd_data)

            result[lxd]['parent'] = machine
            result[machine]['containers'].append(lxd)

    # update list of Juju apps and subordinate units
    for app, app_data in status.applications.items():
        for unit, unit_data in (app_data.get('units') or {}).items():
            if not unit_data['machine']:
                continue

            result[unit_data['machine']]['apps'].append(app)

            for sub, sub_data in (unit_data.get('subordinates') or {}).items():
                result[unit_data['machine']]['subordinates'].append(sub)

    return result


class JujuRequestHandler(ApiRequestHandler):
    """Extends ApiRequestHandler, adding common logic for all Juju
    related endpoints."""

    async def get(self):
        status = await get_juju_status(self.json)
        if not status:
            return self.api_error(400)

        response = self.create_response(status)
        self.write(json.dumps(response, indent=4))

    def create_response(self, status):
        """endpoints will implement this"""
        raise NotImplementedError()


class JujuInventoryHandler(JujuRequestHandler):
    def create_response(self, status):
        machines = get_juju_machines(status)

        result = {
            '_meta': {'hostvars': {}},
            status.model.name: {'children': []}
        }

        for machine, machine_data in machines.items():
            address = machine_data['ip_addresses'][0]

            for app in machine_data['apps']:
                if app not in result:
                    result[app] = {'hosts': []}
                    result[status.model.name]['children'].append(app)

                result[app]['hosts'].append(address)
                result['_meta']['hostvars'][address] = {}

        return result


class JujuHostsHandler(JujuRequestHandler):
    def create_response(self, status):
        return get_juju_machines(status)


class JujuNrpeMachinesHandler(JujuRequestHandler):
    def create_response(self, status):
        # get all juju machines
        all_machines = get_juju_machines(status)

        # for units with a `nrpe-external-master` relation, machine has Juju
        # managed NRPE
        juju_nrpe_machines = []
        for machine, machine_data in all_machines.items():
            for app in machine_data['apps']:
                app_data = status.applications.get(app, {})

                if 'nrpe-external-master' in (app_data.get('relations') or []):
                    juju_nrpe_machines.append(machine_data['ip_addresses'][0])
                    break

        return juju_nrpe_machines


class JujuStatusHandler(JujuRequestHandler):
    def create_response(self, status):
        return json.loads(status.to_json())
