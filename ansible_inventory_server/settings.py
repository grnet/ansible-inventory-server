import pkg_resources
import yaml


def read_config():
    with open(pkg_resources.resource_filename(
            __name__, 'config/config.yml')) as f:
        config = yaml.safe_load(f)
    return config


config_dict = read_config()

CACERT_PATH = pkg_resources.resource_filename(
    __name__, 'config/controller.crt')
CONTROLLER_ENDPOINT = config_dict['juju']['controller_endpoint']
MODEL_UUID = config_dict['juju']['model_uuid']
MAAS_ENDPOINT = config_dict['maas']['endpoint']
