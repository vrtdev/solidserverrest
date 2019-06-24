# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2019-06-23 18:26:01 alex>
#

"""test file for the eip advance suite package, require an SDS to be available
and set in data_sample file
this file is used to tdd"""

import logging
import sys

from SOLIDserverRest.Exception import SSDInitError, SSDRequestError, SSDAuthError, SSDError

try:
    from tests.data_sample import *
except:
    from .data_sample import *

from .context import sdsadv

def test_set_space_empty():
    """create a space object and populate it with the content of the SDS"""
    space = sdsadv.Space()
    obj_string = str(space)
    logging.debug(obj_string)

def test_refresh_space_not_connected():
    """create empty space and do a refresh"""
    space = sdsadv.Space()
    try:
        space.refresh()
    except SSDInitError:
        return

    assert None, "refresh on non connected space should raise an exc"

def test_refresh_space_local():
    """create empty space and do a refresh"""
    sds = sdsadv.SDS()
    sds.set_server_ip(SERVER)
    sds.set_credentials(user=USER, pwd=PWD)
    try:
        sds.connect(method="basicauth", cert_file_path="ca.crt")
    except SSDRequestError:
        logging.debug(e)
        assert None, "certifiate validation error"
    except SSDInitError as e:
        logging.debug(e)
        assert None, "connection error, probable certificate issue"

    space = sdsadv.Space(sds=sds, name="Local")
    space.refresh()

def test_refresh_space_with_classparams():
    """refresh a space with class params"""
    sds = sdsadv.SDS()
    sds.set_server_ip(SERVER)
    sds.set_credentials(user=USER, pwd=PWD)
    try:
        sds.connect(method="basicauth", cert_file_path="ca.crt")
    except SSDRequestError:
        logging.debug(e)
        assert None, "certifiate validation error"
    except SSDInitError as e:
        logging.debug(e)
        assert None, "connection error, probable certificate issue"

    space = sdsadv.Space(sds=sds, name="t01")
    space.refresh()

def test_refresh_space_not_found():
    """lookup for a non existant space"""
    sds = sdsadv.SDS()
    sds.set_server_ip(SERVER)
    sds.set_credentials(user=USER, pwd=PWD)
    try:
        sds.connect(method="basicauth", cert_file_path="ca.crt")
    except SSDRequestError:
        logging.debug(e)
        assert None, "certifiate validation error"
    except SSDInitError as e:
        logging.debug(e)
        assert None, "connection error, probable certificate issue"

    space = sdsadv.Space(sds=sds, name="not_known")
    try:
        space.refresh()
    except SSDError:
        return

    assert None, "should not be able to refresh unknown space"



