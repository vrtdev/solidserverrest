# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2019-11-01 17:46:32 alex>
#

"""test file for the device manager

* test_device_new_object
* test_device_refresh_not_connected
* test_device_new_object_wo_name
* test_device_create
* test_device_delete_not_connected
* test_device_update_not_connected
* test_device_refresh
* test_device_refresh_ukn
* test_device_refresh_destroyed
* test_device_create_not_connected
* test_device_create_twice
* test_device_delete_ukn
* test_device_async

"""

import logging
import sys
import uuid
import datetime

from SOLIDserverRest.Exception import SDSInitError, SDSRequestError
from SOLIDserverRest.Exception import SDSAuthError, SDSError
from SOLIDserverRest.Exception import SDSEmptyError
from SOLIDserverRest.Exception import SDSDeviceError, SDSDeviceNotFoundError

from .context import sdsadv
from .context import _connect_to_sds

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
def test_device_with_classparams():
    """create a device in SDS with meta-data, refresh and delete"""

    device_name = str(uuid.uuid4())

    sds = _connect_to_sds()

    classparams = {
        'a': 12,
        'b': "string",
    }

    dev01 = sdsadv.Device(name=device_name, 
                          sds=sds,
                          class_params = classparams)

    dev01.add_class_params({'c': 'new add'})

    dev01.create()

    dev02 = sdsadv.Device(name=device_name, sds=sds)
    dev02.refresh()
   
    if int(dev02.get_class_params('a')) != int(classparams['a']):
        assert None, "class params not correct"

    dev01.delete()

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
def test_device_update_not_connected():
    """update a device while not connected to SDS"""

    device_name = str(uuid.uuid4())

    dev = sdsadv.Device(name=device_name)
    try:
        dev.update()
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
    except SDSError:
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
    except SDSDeviceError:
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

# -------------------------------------------------------
def test_device_async():
    """async modification are not pushed"""

    device_name = str(uuid.uuid4())
    sds = _connect_to_sds()
    dev01 = sdsadv.Device(name=device_name, sds=sds)

    # sync mode
    dev01.set_sync()

    dev01.create()
    device_name = str(uuid.uuid4())

    # coverage test also
    dev01.set_sync()
    dev01.set_param(param='notexistant')
    dev01.set_param(param={'test':1})
    dev01.set_param(param='notexistant', value=12)
    dev01.set_param(param='hostdev_id', value=12)

    dev01.set_param('hostdev_name', device_name)

    dev02 = sdsadv.Device(name=device_name, sds=sds)
    dev02.refresh()

    dev01_name = dev01.params['hostdev_name']
    dev02_name = dev02.params['hostdev_name']

    if dev01_name != dev02_name:
        assert None, "sync mode not working"

    # async mode
    dev01.set_async()

    dev01.set_param('hostdev_name', str(uuid.uuid4()))

    dev03 = sdsadv.Device(name=device_name, sds=sds)
    dev03.refresh()

    dev01_name = dev01.params['hostdev_name']
    dev03_name = dev03.params['hostdev_name']

    if dev01_name == dev03_name:
        assert None, "async mode not working"

    dev01.update()
    dev03.refresh()
    dev01_name = dev01.params['hostdev_name']
    dev03_name = dev03.params['hostdev_name']

    if dev01_name != dev03_name:
        assert None, "async mode not working"

    dev01.delete()
