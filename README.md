# Ansible Inventory Server
Ansible Inventory Server is an easily extensible lightweight server
which can create dynamic Ansible Inventories from Juju and MaaS data
sources.

## Deployment
The deployment of the Server is as easy as a click of a button. The
provided docker-compose does all the appropriate actions to deploy the
server inside a container and make it available through a host port.

### Prerequisites
In order to deploy the server then docker and docker-compose must be
installed.

Furthermore, you should create a proper `config.yml` file with Juju and
MaaS server info:

```bash
$ cp docker/config.yml.sample docker/config.yml
$ vim docker/config.yml
```

#### Install Docker
To install Docker on Ubuntu you should run the following commands:

```bash
$ sudo apt-get update
$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
$ sudo add-apt-repository \
     "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
     $(lsb_release -cs) \
     stable"
$ sudo apt-get update
$ sudo apt-get install -y docker-ce docker-ce-cli containerd.io
$ sudo docker run hello-world
```

#### Install docker-compose
To install docker-compose on Ubuntu you should run the following
commands:

```bash
$ sudo curl \
     -L "https://github.com/docker/compose/releases/download/1.24.0/docker-compose-$(uname -s)-$(uname -m)" \
     -o /usr/local/bin/docker-compose
$ sudo chmod +x /usr/local/bin/docker-compose
$ docker-compose --version
```

### Instructions
To deploy the server you should run:

```bash
$ sudo docker-compose up -d
```

To teardown the server you should run:

```bash
$ sudo docker-compose down
```

## Usage
At the moment `Ansible Inventory Server` can produce a JSON inventory
representation of the `juju status` command. In order
to get the JSON user should run:

```bash
$ curl \
      -u username:password \
      http://<ip_or_name_of_host>:5000/juju/inventory?model_uuid=<uuid_of_juju_model>
```

The above `username` and `password` are the user's credentials for Juju
and `model_uuid` is the uuid of the Juju model user wants to acquire
information from.

## AWX Dynamic Inventories (for Juju)
In order to create dynamic inventories of Juju models, user should do
the following actions:

1. Create Custom Credentials (e.g. `Juju Credentials`) with the
following fields: `username`, `password` and `model_uuid`
2. Add Credentials of type `Juju Credentials` to provide a valid
combination of `username`, `password` and `model_uuid`.
3. Create an Inventory and use the custom script juju-inventory-script
as a Source for the Inventory.
4. When adding the Source to the Inventory user should use the
Credentials created at step 1 and options `OVERWRITE` and
`UPDATE ON LAUNCH`.
5. Sync the Inventory and confirm that the action succeeded (cloud icon
next to the inventory turns to green color)

## AWX Dynamic Inventories (for MaaS)
Similarly, create Custom Credentials with the field: `api_key`.

### AWX Inventory Script
The provided `juju_inventory_script.py` and `maas_inventory_scripts.py`
are the scripts which AWX runs to create dynamic inventories.

### API Documentation
The API contains the inventory as well as a few others misc endpoints.
Refer to [API.md](./API.md) for details.
