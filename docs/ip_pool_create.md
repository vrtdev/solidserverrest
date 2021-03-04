# Method ip_pool_create

## Description
	Add/modify an IPv4 pool

## Mandatory Input Parameters
	(start_addr && (end_addr || pool_size) && (subnet_id || site_id || site_name))

## Input Parameters
	* site_id: type: >0
	* site_name: type: string, max length: 128
	* subnet_id: type: >0
	* pool_id: type: >0
	* pool_name: type: string, max length: 128, default: 
	* start_addr: type: ipv4_addr
	* end_addr: type: ipv4_addr
	* pool_size: type: >0
	* pool_class_name: type: string, max length: 128, default: , can be empty: true
	* pool_class_parameters: type: string, default: , can be empty: true
	* pool_read_only: type: bool, default: 0, can be empty: true
	* add_flag: type: enum, default: new_edit, values: new_edit,new_only,edit_only
	* class_parameters_to_delete: type: string, can be empty: true
	* pool_class_parameters_properties: type: string, can be empty: true
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