# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2021-08-25 16:08:30 alex>
#

"""test file for DNS records

* test_create_dns_rr_object
* test_dns_rr_A_smart
* test_dns_rr_20xA_smart
* test_dns_rr_A_srv
* test_dns_rr_10xA_srv
* test_dns_rr_200xA_async_srv

start DNS in docker for test:
 sudo iptables -P FORWARD ACCEPT
 sudo sysctl net.ipv4.conf.all.forwarding=1
 docker run --rm -d eip-package-dns

"""

import logging
import sys
import uuid
import datetime
import time
import random

from SOLIDserverRest.Exception import (SDSInitError, SDSRequestError,
                                       SDSAuthError, SDSError, SDSDeviceIfError,
                                       SDSEmptyError, SDSSpaceError,
                                       SDSDeviceError, SDSDeviceNotFoundError,
                                       SDSDNSError,
                                       SDSDNSAlreadyExistingError,
                                       SDSDNSCredentialsError)

from .context import sdsadv
from .context import _connect_to_sds
from .adv_basic import *
from .dns_requester import DNSRequester

try:
    from tests.data_sample import *
except:
    from .data_sample import *


ZONE_NAME = "tdd-12345678.labo"
SMART_NAME = "tdd-12345678.labo"

DNS = DNSRequester()
DNS.setServer("192.168.24.230")


# -------------------------------------------------------
def _dns_create_srv(sds):
    """create a dns server or return existing one"""
    global DNS
    
    dns_name = DNS_SRV01_NAME

    dns = sdsadv.DNS(name=dns_name, sds=sds)
    dns.set_type('ipm')
    dns.set_ipv4(DNS_SRV01_IP)
    dns.set_ipm_credentials('admin', 'admin')
    try:
        dns.create()
    except SDSError:
        dns.refresh()

    DNS.setServer(DNS_SRV01_IP)

    return dns


# -------------------------------------------------------
def _dns_create_smart(sds, random_name=False):
    """create a dns smart or return existing one"""

    if random_name:
        dns_name = "tdd-{}.labo".format(str(uuid.uuid4())[0:8])
    else:
        dns_name = SMART_NAME

    dns = sdsadv.DNS(name=dns_name, sds=sds)
    dns.set_type('vdns', 'single')
    try:
        dns.create()
    except SDSError:
        dns.refresh()

    return dns

# -------------------------------------------------------
def _dns_create_zone(sds, dns=None, random_name=False):
    # coverage
    if random_name:
        name = "tdd-{}.labo".format(str(uuid.uuid4())[0:8])
    else:
        name = ZONE_NAME

    try:
        dns_zone = sdsadv.DNS_zone()
        dns_zone.create()
        assert None, "no connection"
    except SDSInitError:
        pass

    dns_zone = sdsadv.DNS_zone(sds=sds, name=name)

    dns_zone.set_dns(dns)
    dns_zone.set_type(dns_zone.TYPE_MASTER)
    try:
        dns_zone.create()
    except SDSDNSError:
        dns_zone.refresh()

    # logging.info(dns_zone)

    return dns_zone

# -------------------------------------------------------
def test_create_dns_rr_object():
    dns_rr = sdsadv.DNS_record()
    dns_rr = sdsadv.DNS_record(class_params = {'key': 'value'})

# -------------------------------------------------------
def test_dns_rr_A_val_smart():
    sds = _connect_to_sds()

    dns_srv = _dns_create_smart(sds)
    dns_zone = _dns_create_zone(sds, dns_srv)

    name = "{}.{}".format(str(uuid.uuid4())[0:8],
                          dns_zone.name)
    dns_rr = sdsadv.DNS_record(sds, name)
    
    dns_rr.set_zone(dns_zone)
    dns_rr.set_type('A')

    try:
        dns_rr.create()
    except SDSDNSError:
        pass

    dns_rr.set_values(['127.1.2.3'])
    dns_rr.create()

    # logging.info(dns_rr)

    dns_rr.delete()
    dns_zone.delete()
    dns_srv.delete()

# -------------------------------------------------------
def test_dns_rr_A_smart():
    sds = _connect_to_sds()

    dns_srv = _dns_create_smart(sds)
    dns_zone = _dns_create_zone(sds, dns_srv)

    name = "{}.{}".format(str(uuid.uuid4())[0:8],
                          dns_zone.name)
    dns_rr = sdsadv.DNS_record(sds, name)
    
    dns_rr.set_zone(dns_zone)
    dns_rr.set_type('A', ip='127.1.2.3')

    dns_rr.create()

    # logging.info(dns_rr)

    dns_rr.delete()
    dns_zone.delete()
    dns_srv.delete()

# -------------------------------------------------------
def test_dns_rr_types_smart():
    sds = _connect_to_sds()
    dns_srv = _dns_create_smart(sds, random_name=True)
    dns_zone = _dns_create_zone(sds, dns_srv, random_name=True)

    records = [
        { 'name': "MX-foo.{}".format(dns_zone.name),
          'type': "MX",
          'v1': '10',
          'v2': 'mail1.foo'
        },
        { 'name': "MX-foo.{}".format(dns_zone.name),
          'type': "MX",
          'v1': '20',
          'v2': 'mail2.foo'
        },
        { 'name': "A-{}.{}".format(str(uuid.uuid4())[0:8],
                                   dns_zone.name),
          'type': "A",
          'v1': create_rnd_ipv4(),
        },
        { 'name': "AAAA-{}.{}".format(str(uuid.uuid4())[0:8],
                                      dns_zone.name),
          'type': "AAAA",
          'v1': create_rnd_ipv6(),
        },
        { 'name': "TXT-{}.{}".format(str(uuid.uuid4())[0:8],
                                   dns_zone.name),
          'type': "TXT",
          'v1': 'text test for TXT Record, v=1',
        },
        { 'name': "NS-{}.{}".format(str(uuid.uuid4())[0:8],
                                   dns_zone.name),
          'type': "NS",
          'v1': 'ns99.foo',
        },
        { 'name': "CNAME-{}.{}".format(str(uuid.uuid4())[0:8],
                                   dns_zone.name),
          'type': "CNAME",
          'v1': 'foo99.foo',
        },
        
    ]

    for _rr in records:
        # logging.info("create record type %s",_rr['type'])

        for _v in ['v2', 'v3', 'v4', 'v5', 'v6', 'v7']:
            if _v not in _rr:
                _rr[_v] = None
                
        dns_rr = sdsadv.DNS_record(sds, _rr['name'])
        dns_rr.set_zone(dns_zone)
        dns_rr.set_type(_rr['type'])
        dns_rr.set_values([_rr['v1'], _rr['v2']])

        dns_rr.create()

        # logging.info(dns_rr)
        _rr['object'] = dns_rr

    for _rr in records:    
        _rr['object'].delete(sync=True)
        
    dns_zone.delete(sync=True)
    dns_srv.delete()



# -------------------------------------------------------
def test_dns_rr_20xA_smart():
    sds = _connect_to_sds()

    dns_srv = _dns_create_smart(sds)
    dns_zone = _dns_create_zone(sds, dns_srv)

    for i in range(20):
        name = "{}.{}".format(str(uuid.uuid4())[0:8],
                              dns_zone.name)
        dns_rr = sdsadv.DNS_record(sds, name)

        dns_rr.set_zone(dns_zone)
        dns_rr.set_type('A', ip='127.1.2.{}'.format(i))

        dns_rr.create()

        # logging.info(dns_rr)

        dns_rr.delete()
        
    dns_zone.delete()
    dns_srv.delete()


# -------------------------------------------------------
def test_dns_rr_A_srv():
    sds = _connect_to_sds()

    dns_srv = _dns_create_srv(sds)
    dns_zone = _dns_create_zone(sds, dns_srv)

    name = "{}.{}".format(str(uuid.uuid4())[0:8],
                          dns_zone.name)
    dns_rr = sdsadv.DNS_record(sds, name)
    
    dns_rr.set_zone(dns_zone)
    dns_rr.set_type('A', ip='127.1.2.3')
    dns_rr.set_ttl(64)

    dns_rr.create()

    # logging.info(dns_rr)

    dns_check = DNS.simple(name)
    # logging.info(dns_check)
    
    if dns_check['dns-error'] != 'no-error':
        logging.error(dns_rr)
        logging.error(dns_check)
        assert None, "DNS query validation failed"

    if dns_check['dns-ttl'] != 64:
        logging.error(dns_rr)
        logging.error(dns_check)
        assert None, "DNS query validation failed: bad ttl"

    if dns_check['dns-response'] != '127.1.2.3':
        logging.error(dns_rr)
        logging.error(dns_check)
        assert None, "DNS query validation failed: bad value"
        
    dns_rr.delete()
    dns_zone.delete()
    dns_srv.delete()

# -------------------------------------------------------
def test_dns_rr_10xA_srv():
    sds = _connect_to_sds()

    dns_srv = _dns_create_srv(sds)
    dns_zone = _dns_create_zone(sds, dns_srv)

    for i in range(10):
        name = "{}.{}".format(str(uuid.uuid4())[0:8],
                              dns_zone.name)
        dns_rr = sdsadv.DNS_record(sds, name)

        dns_rr.set_zone(dns_zone)
        dns_rr.set_type('A', ip='127.1.2.{}'.format(i))
        dns_rr.set_ttl(64+i)

        dns_rr.create()

        # logging.info(dns_rr)

        dns_check = DNS.simple(name)

        if dns_check['dns-error'] != 'no-error':
            logging.error(dns_rr)
            logging.error(dns_check)
            assert None, "DNS query validation failed"

        if dns_check['dns-ttl'] != 64+i:
            logging.error(dns_rr)
            logging.error(dns_check)
            assert None, "DNS query validation failed: bad ttl"

        if dns_check['dns-response'] != '127.1.2.{}'.format(i):
            logging.error(dns_rr)
            logging.error(dns_check)
            assert None, "DNS query validation failed: bad value"

        dns_rr.delete(sync=False)

    dns_zone.delete()
    dns_srv.delete()

# -------------------------------------------------------
def test_dns_rr_200xA_async_srv():
    sds = _connect_to_sds()

    # logging.info('create server')
    dns_srv = _dns_create_srv(sds)
    # logging.info('create zone')    
    dns_zone = _dns_create_zone(sds, dns_srv)

    now = time.time()
    
    adns_rr = []

    # logging.info('create RRs')
    for i in range(200):
        name = "{}.{}".format(str(uuid.uuid4())[0:8],
                              dns_zone.name)
        dns_rr = sdsadv.DNS_record(sds, name)

        dns_rr.set_zone(dns_zone)
        dns_rr.set_type('A', ip='127.1.2.{}'.format(i))
        dns_rr.set_ttl(64+i)

        dns_rr.create(sync=False)

        # logging.info(dns_rr)

        adns_rr.append({
            'name': name,
            'ttl': 64+i,
            'value': '127.1.2.{}'.format(i),
            'object': dns_rr
        })

    for rr in adns_rr:
        rr['object'].refresh()
        
        dns_check = DNS.simple(rr['name'])

        if dns_check['dns-error'] != 'no-error':
            logging.error(dns_rr)
            logging.error(dns_check)
            assert None, "DNS query validation failed"

        if dns_check['dns-ttl'] != rr['ttl']:
            logging.error(dns_rr)
            logging.error(dns_check)
            assert None, "DNS query validation failed: bad ttl"

        if dns_check['dns-response'] != rr['value']:
            logging.error(dns_rr)
            logging.error(dns_check)
            assert None, "DNS query validation failed: bad value"

        # logging.info(" checked RR %s", rr['name'])

    # logging.info(" elapsed = %d", time.time()-now)

    # refresh object by query
    for rr in adns_rr:
        dns_rr = sdsadv.DNS_record(sds, rr['name'])
        
        dns_check = DNS.simple(rr['name'])
        dns_rr.set_zone(dns_zone)
        dns_rr.set_type('A')

        dns_rr.refresh()

        # logging.info(" found RR %s", dns_rr)

    # logging.info('delete RRs')
    for rr in adns_rr[:-1]:
        # logging.info(' del %s', rr['name'])
        rr['object'].delete(sync=False)

    # logging.info(' del last %s', adns_rr[-1]['name'])                   
    adns_rr[-1]['object'].delete(sync=True)
        
    # logging.info('delete zone %s', dns_zone.name)
    dns_zone.delete(sync=True)

    # logging.info('delete server %s', dns_srv.name)
    dns_srv.delete()
    
