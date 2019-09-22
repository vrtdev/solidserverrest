# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2019-09-22 16:02:01 alex>
#

"""test file for the eip advance suite package, require an SDS to be available
and set in data_sample file
this file is used to tdd

scenario:
"""

import logging
import sys
import uuid
import datetime

from SOLIDserverRest.Exception import SDSInitError, SDSRequestError
from SOLIDserverRest.Exception import SDSAuthError, SDSError
from SOLIDserverRest.Exception import SDSEmptyError, SDSSpaceError

try:
    from tests.data_sample import *
except:
    from .data_sample import *

from .context import sdsadv

# -------------------------------------------------------
def test_space_set_empty():
    """create a space object"""
    space = sdsadv.Space()
    obj_string = str(space)
    logging.debug(obj_string)

# -------------------------------------------------------
def test_space_refresh_not_connected():
    """create empty space and do a refresh"""
    space = sdsadv.Space()
    try:
        space.refresh()
    except SDSInitError:
        return

    assert None, "refresh on non connected space should raise an exc"

# -------------------------------------------------------
def test_space_refresh_local():
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

# -------------------------------------------------------
def test_space_refresh_with_classparams():
    """refresh a space with class params
    TODO: suppress this test"""
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
    
    logging.debug(space)

# -------------------------------------------------------
def test_space_refresh_not_found():
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

# -------------------------------------------------------
def test_space_create_not_connected():
    """create new top level space w/o connection to SDS"""

    space = sdsadv.Space(name=str(uuid.uuid4()))
    try:
        space.create()
        assert None, "not catching create space not connected"
    except SDSSpaceError:
        None

# -------------------------------------------------------
def test_space_delete_not_connected():
    """delete space w/o connection to SDS"""

    space = sdsadv.Space(name=str(uuid.uuid4()))
    try:
        space.delete()
        assert None, "not catching create space not connected"
    except SDSSpaceError:
        None

# -------------------------------------------------------
def test_space_create_new():
    """create new top level space, then delete it"""
    sds = sdsadv.SDS()
    sds.set_server_ip(SERVER)
    sds.set_credentials(user=USER, pwd=PWD)

    try:
        sds.connect(method="basicauth")
    except SDSError as e:
        logging.debug(e)
        assert None, "connection error, probable certificate issue"

    space = sdsadv.Space(sds, name=str(uuid.uuid4()))
    try:
        space.create()
    except SDSSpaceError:
        assert None, "this space should not exists"
    
    # logging.info(space)

    space.delete()

# -------------------------------------------------------
def test_space_create_existing():
    """create new top level space 2 times, then delete it"""
    sds = sdsadv.SDS()
    sds.set_server_ip(SERVER)
    sds.set_credentials(user=USER, pwd=PWD)

    space_name = str(uuid.uuid4())

    try:
        sds.connect(method="basicauth")
    except SDSError as e:
        logging.debug(e)
        assert None, "connection error, probable certificate issue"

    # first creation
    space01 = sdsadv.Space(sds, name=space_name)
    try:
        space01.create()
    except SDSSpaceError:
        assert None, "this space should not exists"

    # collision creation
    space02 = sdsadv.Space(sds, name=space_name)
    try:
        space02.create()
        assert None, "this space should exists"
    except SDSSpaceError:
        None
    
    space01.delete()

# -------------------------------------------------------
def test_space_create_new_with_params():
    """create new top level space with specific class params, then delete it"""
    sds = sdsadv.SDS()
    sds.set_server_ip(SERVER)
    sds.set_credentials(user=USER, pwd=PWD)

    try:
        sds.connect(method="basicauth")
    except SDSError as e:
        logging.debug(e)
        assert None, "connection error, probable certificate issue"

    space_name = str(uuid.uuid4())
    space01 = sdsadv.Space(sds, name=space_name)

    params = {
        'key1': 'ok',
        'key2': 12,
        'date': datetime.datetime.now()
    }

    try:
        space01.create(class_params = params)
    except SDSSpaceError:
        assert None, "this space should not exists"

    check_space01 = str(space01)

    space02 = sdsadv.Space(sds, name=space_name)
    try:
        space02.refresh()
    except SDSInitError:
        return

    check_space02 = str(space02)

    if check_space02 != check_space01:
        assert None, "2 spaces are different"
    
    space01.delete()
