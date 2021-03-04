# Method dns_view_create

## Description
	Add a dns view

## Mandatory Input Parameters
	(dnsview_name && (dns_id || dns_name || hostaddr))

## Input Parameters
	* dns_id: type: >0
	* dns_name: type: string, max length: 255
	* hostaddr: type: ipv4_addr
	* dns_addr: type: ipv4_addr
	* dnsview_order: type: >=0, default: 0
	* dnsview_name: type: string, max length: 63
	* dnsview_match_clients: type: string_array, default: 
	* dnsview_match_to: type: string_array, default: 
	* dnsview_allow_transfer: type: string_array
	* dnsview_allow_query: type: string_array
	* dnsview_allow_recursion: type: string_array
	* dnsview_recursion: type: enum, default: yes, values: yes,no
	* dnsview_id: type: >0
	* dnsview_class_name: type: string, max length: 128, default: , can be empty: true
	* dnsview_class_parameters: type: string, default: , can be empty: true
	* add_flag: type: enum, default: new_edit, values: new_edit,new_only,edit_only
	* class_parameters_to_delete: type: string, can be empty: true
	* dnsview_class_parameters_properties: type: string, can be empty: true
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