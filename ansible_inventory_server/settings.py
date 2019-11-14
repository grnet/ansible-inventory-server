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
JUJU_ENDPOINT = config_dict['juju']['controller_endpoint']
MODEL_UUID = config_dict['juju']['model_uuid']
