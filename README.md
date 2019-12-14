# Ansible Inventory Server

Ansible Inventory Server is an easily extensible lightweight server
which can create dynamic Ansible Inventories from Juju and MaaS data
sources.

## Features

* Rest API for creating dynamic Ansible inventories from MaaS or Juju
  data sources.
* Inventory scripts for Ansible and AWX (`scripts/`)
* Rest API for retrieving machine information for MaaS and Juju machines

Extended documentation for the API can be found at [API.md](./API.md)

## Requirements

* [Docker](https://docs.docker.com/install/)
* [Docker Compose](https://docs.docker.com/compose/install/)

## Deployment

You can deploy the server using docker-compose. First, create a config
file with Juju and MaaS server information:

```bash
$ cp docker/config.yml.sample docker/config.yml
$ vim docker/config.yml
```

Then, deploy the server with:

```bash
$ cd docker
$ docker-compose up -d
```

The server should be available at `localhost:5000`.

## AWX Dynamic Inventory (for Juju)

The following steps are required for creating a dynamic AWX inventory for
Juju machines:

- Under tab `Credential Types`, create a new type of credentials. Choose
  `Juju Credentials` as name. Use [this Input Configuration][1] and
  [this Injector Configuration][2]. Save the new credentials type.
- Under `Resources/Credentials`, create new credentials of type
  `Juju Credentials`. Fill in with the information of your Juju deployment.
- Under `Resources/Inventory Scripts` create a new inventory script, and in
  the `Custom Script` section paste the contents of [the inventory script][3].
- Optionally, edit the script file to suit your specific deployment needs.
- Under `Resources/Inventories` create a new Inventory.
- Open the new inventory, go to the `Sources` tab, and click add. Choose
  `Custom Script` as inventory source type. Choose your inventory script, and
  include the Juju Credentials you created on the second step.
- Save configuration, then click Refresh. You should be seeing your Juju
  machines appearing under your Inventory.

You are now able to use this inventory with your Ansible Playbooks.

The process for MaaS machines is the same. Simply use the appropriate MaaS
files instead.

[1]: ./awx/creds_juju_input.yaml "Juju Credentials Input Configuration"
[2]: ./awx/creds_juju_injector.yaml "Juju Credentials Injector Configuration"
[3]: ./scripts/juju_inventory_script.py "Juju Credentials Injector Configuration"
