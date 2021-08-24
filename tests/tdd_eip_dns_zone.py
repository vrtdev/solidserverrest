# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2021-06-07 18:26:55 alex>
#

"""test file for DNS zones

* test_create_zone_object
* test_create_zone
* test_refresh_existing_zone


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

try:
    from tests.data_sample import *
except:
    from .data_sample import *

# -------------------------------------------------------
def _dns_create():
    """create a dns server or return existing one"""

    dns_name = DNS_SRV01_NAME

    sds = _connect_to_sds()
    dns = sdsadv.DNS(name=dns_name, sds=sds)
    dns.set_type('ipm')
    dns.set_ipv4(DNS_SRV01_IP)
    dns.set_ipm_credentials('admin', 'admin')
    try:
        dns.create()
    except SDSError:
        dns.refresh()

    return dns

# -------------------------------------------------------
def test_create_zone_object():
    dns_zone = sdsadv.DNS_zone()

    dns_zone = sdsadv.DNS_zone(class_params = {'key': 'value'})

# -------------------------------------------------------
def test_create_zone_object_with_type():
    dns_zone = sdsadv.DNS_zone(name="a",
                               zone_type = sdsadv.DNS_zone.TYPE_FWD)

    try:
        dns_zone = sdsadv.DNS_zone(name="b",
                                   zone_type = "ukn")
        assert None, "unkown type"
    except SDSDNSError:
        None
    
# -------------------------------------------------------
def test_simple_create_zone():
    # coverage
    name = str(uuid.uuid4())
    try:
        dns_zone = sdsadv.DNS_zone()
        dns_zone.create()
        assert None, "no connection"
    except SDSInitError:
        pass

    sds = _connect_to_sds()
    dns = _dns_create()

    dns_zone = sdsadv.DNS_zone(sds=sds, name=name)

    # use no dns server
    try:
        dns_zone.create()
        assert None, "no dns, should not create"
    except SDSDNSError:
        pass
        
    # use bad dns server
    try:
        dns_zone.set_dns("dns")
        assert None, "should not be possible to use bad dns"
    except SDSDNSError:
        dns_zone.set_dns(dns)

    # use bad zone type
    try:
        dns_zone.set_type("test")
        assert None, "bad zone type not catched"
    except SDSDNSError:
        dns_zone.set_type(dns_zone.TYPE_MASTER)
        
    dns_zone.create()

    # logging.info(dns_zone)

    dns_zone.delete()

# -------------------------------------------------------
def test_class_params():
    # init
    sds = _connect_to_sds()
    dns = _dns_create()

    # create the zone
    name = str(uuid.uuid4())
    dns_zone = sdsadv.DNS_zone(sds=sds,
                               name=name,
                               class_params = {'key': 'val'})
    dns_zone.set_dns(dns)
    dns_zone.set_type(dns_zone.TYPE_MASTER)
    dns_zone.create()

    dns_zone2 = sdsadv.DNS_zone(sds=sds, name=name)
    dns_zone2.set_dns(dns)
    dns_zone2.refresh()

    if str(dns_zone) != str(dns_zone2):
        logging.error(str(dns_zone))
        logging.error(str(dns_zone2))
        assert None, "2 zones are different vs class params"
    
    dns_zone.delete()

# -------------------------------------------------------
def test_refresh_existing_zone():
    # init
    sds = _connect_to_sds()
    dns = _dns_create()

    # create the zone
    name = str(uuid.uuid4())
    dns_zone = sdsadv.DNS_zone(sds=sds, name=name)
    dns_zone.set_dns(dns)
    dns_zone.set_type(dns_zone.TYPE_MASTER)
    dns_zone.create()

    # 
    dns_zone2 = sdsadv.DNS_zone(sds=sds, name=name)
    dns_zone2.set_dns(dns)
    
    try:
        dns_zone2.refresh()
    except SDSError:
        dns_zone.delete()        
        assert None, "refresh on existant zone should not fail"

    dns_zone.delete()

# -------------------------------------------------------
def test_refresh_nonexisting_zone():
    sds = _connect_to_sds()

    dns = _dns_create()
        
    dns_zone = sdsadv.DNS_zone(sds=sds, name=str(uuid.uuid4()))
    dns_zone.set_dns(dns)
    
    try:
        dns_zone.refresh()
        assert None, "refresh on nonexistant zone should not fail"        
    except SDSError:
        None

# -------------------------------------------------------
def test_create_multi_zone_async():
    sds = _connect_to_sds()
    dns = _dns_create()

    azones = []
    
    for i in range(5):
        name = str(uuid.uuid4())
    
        dns_zone = sdsadv.DNS_zone(sds=sds, name=name)
        dns_zone.set_dns(dns)
        dns_zone.set_type(dns_zone.TYPE_MASTER)
        
        dns_zone.create(sync=False)

        # logging.info(dns_zone)
        
        azones.append(dns_zone)

    for zone in azones:
        zone.refresh()
        # logging.info(zone)

    for zone in azones:
        zone.delete(sync=False)
        
# -------------------------------------------------------
def test_create_zone_reverse():
    sds = _connect_to_sds()
    dns = _dns_create()

    name = '0.'
    name += '.'.join('%s' % random.randint(1, 128) for i in range(2))
    name += '.10.in-addr.arpa'
    
    dns_zone = sdsadv.DNS_zone(sds=sds, name=name)
    dns_zone.set_dns(dns)
    dns_zone.set_type(dns_zone.TYPE_MASTER)
    dns_zone.set_is_reverse(True)
        
    dns_zone.create()

    # logging.info(dns_zone)

    dns_zone.delete()
