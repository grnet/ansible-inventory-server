# Ansible Inventory Server API

## Juju endpoints

Common parameters for all Juju endpoints:

| Parameter  | Description                                                                                                                                  | Example                                   |
|------------|----------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------|
| filter     | Juju filter. If given, will limit results to that specific unit/app/machine. It is the equivalent of calling the CLI `juju status FILTER`    | `nova-compute`                            |

Pass parameters using a JSON body:

```
$ curl -XGET http://localhost:5000/juju/inventory -d \
    '{"juju": {"username": "admin", "password": "pass"}}'
```

*   `GET /juju/inventory`

    Returns an Ansible inventory containing all hosts returned by Juju.
    They are grouped by application name.

*   `GET /juju/status`

    Returns raw Juju status (in JSON format)

*   `GET /juju/hosts`

    Returns a complete list of Juju hosts, as returned by `juju status`

*   `GET /juju/nrpemachines`

    Returns a list of machines that have NRPE installed and are managed
    by Juju.


---

## MaaS endpoints

Pass parameters using a JSON body

```
$ curl -XGET http://localhost:5000/maas/inventory -d \
    '{"maas": {"url": "https://maas.server:5240/MAAS/api/2.0", "apikey": "AAAAA:BBB:CCCC"}}'
```

*   `GET /maas/inventory`

    Returns an Ansible inventory containing all hosts returned by MaaS.
    They are grouped by their tags (NOTE: if a host returned by MaaS
    has more than one tags, it will be listed under all of them)

*   `GET /maas/machines`

    Returns list of MaaS machines (in JSON format), as returned by the
    MaaS API
