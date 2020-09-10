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

import asyncio
import json

from juju.model import Model
from juju.errors import JujuError

from ansible_inventory_server.utils import (ApiRequestHandler,
                                            filter_ip_addresses)


async def get_juju_model(parameters):
    """Returns a new juju.model.Model(), using the specified connection
    parameters. Returns None on error"""

    model = Model()
    try:
        await model.connect(
            cacert=parameters['juju']['cacert'],
            username=parameters['juju']['username'],
            password=parameters['juju']['password'],
            uuid=parameters['juju']['model_uuid'],
            endpoint=parameters['juju']['endpoint'],
        )
    except (JujuError, KeyError):
        pass

    return model


async def get_juju_status(parameters):
    """Connects to a Juju model and returns status"""

    model = await get_juju_model(parameters)
    if not model.is_connected():
        return None

    status = await model.get_status(parameters.get('juju', {}).get('filters'))
    asyncio.ensure_future(model.disconnect())
    return status


def juju_filter_ip_addresses(interfaces, kwargs):
    """Filters IP addresses from Juju network interfaces, optionally with
    interface name and subnet."""

    ip_addresses = []

    try:
        interface_filter = kwargs.get('interface')
        for interface, interface_data in interfaces.items():
            if interface_filter and interface != interface_filter:
                continue

            ip_addresses.extend(interface_data.get('ip-addresses') or [])

    except (ValueError, AttributeError):
        pass

    return filter_ip_addresses(ip_addresses, kwargs)


def juju_filter_machine_info(machine, data, kwargs):
    """Keeps only useful machine information"""

    return {
        'id': machine,
        'name': data.get('display-name') or data.get('instance-id'),
        'instance_id': data.get('instance-id'),
        'ip_addresses': juju_filter_ip_addresses(
            data.get('network-interfaces') or {}, kwargs),
        'apps': [],
        'subordinates': [],
        'containers': [],
        'parent': None
    }


def get_juju_machines(status, kwargs):
    """Gets dictionary of Juju machines."""

    result = {}
    for machine, machine_data in status.machines.items():
        result[machine] = juju_filter_machine_info(
            machine, machine_data, kwargs)

        containers = machine_data.get('containers', {})
        for lxd, lxd_data in containers.items():
            result[lxd] = juju_filter_machine_info(lxd, lxd_data, kwargs)

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
        self.json_response(response)

    def create_response(self, status):
        """endpoints will implement this"""
        raise NotImplementedError()


class JujuInventoryHandler(JujuRequestHandler):
    def create_response(self, status):
        machines = get_juju_machines(status, self.json)

        result = {
            '_meta': {'hostvars': {}},
            status.model.name: {'children': []}
        }

        for machine, machine_data in machines.items():
            if not machine_data['ip_addresses']:
                continue

            name = machine_data['name']
            for app in machine_data['apps']:
                if app not in result:
                    result[app] = {'hosts': []}
                    result[status.model.name]['children'].append(app)

                result[app]['hosts'].append(name)
                result['_meta']['hostvars'][name] = {
                    'ansible_host': machine_data['ip_addresses'][0],
                }

        return result


class JujuMachinesHandler(JujuRequestHandler):
    def create_response(self, status):
        return get_juju_machines(status, self.json)


class JujuStatusHandler(JujuRequestHandler):
    def create_response(self, status):
        return json.loads(status.to_json())
