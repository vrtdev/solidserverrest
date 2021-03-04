# Method vlm_domain_update

## Description
	Add/modify a VLAN Domain

## Mandatory Input Parameters

## Input Parameters
	* vlmdomain_id: type: >0
	* vlmdomain_name: type: string, max length: 128
	* vlmdomain_description: type: string, max length: 128, default: 
	* vlmdomain_start_vlan_id: type: >0, default: 1
	* vlmdomain_end_vlan_id: type: >0
	* support_vxlan: type: bool, default: 0
	* vlmdomain_class_name: type: string, max length: 128, default: , can be empty: true
	* vlmdomain_class_parameters: type: string, default: , can be empty: true
	* add_flag: type: enum, default: new_edit, values: new_edit,new_only,edit_only
	* class_parameters_to_delete: type: string, can be empty: true
	* vlmdomain_class_parameters_properties: type: string, can be empty: true
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