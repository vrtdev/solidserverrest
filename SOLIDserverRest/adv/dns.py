#
# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2020-07-25 19:10:07 alex>
#

"""
SOLIDserver DNS management

"""

import ipaddress
import logging

from SOLIDserverRest.Exception import SDSInitError, SDSError
from SOLIDserverRest.Exception import SDSEmptyError
from SOLIDserverRest.Exception import SDSDNSError
from SOLIDserverRest.Exception import SDSDNSAlreadyExistingError
from SOLIDserverRest.Exception import SDSDNSCredentialsError

from .class_params import ClassParams


class DNS(ClassParams):
    """ class to manipulate the SOLIDserver DNS object """

    # -------------------------------------
    def __init__(self, sds=None,
                 name=None,
                 class_params=None):
        """init the DNS object:
        - sds: object SOLIDserver, could be set afterwards
        - name: dns server name
        """

        super(DNS, self).__init__(sds, name)

        self.ipv4_addr = None
        
        self.params = {
            'aws_keyid': None,
            'dns_allow_query': None,
            'dns_allow_query_cache': None,
            'dns_allow_recursion': None,
            'dns_allow_transfer': None,
            'dns_also_notify': None,
            'dns_ans_key': None,
            'dns_class_name': None,
            'dns_comment': None,
            'dns_forward': None,
            'dns_forwarders': None,
            'dns_id': None,
            'dns_key_name': None,
            'dns_key_proto': None,
            'dns_key_value': None,
            'dns_name': None,
            'dns_notify': None,
            'dns_recursion': None,
            'dns_role': None,
            'dns_state': None,
            'dns_synching': None,
            'dns_type': None,
            'dns_version': None,
            'dnsblast_enabled': None,
            'dnsblast_status': None,
            'dnsgslb_supported': None,
            'dnsguardian_supported': None,
            'dnssec_validation': None,
            'gss_enabled': None,
            'gss_keytab_id': None,
            'ip_addr': None,
            'ipmdns_https_login': None,
            'ipmdns_https_password': None,
            'ipmdns_is_package': None,
            'ipmdns_protocol': 'https',
            'ipmdns_type': None,
            'isolated': '0',
            'ldap_domain': None,
            'ldap_password': None,
            'ldap_user': None,
            'multistatus': None,
            'querylog_state': None,
            'total_vdns_members': None,
            # 'vdns_arch': None,
            # 'vdns_members_name': None,
            'vdns_parent_arch': None,
            'vdns_parent_id': None,
            'vdns_parent_name': None,
            # 'vdns_public_ns_list': None,
        }

        if class_params is not None:
            self.set_class_params(class_params)

    # -------------------------------------
    def _get_dnsid_by_name(self, name):
        """get the DNS server ID from its name, return None if non existant"""

        try:
            rjson = self.sds.query("dns_server_list",
                                   params={
                                       "WHERE": "dns_name='{}'".
                                                format(name),
                                       **self.additional_params
                                   })
        except SDSEmptyError:
            return None

        if rjson[0]['errno'] != '0':   # pragma: no cover
            raise SDSError("errno raised")

        return rjson[0]['dns_id']
            

    # -------------------------------------
    def set_ipv4(self, ipv4=None):
        ''' set ipv4 address of the DNS server'''
        try:
            self.ipv4_addr = ipaddress.IPv4Address(ipv4)
        except ipaddress.AddressValueError:
            raise SDSDNSError(message='bad IPv4 address for DNS server')

    # -------------------------------------
    def set_type(self, type=None):
        '''set type of the DNS server'''
        if type not in ['ipm', 'msdaemon', 'ans', 'aws', 'other', 'vdns']:
            raise SDSDNSError(message='bad DNS type')

        self.params['dns_type'] = type

    # -------------------------------------
    def set_ipm_credentials(self, user, passwd):
        '''set admin credentials to talk to a ipmdns'''
        self.params['ipmdns_https_login'] = user
        self.params['ipmdns_https_password'] = passwd
        
    # -------------------------------------
    def create(self):
        """creates the DNS server"""
        if self.sds is None:
            raise SDSInitError(message="not connected")

        dns_id = self._get_dnsid_by_name(self.name)
        if dns_id is not None:
            raise SDSDNSAlreadyExistingError(message="already existant dns server")

        if self.params['dns_type'] is None:
            raise SDSDNSError(message="DNS server with bad type, use set_type")

        if self.ipv4_addr is None:
            raise SDSDNSError(message="DNS server without IP address, use set_ipv4")
        
        params = {
            'dns_name': self.name,
            'hostaddr': self.ipv4_addr,
            'dns_type': self.params['dns_type'],
            **self.additional_params
        }

        if self.params['dns_type'] == 'ipm':
            params['ipmdns_https_login'] = self.params['ipmdns_https_login']
            params['ipmdns_https_password'] = self.params['ipmdns_https_password']

        self.prepare_class_params('dns', params)

        try:
            rjson = self.sds.query("dns_server_add",
                                   params=params)
        except SDSError:   # pragma: no cover
            logging.error("create DNS server")

        if 'errno' in rjson:   # pragma: no cover
            if rjson['errno'] == '14401':
                raise SDSDNSCredentialsError(message=rjson['errmsg'])

            logging.info(rjson)
            raise SDSDNSError(message="DNS creation error: "
                              + rjson['errmsg'])

        if 'ret_oid' not in rjson[0]:   # pragma: no cover
            raise SDSDNSError(message="DNS server creation error "
                              + rjson['errmsg'])

        self.params['dns_id'] = int(rjson[0]['ret_oid'])
        self.myid = self.params['dns_id']
        self.refresh()

    # -------------------------------------
    def delete(self):
        """deletes the DNS server in the SDS"""
        if self.sds is None:
            raise SDSError(message="not connected")

        if self.myid is None:
            raise SDSError(message="missing DNS id")
        
        try:
            rjson = self.sds.query("dns_server_delete",
                                   params={
                                       'dns_id': self.myid,
                                       **self.additional_params
                                   })
            if 'errmsg' in rjson:  # pragma: no cover
                raise SDSError(message="DNS server delete error, "
                               + rjson['errmsg'])
        except SDSError:   # pragma: no cover
            raise SDSError(message="DNS server delete error")

    # -------------------------------------
    def refresh(self):
        """refresh content of the DNS from the SDS"""
        if self.sds is None:
            raise SDSInitError(message="not connected")

        if self.myid is None or self.myid == -1:
            dns_id = self._get_dnsid_by_name(self.name)
        else:
            dns_id = self.myid

        if dns_id is None:
            raise SDSEmptyError(message="non existant DNS to refresh")

        rjson = self.sds.query("dns_server_info",
                               params={
                                   "dns_id": dns_id,
                                   **self.additional_params
                               })

        if not rjson:   # pragma: no cover
            raise SDSError(message="DNS server refresh error, len of array")

        rjson = rjson[0]
        
        for label in ['dns_id',
                      'dns_role',
                      'dns_ans_key',
                      'aws_keyid',
                      'ipmdns_is_package',
                      'ipmdns_type',
                      'isolated',
                      'dns_notify',
                      'dns_also_notify',
                      'dns_allow_query_cache',
                      'dns_allow_query',
                      'dns_allow_transfer',
                      'dns_allow_recursion',
                      'dns_recursion',
                      'dns_forwarders',
                      'dns_forward',
                      'vdns_parent_id',
                      'dns_state',
                      'querylog_state',
                      'dns_synching',
                      'dns_name',
                      'dns_comment',
                      'dns_type',
                      'dns_class_name',
                      'dns_version',
                      'dns_key_name',
                      'dns_key_value',
                      'dns_key_proto',
                      'dns_hybrid',
                      'gss_keytab_id',
                      'gss_enabled',
                      'dnsblast_enabled',
                      'dnsblast_status',
                      'dnssec_validation',
                      'dnsgslb_supported',
                      'dnsguardian_supported',
                      'multistatus']:
            if label not in rjson:   # pragma: no cover
                raise SDSError("parameter {} not found in DNS server".format(label))
            self.params[label] = rjson[label]

        self.ipv4_addr = ipaddress.IPv4Address(int(rjson['ip_addr'], 16))

        self.myid = int(self.params['dns_id'])
        
        if 'dns_class_parameters' in rjson:
            self.update_class_params(rjson['dns_class_parameters'])

    # -------------------------------------
    def __str__(self):
        """return the string notation of the DNS server object"""
        return_val = "*DNS* name={}".format(self.name)

        if self.myid != -1:
            return_val += " id={}".format(self.myid)

        if self.ipv4_addr is not None:
            return_val += " ip={}".format(self.ipv4_addr)

        if self.params['dns_type'] == 'ipm':
            return_val += " ipm={}".format(str(self.params['ipmdns_type']))
        else:
            return_val += " type={}".format(str(self.params['dns_type']))

        if self.params['dns_forward'] in ['fist', 'only']:
            return_val += " forward[{}]={}".format(self.params['dns_forward'],
                                                   self.params['dns_forwarders'])

        return_val += " notify={}".format(str(self.params['dns_notify']))

        if self.params['dns_class_name'] != '':
            return_val += " class={}".format(str(self.params['dns_class_name']))

        return_val += str(super(DNS, self).__str__())

        return return_val
