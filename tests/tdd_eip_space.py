# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2019-07-06 18:56:38 alex>
#

"""test file for the eip advance suite package, require an SDS to be available
and set in data_sample file
this file is used to tdd"""

import logging
import sys

from SOLIDserverRest.Exception import SDSInitError, SDSRequestError
from SOLIDserverRest.Exception import SDSAuthError, SDSError
from SOLIDserverRest.Exception import SDSEmptyError

try:
    from tests.data_sample import *
except:
    from .data_sample import *

from .context import sdsadv

def test_set_space_empty():
    """create a space object"""
    space = sdsadv.Space()
    obj_string = str(space)
    logging.debug(obj_string)

def test_refresh_space_not_connected():
    """create empty space and do a refresh"""
    space = sdsadv.Space()
    try:
        space.refresh()
    except SDSInitError:
        return

    assert None, "refresh on non connected space should raise an exc"

def test_refresh_space_local():
    """create empty space and do a refresh"""
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

    space = sdsadv.Space(sds=sds, name="Local")
    space.refresh()

def test_refresh_space_with_classparams():
    """refresh a space with class params"""
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

    space = sdsadv.Space(sds=sds, name="t01")
    space.refresh()

def test_refresh_space_not_found():
    """lookup for a non existant space"""
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

    space = sdsadv.Space(sds=sds, name="not_known")
    try:
        space.refresh()
    except SDSEmptyError:
        return

    assert None, "should not be able to refresh unknown space"



