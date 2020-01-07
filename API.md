# Ansible Inventory Server API

<details open><summary><b>Parameters</b></summary>

### Passing Parameters

The API accepts JSON request body parameters. Example (see below for list
of available parameters):

```
$ cat request.json
{
    "response": {"indent": 4},
    "juju": {
        "endpoint": "1.2.3.4:17070",
        "username": "some_username",
        "password": "some_password",
        "model_uuid": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
    }
}
$ curl -XGET https://ansible-inventory-server:port/juju/inventory \
    --data-binary @request.json
```

### List of common parameters

These parameters work for all endpoints below:

| Parameter               | Type          | Description                                                                                                                                                                            | Example          |
|-------------------------|---------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------|
| `subnet`                | String        | For machines with multiple IP addresses, return the addresses of a specific subnet only. If machine has no IP address on this subnet, then one of its IP addresses is chosen at random | `"10.0.0.0/16"`  |
| `subnet_force`          | Boolean       | Ignore machines that have no IP addresses in the specified `subnet`                                                                                                                    | `true`           |
| `interface`             | String        | For machines with multiple IP addresses, return the addresses of a specific interface only.                                                                                            | `"eth0"`         |
| `response.indent`       | Integer       | Indentation for JSON response                                                                                                                                                          | `4`              |
| `response.ensure_ascii` | Boolean       | Whether to escape unicode characters in ASCII format                                                                                                                                   | `false`          |


</details>

---

<details open><summary><b>Juju endpoints</b></summary>

### Parameters

| Parameter         | Type   | Required | Example                               | Description                                       |
|-------------------|--------|----------|---------------------------------------|---------------------------------------------------|
| `juju.username`   | String | YES      | `"admin"`                             | Juju username                                     |
| `juju.password`   | String | YES      | `"some_password"`                     | Juju password                                     |
| `juju.endpoint`   | String | NO (*)   | `"https://10.0.0.1:17070"`            | Juju controller endpoint                          |
| `juju.cacert`     | String | NO (*)   | `"<contents of Juju certificate>"`    | Certificate for connecting to the Juju controller |
| `juju.model_uuid` | String | NO (*)   | `"aaaaaa-bbbbb-cccccc-dddd-eeeeeee"`  | Juju model UUID to connect to                     |
| `juju.filters`    | List   | NO       | `["nova-compute", "keystone"]`        | List of filters for Juju applications/hosts/units |

`(*)`: If missing, the default ones from the server config.yml file are used instead

Example passing Juju credentials:

```
$ curl -d '{"juju": {"username": "user", "password": "pass", "filters": ["nova-compute"]}}' ...
```

### Endpoints

*   `GET /juju/inventory`

    Returns an Ansible inventory containing all hosts returned by Juju.
    They are grouped by application name.

    <details><summary>Example:</summary>

    ```
    curl -XGET -d '{"juju": {"username": "USER", "pasword": "PASS", "filters": ["keystone"]}, "response": {"indent": 4}}' localhost:5000/juju/inventory
    ```

    ```json
    {
        "_meta": {
            "hostvars": {
                "IP_ADDRESS_FOR_MACHINE_1": {},
                "IP_ADDRESS_FOR_MACHINE_2": {},
                "IP_ADDRESS_FOR_MACHINE_3": {}
            }
        },
        "openstack": {
            "children": [
                "keystone"
            ]
        },
        "keystone": {
            "hosts": [
                "MACHINE_1",
                "MACHINE_2",
                "MACHINE_3"
            ]
        }
    }
    ```
    </details>

*   `GET /juju/machines`

    Returns a complete list of Juju machines (and containers), along with
    information regarding their running apps, subordinate units and containers.

    <details><summary>Example response:</summary>

    ```json
    {
        "92": {
            "id": "92",
            "name": "lar0502",
            "instance_id": "23ad31",
            "ip_addresses": [
                "110.34.10.31",
                "10.0.0.30"
            ],
            "apps": [],
            "subordinates": [],
            "containers": [
                "92/lxd/36"
            ],
            "parent": null
        },
        "92/lxd/36": {
            "id": "92/lxd/36",
            "name": "juju-980f92-92-lxd-36",
            "instance_id": "juju-980f92-92-lxd-36",
            "ip_addresses": [
                "110.34.10.35",
                "10.0.0.31"
            ],
            "apps": [
                "ubuntu"
            ],
            "subordinates": [
                "nrpe-container/836",
                "ntp/1090"
            ],
            "containers": [],
            "parent": "92"
        }
    }
    ```
    </details>

*   `GET /juju/status`

    Returns raw Juju status (in JSON format). Same as running `juju status --format json`

</details>

---

<details open>
<summary><b>MaaS endpoints</b>
</summary>

### Parameters

| Parameter         | Type   | Required | Example                                        | Description                                       |
|-------------------|--------|----------|------------------------------------------------|---------------------------------------------------|
| `maas.url`        | String | YES      | `"https://maas-server-name:5240/MAAS/api/2.0"` | MaaS API URL                                      |
| `maas.apikey`     | String | YES      | `"aaaaaaa:bbbbbbbbbbbbbbbbbbbb:cccccccccccc"`  | MaaS API Key                                      |

### Endpoints

*   `GET /maas/inventory`

    Returns an Ansible inventory containing all hosts returned by MaaS.
    They are grouped by their tags (NOTE: if a host returned by MaaS
    has more than one tags, it will be listed under all of them).

    <details><summary>Example:</summary>

    ```
    curl -XGET -d '{"maas": {"url": "https://maas-server:5240/MAAS/api/2.0", "api_key": "AAAAA:BBBB:CCCC"}, "response": {"indent": 4}}' localhost:5000/maas/inventory
    ```

    ```json
    {
        "production": [
            "HOST_1_IP_ADDRESS",
            "HOST_2_IP_ADDRESS"
        ],
        "other-tag": [
            "HOST_2_IP_ADDRESS",
            "HOST_3_IP_ADDRESS"
        ]
    }
    ```

    </details>


*   `GET /maas/machines`

    | Parameter         | Type    | Required | Example  | Description                                        |
    |-------------------|---------|----------|----------|----------------------------------------------------|
    | `maas.raw`        | Boolean | NO       | `true`   | Return raw response, as returned from the MaaS API |

    Returns list of MaaS machines, along with basic information about them.

    <details><summary>Example:</summary>

    ```
    curl -XGET -d '{"maas": {"url": "https://maas-server:5240/MAAS/api/2.0", "api_key": "AAAAA:BBBB:CCCC"}, "response": {"indent": 4}}' localhost:5000/maas/machines
    ```

    ```js
    [
        {
            "fqdn": "HOST_1.DOMAIN.EXT",
            "hostname": "HOST_1",
            "system_id": "asd67a",
            "ip_addresses": [
                "10.0.0.10",
                "241.23.23.23"
            ],
            "tags": [
                "tag1",
                "tag2"
            ],
            "pod": "gf782"               /* parent system id */
        },
        {
            "fqdn": "HOST_2.DOMAIN_EXT",
            "hostname": "HOST_2",
            "system_id": "gf782a",
            "ip_addresses": [
                "10.0.0.32",
                "241.23.23.24"
            ],
            "tags": [
                "tag2",
                "tag3"
            ],
            "pod": null                  /* bare metal server */
        }
    ]
    ```
    </details>

</details>
