# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2019-09-22 15:27:40 alex>
#

"""test file for the device manager
"""

import logging
import sys
import uuid
import datetime

from SOLIDserverRest.Exception import SDSInitError, SDSRequestError
from SOLIDserverRest.Exception import SDSAuthError, SDSError
from SOLIDserverRest.Exception import SDSEmptyError
from SOLIDserverRest.Exception import SDSDeviceError, SDSDeviceNotFoundError

try:
    from tests.data_sample import *
except:
    from .data_sample import *

from .context import sdsadv

# -------------------------------------------------------
def _connect_to_sds():
    sds = sdsadv.SDS()
    sds.set_server_ip(SERVER)
    sds.set_credentials(user=USER, pwd=PWD)

    try:
        sds.connect(method="basicauth")
    except SDSError as e:
        logging.debug(e)
        assert None, "connection error, probable certificate issue"

    return sds

# -------------------------------------------------------
def test_device_new_object():
    """create a device object"""

    device_name = str(uuid.uuid4())

    dev = sdsadv.Device(name=device_name)

    obj_string = str(dev)
    logging.debug(obj_string)

# -------------------------------------------------------
def test_device_refresh_not_connected():
    """refresh an object not connected"""

    device_name = str(uuid.uuid4())

    dev = sdsadv.Device(name=device_name)
    try:
        dev.refresh()
        assert None, "refresh and not connected should fail"
    except SDSDeviceError as e:
        return


# -------------------------------------------------------
def test_device_new_object_wo_name():
    """create a device object without name"""

    try:
        dev = sdsadv.Device()
        assert None, "assertion should be raised on device with no name"
    except SDSDeviceError:
        None

# -------------------------------------------------------
def test_device_create():
    """create a device in SDS"""

    device_name = str(uuid.uuid4())

    sds = _connect_to_sds()

    dev = sdsadv.Device(name=device_name, sds=sds)

    dev.create()
    dev.delete()

# -------------------------------------------------------
def test_device_delete_not_connected():
    """delete a device while not connected to SDS"""

    device_name = str(uuid.uuid4())

    dev = sdsadv.Device(name=device_name)
    try:
        dev.delete()
        assert None, "not detecting delete on not connected"
    except SDSDeviceError:
        None

# -------------------------------------------------------
def test_device_refresh():
    """create a device in SDS and refresh"""

    device_name = str(uuid.uuid4())

    sds = _connect_to_sds()

    dev01 = sdsadv.Device(name=device_name, sds=sds)
    dev01.create()
    del(dev01)

    dev02 = sdsadv.Device(name=device_name, sds=sds)
    dev02.refresh()

    dev02.delete()

# -------------------------------------------------------
def test_device_refresh_ukn():
    """refresh on ukn device"""

    device_name = str(uuid.uuid4())

    sds = _connect_to_sds()

    dev02 = sdsadv.Device(name=device_name, sds=sds)

    try:
        dev02.refresh()
        assert None, "not detecting refresh ukn"
    except SDSDeviceError:
        None

# -------------------------------------------------------
def test_device_refresh_destroyed():
    """refresh on destroyed device"""

    device_name = str(uuid.uuid4())

    sds = _connect_to_sds()
    dev = sdsadv.Device(name=device_name, sds=sds)
    dev.create()

    sds.query("host_device_delete",
              params={
                  'hostdev_name': device_name
              })

    try:
        dev.refresh()
        assert None, "not detecting refresh on destroyed"
    except SDSDeviceError:
        None

# -------------------------------------------------------
def test_device_create_not_connected():
    """create a device with no connection to SDS"""

    dev = sdsadv.Device(name="test")

    try:
        dev.create()
        assert None, "assertion should be raised on device with no name"
    except SDSInitError:
        None

# -------------------------------------------------------
def test_device_create_twice():
    """create 2 same devices in SDS"""

    device_name = str(uuid.uuid4())

    sds = _connect_to_sds()

    dev = sdsadv.Device(name=device_name, sds=sds)

    dev.create()

    error = False
    try:
        dev.create()
        error = True
    except SDSDeviceError:
        None

    dev.delete()

    if error:
        assert None, "assertion should be raised on device already in database"

# -------------------------------------------------------
def test_device_delete_ukn():
    """delete non existant device"""

    device_name = str(uuid.uuid4())

    sds = _connect_to_sds()

    dev = sdsadv.Device(name=device_name, sds=sds)

    dev.create()
    dev.delete()
    try:
        dev.delete()
        assert None, "delete ukn device"
    except SDSDeviceNotFoundError:
        None
