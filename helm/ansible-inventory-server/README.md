# Ansible Inventory Server Helm Chart
[Ansible Inventory Server](https://github.com/grnet/ansible-inventory-server) is an easily extensible lightweight server which can create dynamic Ansible Inventories from Juju and MaaS data sources.

## Introduction

This chart bootstraps a Ansible Inventory Server deployment on a [Kubernetes](http://kubernetes.io) cluster using the [Helm](https://helm.sh) package manager.

## Installing the Chart
To install the chart with the release name `my-release`:

```console
$ helm install my-release .
```

The command deploys Ansible Inventory Server on the Kubernetes cluster in the default configuration. The [Parameters](#parameters) section lists the parameters that can be configured during installation.

## Uninstalling the Chart

To uninstall/delete the `my-release` deployment:

```console
$ helm delete my-release
```

The command removes all the Kubernetes components associated with the chart and deletes the release.

## Parameters

The following tables lists the configurable parameters of the Ansible Inventory Server chart and their default values.

| Variable                                  | Description                                 | Default                                                  |
| ----------------------------------------- | ------------------------------------------- | -------------------------------------------------------- |
| `ansibleInventoryServerImage.repository`  | Ansible Inventory Server Image name         | `cloudeng/ansible-inventory-server`                      |
| `ansibleInventoryServerImage.tag`         | Ansible Inventory Server Image tag          | `{TAG_NAME}`                                             |
| `ansibleInventoryServerImage.pullPolicy`  | Ansible Inventory Server Image pull policy  | `IfNotPresent`                                           |
| `ansibleInventoryServerImage.pullSecrets` | Ansible Inventory Server Image pull secrets | `nil` (does not add image pull secrets to deployed pods) |
