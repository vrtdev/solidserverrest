# Method ip_pool6_create

## Description
	Add/modify an IPv6 pool

## Mandatory Input Parameters
	(start_addr && end_addr && (subnet6_id || site_id || site_name))

## Input Parameters
	* site_id: type: >0
	* site_name: type: string, max length: 128
	* subnet6_id: type: >0
	* pool6_id: type: >0
	* pool6_name: type: string, max length: 128, default: 
	* start_addr: type: ipv6_addr
	* end_addr: type: ipv6_addr
	* pool6_class_name: type: string, max length: 128, default: , can be empty: true
	* pool6_class_parameters: type: string, default: , can be empty: true
	* pool6_read_only: type: bool, default: 0, can be empty: true
	* add_flag: type: enum, default: new_edit, values: new_edit,new_only,edit_only
	* class_parameters_to_delete: type: string, can be empty: true
	* pool6_class_parameters_properties: type: string, can be empty: true
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