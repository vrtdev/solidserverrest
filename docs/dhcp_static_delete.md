# Method dhcp_static_delete

## Description
	Delete a DHCP static

## Mandatory Input Parameters

## Input Parameters
	* dhcp_id: type: >0
	* dhcp_name: type: string, max length: 255
	* hostaddr: type: ipv4_addr
	* dhcp_addr: type: ipv4_addr
	* dhcpscope_id: type: >0
	* scope_id: type: >0
	* dhcphost_id: type: >0
	* static_id: type: >0
	* dhcphost_addr: type: ipv4_addr
	* static_addr: type: ipv4_addr
	* static_ip_addr: type: ipv4_addr
	* dhcphost_mac_addr: type: mac
	* static_mac_addr: type: mac
	* dhcphost_name: type: string
	* validate_warnings: type: enum, values: accept

## Returned Values
	* errno
	* errmsg
	* msg
	* severity
	* parameters
	* param_format
	* param_value
	* ret_oid
	* ret_code


*this file is automatically generated* - date: 18 Feb 2021 19:32