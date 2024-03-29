# Method dhcp_range_create

## Description
	Add a DHCP range

## Mandatory Input Parameters
	(dhcprange_start_addr && dhcprange_end_addr && (dhcpscope_id || dhcp_id || dhcp_name || hostaddr))

## Input Parameters
	* dhcp_id: type: >0
	* dhcp_name: type: string, max length: 255
	* hostaddr: type: ipv4_addr
	* dhcp_addr: type: ipv4_addr
	* dhcpscope_name: type: string, max length: 255
	* dhcpscope_id: type: >=0
	* scope_id: type: >=0
	* dhcprange_id: type: >0
	* start_addr: type: ipv4_addr
	* dhcprange_start_addr: type: ipv4_addr
	* end_addr: type: ipv4_addr
	* dhcprange_end_addr: type: ipv4_addr
	* acl: type: string, max length: 4000
	* dhcprange_name: type: string, max length: 32
	* dhcprange_acl: type: string, max length: 4000
	* dhcprange_class_name: type: string, max length: 128, default: , can be empty: true
	* dhcprange_class_parameters: type: string, default: , can be empty: true
	* add_flag: type: enum, default: new_edit, values: new_edit,new_only,edit_only
	* class_parameters_to_delete: type: string, can be empty: true
	* dhcprange_class_parameters_properties: type: string, can be empty: true
	* apply_write_data_add_update: type: bool, default: 1
	* validate_warnings: type: enum, values: accept

## Returned Values
	* ret_oid
	* errno
	* errmsg
	* msg
	* severity
	* parameters
	* param_format
	* param_value
	* ret_code


*this file is automatically generated* - date: 24 Feb 2023 13:16