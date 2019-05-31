# Methods Naming Convention
Each available method rely on the following naming convention for intuitive usage :

```
	<module>_<object>_<action>
```

# Methode list

## Sites - address spaces
* **[ip_site_add](ip_site_add.md)** => This service allows to add an IP address Space.
* **[ip_site_update](ip_site_update.md)** => This service allows to update an IP address Space.
* **[ip_site_count](ip_site_count.md)** => This service returns the number of IP address Spaces matching optional condition(s).
* **[ip_site_list](ip_site_list.md)** => This service returns a list of IP address Spaces matching optional condition(s).
* **[ip_site_info](ip_site_info.md)** => This service returns information about a specific IP address Space.
* **[ip_site_delete](ip_site_delete.md)** => This service allows to delete a specific IP address Space.

## Subnets
### IPv4
* **[ip_subnet_add](ip_subnet_add.md)** => This service allows to add an IPv4 Network of type Subnet or Block.
* **[ip_subnet_update](ip_subnet_update.md)** => This service allows to update an IPv4 Network of type Subnet or Block.
* **[ip_subnet_count](ip_subnet_count.md)** => This service returns the number of IPv4 Networks matching optional condition(s).
* **[ip_subnet_list](ip_subnet_list.md)** => This service returns a list of IPv4 Networks matching optional condition(s).
* **[ip_subnet_info](ip_subnet_info.md)** => This service returns information about a specific IPv4 Network.
* **[ip_subnet_delete](ip_subnet_delete.md)** => This service allows to delete a specific IPv4 Network.
### IPv6
* **[ip_subnet6_add](ip_subnet6_add.md)** => This service allows to add an IPv6 Network of type Subnet or Block.
* **[ip_subnet6_update](ip_subnet6_update.md)** => This service allows to update an IPv6 Network of type Subnet or Block.
* **[ip_subnet6_count](ip_subnet6_count.md)** => This service returns the number of IPv6 Networks matching optional condition(s).
* **[ip_subnet6_list](ip_subnet6_list.md)** => This service returns a list of IPv6 Networks matching optional condition(s).
* **[ip_subnet6_info](ip_subnet6_info.md)** => This service returns information about a specific IPv6 Network.
* **[ip_subnet6_delete](ip_subnet6_delete.md)** => This service allows to delete a specific IPv6 Network.

## Pools
### IPv4
* **[ip_pool_add](ip_pool_add.md)** => This service allows to add an IPv4 Address Pool.
* **[ip_pool_update](ip_pool_update.md)** => This service allows to update an IPv4 Address Pool.
* **[ip_pool_count](ip_pool_count.md)** => This service returns the number of IPv4 Address Pools matching optional condition(s).
* **[ip_pool_list](ip_pool_list.md)** => This service returns a list of IPv4 Address Pools matching optional condition(s).
* **[ip_pool_info](ip_pool_info.md)** => This service returns information about a specific IPv4 Address Pool.
* **[ip_pool_delete](ip_pool_delete.md)** => This service allows to delete a specific IPv4 Address Pool.
### IPv6
* **[ip_pool6_add](ip_pool6_add.md)** => This service allows to add an IPv6 Address Pool.
* **[ip_pool6_update](ip_pool6_update.md)** => This service allows to update an IPv6 Address Pool.
* **[ip_pool6_count](ip_pool6_count.md)** => This service returns the number of IPv6 Address Pools matching optional condition(s).
* **[ip_pool6_list](ip_pool6_list.md)** => This service returns a list of IPv6 Address Pools matching optional condition(s).
* **[ip_pool6_info](ip_pool6_info.md)** => This service returns information about a specific IPv6 Address Pool.
* **[ip_pool6_delete](ip_pool6_delete.md)** => This service allows to delete a specific IPv6 Address Pool.

## Addresses
### IPv4
* **[ip_address_add](ip_address_add.md)** => This service allows to add an IPv4 Address.
* **[ip_address_update](ip_address_update.md)** => This service allows to update an IPv4 Address.
* **[ip_address_count](ip_address_count.md)** => This service returns the number of IPv4 Addresses matching optional condition(s).
* **[ip_address_list](ip_address_list.md)** => This service returns a list of IPv4 Addresses matching optional condition(s).
* **[ip_address_info](ip_address_info.md)** => This service returns information about a specific IPv4 Address.
* **[ip_address_delete](ip_address_delete.md)** => This service allows to delete a specific IPv4 Address.

### IPv6
* **[ip_address6_add](ip_address6_add.md)** => This service allows to add an IPv6 Address
* **[ip_address6_update](ip_address6_update.md)** => This service allows to update an IPv6 Address
* **[ip_address6_count](ip_address6_count.md)** => This service returns the number of IPv6 Addresses matching optional condition(s).
* **[ip_address6_list](ip_address6_list.md)** => This service returns a list of IPv6 Addresses matching optional condition(s).
* **[ip_address6_info](ip_address6_info.md)** => This service returns information about a specific IPv6 Address.
* **[ip_address6_delete](ip_address6_delete.md)** => This service allows to delete a specific IPv6 Address.

## Aliases
### IPv4
* **[ip_alias_add](ip_alias_add.md)** => This service allows to associate an Alias of type A or CNAME to an IPv4 Address.
* **[ip_alias_list](ip_alias_list.md)** => This service returns the list of an IPv4 Address associated Aliases.
* **[ip_alias_delete](ip_alias_delete.md)** => This service allows to remove an Alias associated to an IPv4 Address.

### IPv6
* **[ip_alias6_add](ip_alias6_add.md)** => This service allows to associate an Alias of type A or CNAME to an IPv4 Address.
* **[ip_alias6_list](ip_alias6_add.md)** => This service returns the list of an IPv6 Address associated Aliases.
* **[ip_alias6_delete](ip_alias6_delete.md)** => This service allows to remove an Alias associated to an IPv6 Address.

## Applications
### Application

* **app_application_list** => lists all the applications in the IPAM
* **app_application_add** => add an application definition
* **app_application_delete** => delete the specified application
* **app_application_count** => count the applications in the IPAM
* **app_application_info** => provide information on an application
* **app_application_delete** => delete an application and all pools and nodes attached

### Pool of nodes
* **app_pool_add** => add a pool of nodes to the application
* **app_pool_update** => update a pool of nodes from an application
* **app_pool_list** => list all the pools
* **app_pool_count** => count the pools
* **app_pool_info** => get information about a pool
* **app_pool_delete** => delete a pool and all the nodes attached

### Nodes
* **app_node_add': 'app_node_add'** => add a node to a pool
* **app_node_update': 'app_node_add'** => update a node in a pool
* **app_node_info': 'app_node_info'** => get information from a node in a pool
* **app_node_count': 'app_node_count'** => count the nodes
* **app_node_list': 'app_node_list'** => list the nodes
* **app_node_delete': 'app_node_delete'** => delete a node in a pool

### Healthchecks

* **app_healthcheck_count': 'app_healthcheck_count'** => add a health check to a node
* **app_healthcheck_info': 'app_healthcheck_info'** => get information about a node health check
* **app_healthcheck_list': 'app_healthcheck_list'** => list the health checks attached to a node
