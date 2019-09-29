# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2019-09-22 15:54:35 alex>
#

"""test file for the eip advance suite package, require an SDS to be available
and set in data_sample file
this file is used to tdd"""

import logging
import sys

from SOLIDserverRest.Exception import SDSInitError, SDSRequestError, SDSAuthError, SDSError

if sys.version_info[0] == 3:
    try:
        from tests.data_sample import *
    except:
        from .data_sample import *
else:
    try:
        from data import *
    except:
        from data_sample import *

from .context import sdsadv

# ------ SDS connection ---------------------
def test_create_sds_basic():
    """create a basic connection to a SOLIDserver"""
    sds = sdsadv.SDS()
    class_string = str(sds)
    logging.debug(class_string)

def test_create_sds_basic_initip():
    """create a basic connection to a SOLIDserver"""
    sds = sdsadv.SDS(ip_address=SERVER)
    logging.debug(sds)

def test_create_sds_valid_ip():
    """create a connection to a SOLIDserver with an active server"""
    sds = sdsadv.SDS()
    sds.set_server_ip(SERVER)
    logging.debug(sds)

def test_create_sds_bad_ip():
    """create a connection to a SOLIDserver with a bad ip address format"""
    sds = sdsadv.SDS()
    try:
        sds.set_server_ip('192.168.56.254.test')
    except SDSInitError:
        return
    assert None, "should have raised an error on bad IP address"

def test_create_sds_bad_not_responsive_ip():
    """create a connection to a SOLIDserver with a bad ip address format"""
    sds = sdsadv.SDS()
    sds.set_server_ip('192.168.56.1')
    sds.set_credentials(user=USER, pwd=PWD)
    try:
        sds.connect(timeout=0.01)
    except SDSError:
        None

def test_create_sds_withuser():
    """create a basic connection to a SOLIDserver"""
    sds = sdsadv.SDS(user=USER, pwd=PWD)
    logging.debug(sds)

def test_create_sds_set_user():
    """create a connection to a SOLIDserver with an active server with user"""
    sds = sdsadv.SDS()
    sds.set_server_ip(SERVER)

    try:
        sds.set_credentials()
        assert None, "should have raised an error on no credentials"
    except SDSInitError:
        None

    sds.set_credentials(user=USER, pwd=PWD)
    logging.debug(sds)

def test_create_sds_set_baduser():
    """create a connection to a SOLIDserver with an active server with wrong user"""
    sds = sdsadv.SDS()
    sds.set_server_ip(SERVER)
    sds.set_credentials(user=USER, pwd="error")
    try:
        sds.connect()
    except SDSAuthError as e:
        return

    assert None, "should have raised an error on bad credentials"

def test_create_sds_connect_wo_user():
    """create a connection to a SOLIDserver without user"""
    sds = sdsadv.SDS()
    sds.set_server_ip(SERVER)
    try:
        sds.connect()
    except SDSInitError as e:
        return

    assert None, "should have raised an error on no credentials"

def test_create_sds_connect_wo_ip():
    """create a connection to a SOLIDserver without ip"""
    sds = sdsadv.SDS()
    sds.set_credentials(user=USER, pwd=PWD)
    try:
        sds.connect()
    except SDSInitError as e:
        return

    assert None, "should have raised an error on no ip"

def test_basic_auth():
    """create a connection to a SOLIDserver with basic auth"""
    sds = sdsadv.SDS()
    sds.set_server_ip(SERVER)
    sds.set_credentials(user=USER, pwd=PWD)
    sds.connect()
    sds.connect() # for cache on the version
    class_string = str(sds)
    logging.debug(class_string)
    sds = None


def test_basic_auth_with_cert():
    """create a connection to a SOLIDserver with basic auth and server certificate for check"""
    sds = sdsadv.SDS()
    sds.set_server_ip(SERVER)
    sds.set_credentials(user=USER, pwd=PWD)
    try:
        sds.connect(method="basicauth", cert_file_path="ca.crt")
    except SDSRequestError:
        logging.debug(e)
        assert None, "certifiate validation error"
    except SDSInitError as e:
        logging.debug(e)
        assert None, "connection error, probable certificate issue"

    logging.debug(sds)

def test_native_auth():
    """create a connection to a SOLIDserver with native auth"""
    sds = sdsadv.SDS()
    sds.set_server_ip(SERVER)
    sds.set_credentials(user=USER, pwd=PWD)
    sds.connect(method="native")
    logging.debug(sds)

#----
def test_query_timeout():
    sds = sdsadv.SDS()
    sds.set_server_ip(SERVER)
    sds.set_credentials(user=USER, pwd=PWD)
    sds.connect(method="native")

    sds.query("ip_site_count", timeout=2)
