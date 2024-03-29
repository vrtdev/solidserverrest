# Method dns_server_update

## Description
	Add a DNS server

## Mandatory Input Parameters

## Input Parameters
	* dns_id: type: >0
	* dns_name: type: string
	* dns_type: type: enum, default: , values: ipm,microsoft,windns,msdaemon,other,vdns,nsd,unbound,aws,azure
	* hostaddr: type: ipv4_addr, can be empty: true
	* dns_comment: type: string
	* dns_class_name: type: string, max length: 128, default: , can be empty: true
	* dns_class_parameters: type: string, default: , can be empty: true
	* vdns_list: type: string_array
	* vdns_dns_group_role: type: string_array
	* isolated: type: bool, default: 0
	* dns_allow_transfer: type: string_array, default: any;
	* dns_allow_query: type: string_array, default: any;
	* dns_allow_query_cache: type: string_array, default: any;
	* dns_allow_recursion: type: string_array, default: any;
	* dns_recursion: type: string_array, default: yes
	* dns_forward: type: string_array, default: none
	* dns_forwarders: type: string_array
	* dns_notify: type: string_array, default: yes
	* dns_also_notify: type: string_array
	* zone: type: string
	* snmp_id: type: >0, default: 0
	* snmp_port: type: >=0
	* snmp_profile_id: type: >0
	* snmp_retry: type: >=0
	* snmp_timeout: type: >0
	* snmp_use_tcp: type: bool
	* ipmdns_protocol: type: enum, default: https, values: snmp,https
	* ipmdns_https_login: type: string
	* ipmdns_https_password: type: string
	* ipmdns_is_package: type: string
	* aws_keyid: type: string
	* aws_secret: type: string
	* aws_delegation_set: type: string, default: #
	* az_tenantid: type: string
	* az_keyid: type: string
	* az_subscriptionid: type: string
	* az_group: type: string
	* az_secret: type: string
	* ad_domain: type: string
	* ad_user: type: string
	* ad_password: type: string
	* vdns_arch: type: enum, values: masterslave,multimaster,stealth,cache,single,farm
	* vdns_ref1_dns_id: type: >=0, default: 0, can be empty: true
	* vdns_ref2_dns_id: type: >=0, default: 0, can be empty: true
	* vdns_public_ns_list: type: string_array, default: , can be empty: true
	* tsig_key_name: type: string
	* dns_key_name: type: string
	* tsig_key_value: type: string
	* dns_key_value: type: string
	* tsig_key_proto: type: string
	* dns_key_proto: type: string
	* gss_keytab_id: type: >=0, default: 0, can be empty: true
	* gss_enabled: type: bool, default: 0, can be empty: true
	* windns_use_ssl: type: bool, default: 0
	* windns_port: type: >0
	* windns_protocol: type: enum, default: plain, values: plain,soap
	* windns_login: type: string
	* windns_password: type: string, default: password
	* dns_force_hybrid: type: >=0, default: 0
	* reverse_proxy_conf: type: string
	* stat_enabled: type: string, default: U
	* stat_period: type: >0, default: 5
	* dns_cloud_private: type: string, default: 0
	* dns_vpc_list: type: string
	* add_flag: type: enum, default: new_edit, values: new_edit,new_only,edit_only
	* class_parameters_to_delete: type: string, can be empty: true
	* dns_class_parameters_properties: type: string, can be empty: true
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