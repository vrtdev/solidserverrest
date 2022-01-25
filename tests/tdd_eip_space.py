# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2022-01-14 11:57:50 alex>
#

"""test file for the eip advance suite package, require an SDS to be available
and set in data_sample file
this file is used to tdd

scenario:
* test_space_set_empty
* test_space_refresh_not_connected
* test_space_refresh_local
* test_space_refresh_not_found
* test_space_create_not_connected
* test_space_delete_not_connected
* test_space_create_new
* test_space_create_existing
* test_space_create_new_with_params
"""

import logging
import sys
import uuid
import datetime

from SOLIDserverRest.Exception import SDSInitError, SDSRequestError
from SOLIDserverRest.Exception import SDSAuthError, SDSError
from SOLIDserverRest.Exception import SDSEmptyError, SDSSpaceError

from .context import sdsadv
from .context import _connect_to_sds

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
    sds = _connect_to_sds()

    space = sdsadv.Space(sds=sds, name="Local")
    space.refresh()

# -------------------------------------------------------
def test_space_refresh_not_found():
    """lookup for a non existant space"""
    sds = _connect_to_sds()

    space = sdsadv.Space(sds=sds, name="not_known")
    try:
        space.refresh()
    except SDSError:
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
    sds = _connect_to_sds()

    space = sdsadv.Space(sds, name=str(uuid.uuid4()))
    try:
        space.create()
    except SDSSpaceError:
        assert None, "this space should not exists"
    
    space.delete()

# -------------------------------------------------------
def test_space_create_existing():
    """create new top level space 2 times, then delete it"""
    sds = _connect_to_sds()

    space_name = str(uuid.uuid4())

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
    sds = _connect_to_sds()

    space_name = str(uuid.uuid4())
    space01 = sdsadv.Space(sds, name=space_name)

    params = {
        'key1': 'ok',
        'key2': 12,
        'date': datetime.datetime.now()
    }

    space01.set_class_params(params)

    try:
        space01.create()
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

    space_name = str(uuid.uuid4())
    space02 = sdsadv.Space(sds, name=space_name,
                           class_params = { 'key1': 'ok',
                                            'key2': 12,
                                            'date': datetime.datetime.now()})

