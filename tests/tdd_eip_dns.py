# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2020-07-25 19:10:56 alex>
#

"""test file for DNS

* test_dns_new_object

"""

import logging
import sys
import uuid
import datetime
import time

from SOLIDserverRest.Exception import SDSInitError, SDSRequestError
from SOLIDserverRest.Exception import SDSAuthError, SDSError, SDSDeviceIfError
from SOLIDserverRest.Exception import SDSEmptyError, SDSSpaceError
from SOLIDserverRest.Exception import SDSDeviceError, SDSDeviceNotFoundError
from SOLIDserverRest.Exception import SDSDNSError
from SOLIDserverRest.Exception import SDSDNSAlreadyExistingError
from SOLIDserverRest.Exception import SDSDNSCredentialsError

from .context import sdsadv
from .context import _connect_to_sds
from .adv_basic import *

try:
    from tests.data_sample import *
except:
    from .data_sample import *

# -------------------------------------------------------
def test_dns_new_object():
    """create a dns object"""

    dns_name = str(uuid.uuid4())+'.test'

    dns = sdsadv.DNS(name=dns_name)

    obj_string = str(dns)
    logging.debug(obj_string)

# -------------------------------------------------------
def test_dns_create_err_nosds():
    """create a dns server w/o sds"""

    dns_name = DNS_SRV01_NAME

    dns = sdsadv.DNS(name=dns_name)

    try:
        dns.create()
        assert None, 'dns creation without sds'
    except SDSInitError:
        None

# -------------------------------------------------------
def test_dns_create_err_type():
    """create a dns server w/o type"""

    dns_name = DNS_SRV01_NAME

    dns = sdsadv.DNS(name=dns_name)

    sds = _connect_to_sds()
    dns = sdsadv.DNS(name=dns_name, sds=sds)

    try:
        dns.create()
        assert None, 'dns creation without type'
    except SDSError:
        None

    try:
        dns.set_type('none')
        assert None, 'dns bad type'
    except SDSError:
        None

# -------------------------------------------------------
def test_dns_create_err_add():
    """create a dns server w/o address"""

    dns_name = DNS_SRV01_NAME

    dns = sdsadv.DNS(name=dns_name)

    sds = _connect_to_sds()
    dns = sdsadv.DNS(name=dns_name, sds=sds)
    dns.set_type('ipm')

    try:
        dns.create()
        assert None, 'dns creation without address'
    except SDSError:
        None


# -------------------------------------------------------
def test_dns_create_err_credentials():
    """create a dns server"""

    dns_name = DNS_SRV01_NAME

    dns = sdsadv.DNS(name=dns_name)

    sds = _connect_to_sds()
    dns = sdsadv.DNS(name=dns_name, sds=sds)

    dns.set_type('ipm')

    try:
        dns.set_ipv4('none')
        assert None, 'dns bad IPv4'
    except SDSDNSError:
        None
        
    dns.set_ipv4(DNS_SRV01_IP)
    
    try:
        dns.create()
        assert None, 'dns creation without credentials'
    except SDSDNSError:
        None


# -------------------------------------------------------
def test_dns_refresh():
    """create a dns server"""

    dns_name = DNS_SRV01_NAME

    dns = sdsadv.DNS(name=dns_name)
    sds = _connect_to_sds()
    dns = sdsadv.DNS(name=dns_name, sds=sds)
    dns.set_type('ipm')
    dns.set_ipv4(DNS_SRV01_IP)
    dns.set_ipm_credentials('admin', 'admin')
    try:
        dns.create()
    except SDSError:
        assert None, "cannot create DNS"

    dns01 = str(dns)

    dns = sdsadv.DNS(name=dns_name)
    sds = _connect_to_sds()
    dns = sdsadv.DNS(name=dns_name, sds=sds)
    dns.refresh()

    dns02 = str(dns)

    if dns01 != dns02:
        assert None, "bad refresh state"

    dns.delete()
    
# -------------------------------------------------------
def test_dns_create():
    """create a dns server"""

    dns_name = DNS_SRV01_NAME

    dns = sdsadv.DNS(name=dns_name)
    sds = _connect_to_sds()
    dns = sdsadv.DNS(name=dns_name, sds=sds)
    dns.set_type('ipm')
    dns.set_ipv4(DNS_SRV01_IP)
    dns.set_ipm_credentials('admin', 'admin')
    try:
        dns.create()
    except SDSError:
        assert None, "cannot create DNS"

    dns.delete()
    
