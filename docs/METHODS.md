# Methods Naming Convention
Each available method rely on the following naming convention for intuitive usage :

```
	<module>_<object>_<action>
```

# Method list

## Sites - address spaces
* **[ip_site_create](ip_site_create.md)** => This service allows to add an IP address Space.
* **[ip_site_update](ip_site_update.md)** => This service allows to update an IP address Space.
* **[ip_site_count](ip_site_count.md)** => This service returns the number of IP address Spaces matching optional condition(s).
* **[ip_site_list](ip_site_list.md)** => This service returns a list of IP address Spaces matching optional condition(s).
* **[ip_site_info](ip_site_info.md)** => This service returns information about a specific IP address Space.
* **[ip_site_delete](ip_site_delete.md)** => This service allows to delete a specific IP address Space.

## Subnets
### IPv4
* **[ip_subnet_create](ip_subnet_create.md)** => This service allows to add an IPv4 Network of type Subnet or Block.
* **[ip_subnet_update](ip_subnet_update.md)** => This service allows to update an IPv4 Network of type Subnet or Block.
* **[ip_subnet_count](ip_subnet_count.md)** => This service returns the number of IPv4 Networks matching optional condition(s).
* **[ip_subnet_list](ip_subnet_list.md)** => This service returns a list of IPv4 Networks matching optional condition(s).
* **[ip_subnet_info](ip_subnet_info.md)** => This service returns information about a specific IPv4 Network.
* **[ip_subnet_delete](ip_subnet_delete.md)** => This service allows to delete a specific IPv4 Network.
* **ip_subnet_find_free** => This service allows to find a free subnet for further creation

### IPv6
* **[ip_subnet6_create](ip_subnet6_create.md)** => This service allows to add an IPv6 Network of type Subnet or Block.
* **[ip_subnet6_update](ip_subnet6_update.md)** => This service allows to update an IPv6 Network of type Subnet or Block.
* **[ip_subnet6_count](ip_subnet6_count.md)** => This service returns the number of IPv6 Networks matching optional condition(s).
* **[ip_subnet6_list](ip_subnet6_list.md)** => This service returns a list of IPv6 Networks matching optional condition(s).
* **[ip_subnet6_info](ip_subnet6_info.md)** => This service returns information about a specific IPv6 Network.
* **[ip_subnet6_delete](ip_subnet6_delete.md)** => This service allows to delete a specific IPv6 Network.

## Pools
### IPv4
* **[ip_pool_create](ip_pool_create.md)** => This service allows to add an IPv4 Address Pool.
* **[ip_pool_update](ip_pool_update.md)** => This service allows to update an IPv4 Address Pool.
* **[ip_pool_count](ip_pool_count.md)** => This service returns the number of IPv4 Address Pools matching optional condition(s).
* **[ip_pool_list](ip_pool_list.md)** => This service returns a list of IPv4 Address Pools matching optional condition(s).
* **[ip_pool_info](ip_pool_info.md)** => This service returns information about a specific IPv4 Address Pool.
* **[ip_pool_delete](ip_pool_delete.md)** => This service allows to delete a specific IPv4 Address Pool.

### IPv6
* **[ip_pool6_create](ip_pool6_create.md)** => This service allows to add an IPv6 Address Pool.
* **[ip_pool6_update](ip_pool6_update.md)** => This service allows to update an IPv6 Address Pool.
* **[ip_pool6_count](ip_pool6_count.md)** => This service returns the number of IPv6 Address Pools matching optional condition(s).
* **[ip_pool6_list](ip_pool6_list.md)** => This service returns a list of IPv6 Address Pools matching optional condition(s).
* **[ip_pool6_info](ip_pool6_info.md)** => This service returns information about a specific IPv6 Address Pool.
* **[ip_pool6_delete](ip_pool6_delete.md)** => This service allows to delete a specific IPv6 Address Pool.

## Addresses
### IPv4
* **[ip_address_create](ip_address_create.md)** => This service allows to add an IPv4 Address.
* **[ip_address_update](ip_address_update.md)** => This service allows to update an IPv4 Address.
* **[ip_address_count](ip_address_count.md)** => This service returns the number of IPv4 Addresses matching optional condition(s).
* **[ip_address_list](ip_address_list.md)** => This service returns a list of IPv4 Addresses matching optional condition(s).
* **[ip_address_info](ip_address_info.md)** => This service returns information about a specific IPv4 Address.
* **[ip_address_delete](ip_address_delete.md)** => This service allows to delete a specific IPv4 Address.

### IPv6
* **[ip_address6_create](ip_address6_create.md)** => This service allows to add an IPv6 Address
* **[ip_address6_update](ip_address6_update.md)** => This service allows to update an IPv6 Address
* **[ip_address6_count](ip_address6_count.md)** => This service returns the number of IPv6 Addresses matching optional condition(s).
* **[ip_address6_list](ip_address6_list.md)** => This service returns a list of IPv6 Addresses matching optional condition(s).
* **[ip_address6_info](ip_address6_info.md)** => This service returns information about a specific IPv6 Address.
* **[ip_address6_delete](ip_address6_delete.md)** => This service allows to delete a specific IPv6 Address.

## Aliases
### IPv4
* **[ip_alias_create](ip_alias_create.md)** => This service allows to associate an Alias of type A or CNAME to an IPv4 Address.
* **[ip_alias_list](ip_alias_list.md)** => This service returns the list of an IPv4 Address associated Aliases.
* **[ip_alias_delete](ip_alias_delete.md)** => This service allows to remove an Alias associated to an IPv4 Address.

### IPv6
* **[ip_alias6_create](ip_alias6_create.md)** => This service allows to associate an Alias of type A or CNAME to an IPv4 Address.
* **[ip_alias6_list](ip_alias6_add.md)** => This service returns the list of an IPv6 Address associated Aliases.
* **[ip_alias6_delete](ip_alias6_delete.md)** => This service allows to remove an Alias associated to an IPv6 Address.


## DNS
### DNS server
* **[dns_server_create](dns_server_create.md)** => add a DNS server
* **[dns_server_update](dns_server_update.md)** => update a DNS server
* **[dns_server_count](dns_server_count.md)** => count the DNS servers
* **[dns_server_list](dns_server_list.md)** => list DNS servers with their attributes
* **[dns_server_info](dns_server_info.md)** => get information about one DNS server
* **[dns_server_delete](dns_server_delete.md)** => delete a DNS server

### DNS zone
* **[dns_zone_create](dns_zone_create.md)** => add a DNS zone for a DNS server
* **[dns_zone_update](dns_zone_update.md)** => update a zone
* **[dns_zone_count](dns_zone_count.md)** => count the DNS zones
* **[dns_zone_list](dns_zone_list.md)** => list DNS zones with their attributes
* **[dns_zone_info](dns_zone_info.md)** => get information about one DNS zone
* **[dns_zone_delete](dns_zone_delete.md)** => delete a DNS zone

### DNS zone options
* **[dns_zone_param_create](dns_zone_param_create.md)** => add a DNS option on a zone
* **[dns_zone_param_update](dns_zone_param_update.md)** => update a DNS zone option
* **[dns_zone_param_count](dns_zone_param_count.md)** => count the DNS options on a zone
* **[dns_zone_param_list](dns_zone_param_list.md)** => list DNS options on a zone with their attributes
* **[dns_zone_param_info](dns_zone_param_info.md)** => get information about one DNS zone options
* **[dns_zone_param_delete](dns_zone_param_delete.md)** => delete a DNS zone option

### DNS view
* **[dns_view_create](dns_view_create.md)** => add a DNS view on a DNS server
* **[dns_view_update](dns_view_update.md)** => update a DNS view
* **[dns_view_count](dns_view_count.md)** => count the DNS views
* **[dns_view_list](dns_view_list.md)** => list DNS views with their attributes
* **[dns_view_info](dns_view_info.md)** => get information about one DNS view
* **[dns_view_delete](dns_view_delete.md)** => delete a DNS view

### DNS view options
* **[dns_view_param_create](dns_view_param_create.md)** => add a DNS option on a view
* **[dns_view_param_update](dns_view_param_update.md)** => update a DNS view option
* **[dns_view_param_count](dns_view_param_count.md)** => count the DNS options on a view
* **[dns_view_param_list](dns_view_param_list.md)** => list DNS options on a view with their attributes
* **[dns_view_param_info](dns_view_param_info.md)** => get information about one DNS view options
* **[dns_view_param_delete](dns_view_param_delete.md)** => delete a DNS view option


## DHCP
### DHCP server for IPv4
* **[dhcp_server_create](dhcp_server_create.md)** => add a DHCP server
* **[dhcp_server_update](dhcp_server_update.md)** => update a DHCP server
* **[dhcp_server_count](dhcp_server_count.md)** => count the DHCP servers
* **[dhcp_server_list](dhcp_server_list.md)** => list DHCP servers with their attributes
* **[dhcp_server_info](dhcp_server_info.md)** => get information about one DHCP server
* **[dhcp_server_delete](dhcp_server_delete.md)** => delete a DHCP server

### DHCP scope for IPv4
* **[dhcp_scope_create](dhcp_scope_create.md)** => add a DHCP scope
* **[dhcp_scope_update](dhcp_scope_update.md)** => update a DHCP scope
* **[dhcp_scope_count](dhcp_scope_count.md)** => count the DHCP scope
* **[dhcp_scope_list](dhcp_scope_list.md)** => list DHCP scope with their attributes
* **[dhcp_scope_info](dhcp_scope_info.md)** => get information about one DHCP scope
* **[dhcp_scope_delete](dhcp_scope_delete.md)** => delete a DHCP scope

### DHCP range for IPv4
* **[dhcp_range_create](dhcp_range_create.md)** => add a DHCP range of addresses
* **[dhcp_range_update](dhcp_range_update.md)** => update a DHCP range of addresses
* **[dhcp_range_count](dhcp_range_count.md)** => count the DHCP ranges
* **[dhcp_range_list](dhcp_range_list.md)** => list DHCP ranges with their attributes
* **[dhcp_range_info](dhcp_range_info.md)** => get information about one DHCP range of addresses
* **[dhcp_range_delete](dhcp_range_delete.md)** => delete a DHCP range

### DHCP group for IPv4
* **[dhcp_group_create](dhcp_group_create.md)** => add a DHCP group
* **[dhcp_group_update](dhcp_group_update.md)** => update a DHCP group
* **[dhcp_group_count](dhcp_group_count.md)** => count the number of DHCP groups
* **[dhcp_group_list](dhcp_group_list.md)** => list DHCP groups with their attributes
* **[dhcp_group_info](dhcp_group_info.md)** => get information about one DHCP group
* **[dhcp_group_delete](dhcp_group_delete.md)** => delete a DHCP group

### DHCP shared network for IPv4
* **[dhcp_shared_net_create](dhcp_shared_net_create.md)** => add a DHCP shared network definition
* **[dhcp_shared_net_count](dhcp_shared_net_count.md)** => count the number of DHCP shared networks
* **[dhcp_shared_net_list](dhcp_shared_net_list.md)** => list DHCP shared networks with their attributes
* **[dhcp_shared_net_info](dhcp_shared_net_info.md)** => get information about one DHCP shared network

### DHCP static for IPv4
* **[dhcp_static_create](dhcp_static_create.md)** => add a DHCP static addresses
* **[dhcp_static_update](dhcp_static_update.md)** => update a DHCP static addresses
* **[dhcp_static_count](dhcp_static_count.md)** => count the DHCP static addresses
* **[dhcp_static_list](dhcp_static_list.md)** => list DHCP static addresses with their attributes
* **[dhcp_static_info](dhcp_static_info.md)** => get information about one DHCP static address
* **[dhcp_static_delete](dhcp_range_delete.md)** => delete a DHCP static address

### DHCP server for IPv6
* **[dhcp_server6_create](dhcp_server6_create.md)** => add a DHCP server
* **[dhcp_server6_update](dhcp_server6_update.md)** => update a DHCP server
* **[dhcp_server6_count](dhcp_server6_count.md)** => count the DHCP servers
* **[dhcp_server6_list](dhcp_server6_list.md)** => list DHCP servers with their attributes
* **[dhcp_server6_info](dhcp_server6_info.md)** => get information about one DHCP server
* **[dhcp_server6_delete](dhcp_server6_delete.md)** => delete a DHCP server

### DHCP scope for IPv6
* **[dhcp_scope6_create](dhcp_scope6_create.md)** => add a DHCP scope
* **[dhcp_scope6_update](dhcp_scope6_update.md)** => update a DHCP scope
* **[dhcp_scope6_count](dhcp_scope6_count.md)** => count the DHCP scope
* **[dhcp_scope6_list](dhcp_scope6_list.md)** => list DHCP scope with their attributes
* **[dhcp_scope6_info](dhcp_scope6_info.md)** => get information about one DHCP scope
* **[dhcp_scope6_delete](dhcp_scope6_delete.md)** => delete a DHCP scope

### DHCP range for IPv6
* **[dhcp_range6_create](dhcp_range6_create.md)** => add a DHCP range of addresses
* **[dhcp_range6_update](dhcp_range6_update.md)** => update a DHCP range of addresses
* **[dhcp_range6_count](dhcp_range6_count.md)** => count the DHCP ranges
* **[dhcp_range6_list](dhcp_range6_list.md)** => list DHCP ranges with their attributes
* **[dhcp_range6_info](dhcp_range6_info.md)** => get information about one DHCP range of addresses
* **[dhcp_range6_delete](dhcp_range6_delete.md)** => delete a DHCP range

### DHCP static for IPv6
* **[dhcp_static6_create](dhcp_static6_create.md)** => add a DHCP static addresses
* **[dhcp_static6_update](dhcp_static6_update.md)** => update a DHCP static addresses
* **[dhcp_static6_count](dhcp_static6_count.md)** => count the DHCP static addresses
* **[dhcp_static6_list](dhcp_static6_list.md)** => list DHCP static addresses with their attributes
* **[dhcp_static6_info](dhcp_static6_info.md)** => get information about one DHCP static address
* **[dhcp_static6_delete](dhcp_range6_delete.md)** => delete a DHCP static address

## Applications
### Application

* **[app_application_create](app_application_create.md)** => add an application definition
* **[app_application_update](app_application_update.md)** => update an application definition
* **[app_application_list](app_application_list.md)** => lists all the applications in the IPAM
* **[app_application_count](app_application_count.md)** => count the applications in the IPAM
* **[app_application_info](app_application_info.md)** => provide information on an application
* **[app_application_delete](app_application_delete.md)** => delete an application and all pools and nodes attached

### Pool of nodes
* **[app_pool_create](app_pool_create.md)** => add a pool of nodes to the application
* **[app_pool_update](app_pool_update.md)** => update a pool of nodes from an application
* **[app_pool_list](app_pool_list.md)** => list all the pools
* **[app_pool_count](app_pool_count.md)** => count the pools
* **[app_pool_info](app_pool_info.md)** => get information about a pool
* **[app_pool_delete](app_pool_delete.md)** => delete a pool and all the nodes attached

### Nodes
* **[app_node_create](app_node_create.md)** => add a node to a pool
* **[app_node_update](app_node_update.md)** => update a node in a pool
* **[app_node_info](app_node_info.md)** => get information from a node in a pool
* **[app_node_count](app_node_count.md)** => count the nodes
* **[app_node_list](app_node_list.md)** => list the nodes
* **[app_node_delete](app_node_delete.md)** => delete a node in a pool

### Healthchecks

* **[app_healthcheck_count](app_healthcheck_count.md)** => add a health check to a node
* **[app_healthcheck_info](app_healthcheck_info.md)** => get information about a node health check
* **[app_healthcheck_list](app_healthcheck_list.md)** => list the health checks attached to a node

## VLan Manager
### Domain
* **[vlm_domain_create](vlm_domain_create.md)** => add a vlan domain
* **[vlm_domain_update](vlm_domain_update.md)** => update a vlan domain
* **[vlm_domain_list](vlm_domain_list.md)** => list all the vlan domains
* **[vlm_domain_count](vlm_domain_count.md)** => count the vlan domains
* **[vlm_domain_info](vlm_domain_info.md)** => get information about a vlan domain
* **[vlm_domain_delete](vlm_domain_delete.md)** => delete a vlan domain

### Range
* **[vlm_range_create](vlm_range_create.md)** => add a vlan range
* **[vlm_range_update](vlm_range_update.md)** => update a vlan range
* **[vlm_range_list](vlm_range_list.md)** => list all the vlan ranges
* **[vlm_range_count](vlm_range_count.md)** => count the vlan ranges
* **[vlm_range_info](vlm_range_info.md)** => get information about a vlan range
* **[vlm_range_delete](vlm_range_delete.md)** => delete a vlan range

### VLan
* **[vlm_vlan_create](vlm_vlan_create.md)** => add vlan
* **[vlm_vlan_update](vlm_vlan_update.md)** => update a vlan
* **[vlm_vlan_list](vlm_vlan_list.md)** => list all the vlan
* **[vlm_vlan_count](vlm_vlan_count.md)** => count the vlan
* **[vlm_vlan_info](vlm_vlan_info.md)** => get information about a vlan
* **[vlm_vlan_delete](vlm_vlan_delete.md)** => delete a vlan

## Device Manager
### Device Manager Host
* **[host_device_create](host_device_create.md)** => add a Device Manager device
* **[host_device_update](host_device_update.md)** => update a Device Manager device
* **[host_device_list](host_device_list.md)** => list all the devices in Device Manager
* **[host_device_count](host_device_count.md)** => count the number of devices in Device Manager
* **[host_device_info](host_device_info.md)** => get information about a device in Device Manager
* **[host_device_delete](host_device_delete.md)** => delete a device in Device Manager

### Device Manager Host Interface (or Port)
* **[host_iface_create](host_iface_create.md)** => add a Device Manager device interface
* **[host_iface_update](host_iface_update.md)** => update a Device Manager device interface
* **[host_iface_list](host_iface_list.md)** => list all the interfaces in Device Manager
* **[host_iface_count](host_iface_count.md)** => count the number of interfaces in Device Manager
* **[host_iface_info](host_iface_info.md)** => get information about an interface in Device Manager
* **[host_iface_delete](host_iface_delete.md)** => delete an interface in Device Manager

### Device Manager Links between Interfaces/Ports
* **[host_link_create](host_link_create.md)** => add a link between 2 devices of Device Manager
* **[host_link_update](host_link_update.md)** => update a link between 2 devices of Device Manager
* **[host_link_list](host_link_list.md)** => list all the links between interfaces in Device Manager
* **[host_link_count](host_link_count.md)** => count the number of links in Device Manager
* **[host_link_info](host_link_info.md)** => get information about a link between interfaces in Device Manager
* **[host_link_delete](host_link_delete.md)** => delete a link between 2 interfaces in Device Manager

