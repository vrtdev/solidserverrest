# Method dns_view_param_create

## Description
	Add/Modify options on view

## Mandatory Input Parameters
	(dnsview_id && param_key)

## Input Parameters
	* dnsview_id: type: >0
	* param_key: type: string, max length: 64
	* is_array: type: bool, default: 0
	* param_value: type: string, max length: 200000
	* add_flag: type: enum, default: new_edit, values: new_edit,new_only,edit_only

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