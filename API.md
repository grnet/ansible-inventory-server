# Ansible Inventory Server API

## Common parameters for all endpoints

| Parameter    | Type          | Description                                                                                                                                                                            | Example          |
|--------------|---------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------|
| subnet       | String        | For machines with multiple IP addresses, return the addresses of a specific subnet only. If machine has no IP address on this subnet, then one of its IP addresses is chosen at random | `"10.0.0.0/16"`  |
| subnet_force | Boolean       | Ignore machines that have no IP addresses in the specified `subnet`                                                                                                                    | `true`           |


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

*   `GET /juju/machines`

    Returns a comprehensive list of Juju machines, along with the
    applications that run on each one.

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
