# Method dhcp_range6_create

## Description
	Add a DHCP6 range6

## Mandatory Input Parameters
	(dhcprange6_start_addr && dhcprange6_end_addr && (dhcpscope6_id || dhcp6_id || dhcp6_name || hostaddr))

## Input Parameters
	* dhcp6_id: type: >0
	* dhcp6_name: type: string, max length: 255
	* hostaddr: type: ipv4_addr
	* dhcpscope6_name: type: string, max length: 128
	* dhcpscope6_id: type: >=0
	* dhcprange6_id: type: >0
	* dhcprange6_start_addr: type: ipv6_addr
	* dhcprange6_end_addr: type: ipv6_addr
	* dhcprange6_acl: type: string, max length: 4000
	* dhcprange6_class_name: type: string, max length: 128, default: , can be empty: true
	* dhcprange6_class_parameters: type: string, default: , can be empty: true
	* add_flag: type: enum, default: new_edit, values: new_edit,new_only,edit_only
	* class_parameters_to_delete: type: string, can be empty: true
	* dhcprange6_class_parameters_properties: type: string, can be empty: true
	* apply_write_data_add_update: type: bool, default: 1
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