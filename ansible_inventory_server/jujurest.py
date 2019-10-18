import json
from collections import defaultdict
import logging

from juju.model import Model

from ansible_inventory_server.utils import ApiRequestHandler
from ansible_inventory_server import settings


async def juju_status(credentials, model_uuid, filters=None):
    """Deserialize the current Juju status."""
    with open(settings.CACERT_PATH, 'r') as f:
        cacert = f.read()

    current_model = Model()
    try:
        await current_model.connect(
            uuid=model_uuid if model_uuid else settings.MODEL_UUID,
            endpoint=settings.CONTROLLER_ENDPOINT,
            username=credentials.username,
            password=credentials.password,
            cacert=cacert)
    except Exception as e:
        logging.exception(e)
        return {}

    status = await current_model.get_status(filters)
    return json.loads(status.to_json())


def get_machines_ips(status):
    machine_dict = {}
    machines = status.get('machines', {})
    for machine_name, machine_data in machines.items():
        machine_addresses = machine_data.get('ip-addresses', [])
        for address in machine_addresses:
            if address.startswith('10.0.'):
                machine_dict[machine_name] = address
                break

        containers = machine_data.get('containers', {})
        for container_name, container_data in containers.items():
            container_addresses = container_data.get('ip-addresses', [])
            for address in container_addresses:
                if address.startswith('10.0.'):
                    machine_dict[container_name] = address
                    break

    return machine_dict


def to_inventory_object(status, machines):
    result = {'_meta': {'hostvars': {}}}
    model_name = status.get('model', {}).get('name')
    apps = {}
    applications = status.get('applications', {})
    apps[model_name] = {'children': []}
    for application_name, application_data in applications.items():
        if application_data.get('units'):
            apps[model_name]['children'].append(application_name)
            result[application_name] = {'hosts': []}
            for units, unit_data in application_data.get('units', {}) \
                                                    .items():
                if unit_data.get('machine'):
                    host = unit_data.get('machine')
                    try:
                        host_address = machines[host]
                        result['_meta']['hostvars'][host_address] = {}
                        result[application_name]['hosts'].append(
                            host_address)
                    except KeyError:
                        pass

    result.update(apps)

    return result


def inventory_host_units(status):
    """returns an {'ip_address': 'unit_name'} dict"""
    result = defaultdict(lambda: [])

    apps = status.get('applications') or {}
    for app_name, app in apps.items():

        units = app.get('units') or {}
        for unit_name, unit in units.items():
            address = unit.get('public-address')

            if address:
                result[address].append(unit_name)

    return result


class JujuRequestHandler(ApiRequestHandler):
    """extend the base RequestHandler class to add code shared
    by our endpoints. Endpoints should extend this class and
    implement the create_response() method as needed."""

    async def get(self):
        credentials = self.get_basic_auth(self.request.headers)

        filters = self.get_arguments('filter')
        if credentials:
            model_uuid = self.get_argument('model_uuid', None, True)
            status = await juju_status(credentials, model_uuid, filters)
            if status:
                inventory = self.create_response(status)
                self.write(json.dumps(inventory, indent=4))
                return

        self.write(json.dumps({}))

    def create_response(self, status):
        """endpoints will implement this"""
        raise NotImplementedError()


class JujuInventoryHandler(JujuRequestHandler):
    def create_response(self, status):
        machines = get_machines_ips(status)
        return to_inventory_object(status, machines)


class JujuHostsHandler(JujuRequestHandler):
    def create_response(self, status):
        return inventory_host_units(status)


class JujuNrpeMachinesHandler(JujuRequestHandler):
    def create_response(self, status):
        # get all juju machines
        all_machines = get_machines_ips(status)

        # check units. If they have a `nrpe-host` or `nrpe-container`
        # subordinate, or they have a `nrpe-external-master` relation,
        # then machine has Juju managed NRPE
        juju_nrpe_machines = {}
        for app_name, app_data in status['applications'].items():

            app_has_nrpe = 'nrpe-external-master' in app_data['relations']
            for unit_name, unit_data in (app_data.get('units') or {}).items():
                machine_id = unit_data['machine']
                unit_has_nrpe = any(
                    x.startswith('nrpe-')
                    for x in (unit_data.get('subordinates') or []))

                if unit_has_nrpe or app_has_nrpe:
                    juju_nrpe_machines[machine_id] = all_machines[machine_id]

        return juju_nrpe_machines


class JujuStatusHandler(JujuRequestHandler):
    def create_response(self, status):
        return status
