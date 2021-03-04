# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2020-12-01 21:14:33 alex>
#

"""test file for DNS

* test_dns_refresh
* test_dns_new_object
* test_dns_create_err_nosds
* test_dns_create_err_type
* test_dns_create_err_add
* test_dns_create_err_credentials
* test_dns_refresh_ukn
* test_dns_create
* test_dns_create_class
* test_dns_create_duplicate
* test_dns_delete_not_connected
* test_dns_update_not_connected
* test_dns_delete_no_id
* test_dns_update_no_id
* test_dns_refresh_not_connected
* test_dns_create_forward
* test_dns_create_recursion

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
def test_dns_refresh_ukn():
    """refresh an inexistant dns server"""

    dns_name = DNS_SRV01_NAME

    sds = _connect_to_sds()
    dns = sdsadv.DNS(name=dns_name, sds=sds)
    try:
        dns.refresh()
        assert None, "refresh inexistant server should fail"
    except SDSDNSError:
        None


# -------------------------------------------------------
def test_dns_refresh():
    """create a dns server"""

    dns_name = DNS_SRV01_NAME

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


# -------------------------------------------------------
def test_dns_create_class():
    """create a dns server with class params"""

    dns_name = DNS_SRV01_NAME

    sds = _connect_to_sds()

    params = {
        'key1': 'ok',
        'key2': 12,
        'date': datetime.datetime.now()
    } 

    dns = sdsadv.DNS(name=dns_name,
                     sds=sds,
                     class_params=params)
    dns.set_type('ipm')
    dns.set_ipv4(DNS_SRV01_IP)
    dns.set_ipm_credentials('admin', 'admin')
    try:
        dns.create()
    except SDSError:
        assert None, "cannot create DNS"

    dns01 = str(dns)

    dns = sdsadv.DNS(name=dns_name, sds=sds)
    dns.refresh()

    dns02 = str(dns)

    if dns01 != dns02:
        assert None, "bad refresh state"
    
    dns.delete()

# -------------------------------------------------------
def test_dns_create_duplicate():
    """create a dns server and recreate the same one"""

    dns_name = DNS_SRV01_NAME

    sds = _connect_to_sds()
    dns = sdsadv.DNS(name=dns_name, sds=sds)
    dns.set_type('ipm')
    dns.set_ipv4(DNS_SRV01_IP)
    dns.set_ipm_credentials('admin', 'admin')
    try:
        dns.create()
    except SDSError:
        assert None, "cannot create DNS"

    dns2 = sdsadv.DNS(name=dns_name, sds=sds)
    dns2.set_type('ipm')
    dns2.set_ipv4(DNS_SRV01_IP)
    dns2.set_ipm_credentials('admin', 'admin')
    try:
        dns2.create()
        assert None, "create DNS as duplicate"
    except SDSError:
        None

    dns.delete()


# -------------------------------------------------------
def test_dns_delete_not_connected():
    """delete a dns server without connexion"""

    dns_name = DNS_SRV01_NAME

    dns = sdsadv.DNS(name=dns_name)
    try:
        dns.delete()
        assert None, "delete DNS with duplicate should not be possible"
    except SDSDNSError:
        None


# -------------------------------------------------------
def test_dns_update_not_connected():
    """update a dns server without connexion"""

    dns_name = DNS_SRV01_NAME

    dns = sdsadv.DNS(name=dns_name)
    try:
        dns.update()
        assert None, "update DNS with duplicate should not be possible"
    except SDSDNSError:
        None


# -------------------------------------------------------
def test_dns_delete_no_id():
    """delete a dns server without refresh/create"""

    dns_name = DNS_SRV01_NAME
    sds = _connect_to_sds()
    dns = sdsadv.DNS(name=dns_name, sds=sds)
    try:
        dns.delete()
        assert None, "delete DNS without id should not be possible"
    except SDSDNSError:
        None


# -------------------------------------------------------
def test_dns_update_no_id():
    """update a dns server without refresh/create"""

    dns_name = DNS_SRV01_NAME
    sds = _connect_to_sds()
    dns = sdsadv.DNS(name=dns_name, sds=sds)
    try:
        dns.update()
        assert None, "update DNS without id should not be possible"
    except SDSDNSError:
        None


# -------------------------------------------------------
def test_dns_refresh_not_connected():
    """refresh a dns server without connexion"""

    dns_name = DNS_SRV01_NAME

    dns = sdsadv.DNS(name=dns_name)
    try:
        dns.refresh()
        assert None, "refresh DNS with duplicate should not be possible"
    except SDSDNSError:
        None


# -------------------------------------------------------
def test_dns_create_forward():
    """create a dns server"""

    dns_name = DNS_SRV01_NAME

    sds = _connect_to_sds()
    dns = sdsadv.DNS(name=dns_name, sds=sds)
    dns.set_type('ipm')
    dns.set_ipv4(DNS_SRV01_IP)
    dns.set_ipm_credentials('admin', 'admin')
    try:
        dns.create()
    except SDSError:
        assert None, "cannot create DNS"

    dns.set_forward('first', ['1.1.1.3', '1.1.1.4'])
    dns.update()
    
    dns2 = sdsadv.DNS(name=dns_name, sds=sds)
    dns2.refresh()

    if str(dns) != str(dns2):
        assert None, "forwarder not taken into account"

    dns.set_forward()
    dns.update()
    
    dns2 = sdsadv.DNS(name=dns_name, sds=sds)
    dns2.refresh()

    if str(dns) != str(dns2):
        assert None, "forwarder suppress not taken into account"

    dns.delete()


# -------------------------------------------------------
def test_dns_create_recursion():
    """create a dns server and set the recursion mode on and off"""

    dns_name = DNS_SRV01_NAME

    sds = _connect_to_sds()
    dns = sdsadv.DNS(name=dns_name, sds=sds)
    dns.set_type('ipm')
    dns.set_ipv4(DNS_SRV01_IP)
    dns.set_ipm_credentials('admin', 'admin')
    dns.set_forward()
    try:
        dns.create()
    except SDSError:
        assert None, "cannot create DNS"
    
    dns.set_recursion(False)
    dns.update()
    
    dns2 = sdsadv.DNS(name=dns_name, sds=sds)
    dns2.refresh()

    if str(dns) != str(dns2):
        assert None, "forwarder not taken into account"

    if dns2.params['dns_recursion'] != "no":
        logging.info(dns2)
        assert None, "recursion not set"
        
    dns.set_recursion(True)
    dns.update()
    
    dns2 = sdsadv.DNS(name=dns_name, sds=sds)
    dns2.refresh()

    if str(dns) != str(dns2):
        assert None, "forwarder suppress not taken into account"

    if dns2.params['dns_recursion'] != "yes":
        logging.info(dns2)
        assert None, "recursion not set"

    dns.delete()
