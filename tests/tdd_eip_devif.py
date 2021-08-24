# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2021-06-07 17:47:46 alex>
#

"""test for device manager interfaces
 * create_rnd_mac
 * create_rnd_ipv4
 * create_rnd_ipv4_hex
 * create_rnd_ipv6
 * create_rnd_ipv6_hex
 * device_create
 * device_delete
 * test_devif_new_object
 * test_devif_create
 * test_devif_create_ipmac

"""

import logging
import sys
import uuid
import datetime
import time
import random

from SOLIDserverRest.Exception import SDSInitError, SDSRequestError
from SOLIDserverRest.Exception import SDSAuthError, SDSError
from SOLIDserverRest.Exception import SDSEmptyError
from SOLIDserverRest.Exception import SDSDeviceError, SDSDeviceNotFoundError
from SOLIDserverRest.Exception import SDSDeviceIfError
from SOLIDserverRest.Exception import SDSDeviceIfNotFoundError

from .context import sdsadv
from .context import _connect_to_sds
from .adv_basic import *


# -------------------------------------------------------
def device_create(sds):
    """create a device in SDS"""

    device_name = str(uuid.uuid4())

    dev = sdsadv.Device(name=device_name, sds=sds)

    dev.create()
    return dev


# -------------------------------------------------------
def device_delete(dev):
    """delete the param device"""

    dev.delete()


# -------------------------------------------------------
def test_devif_new_object():
    """create a device interface object"""

    if_name = 'tdd-'+str(uuid.uuid4())
    device_name = 'tdd-'+str(uuid.uuid4())

    try:
        devif = sdsadv.DeviceInterface()
        assert None, "no name provided"
    except SDSDeviceIfError:
        None

    try:
        devif = sdsadv.DeviceInterface(name=if_name)
        assert None, "no device provided"
    except SDSDeviceIfError:
        None

    sds = _connect_to_sds()
    dev = sdsadv.Device(sds=sds, name=device_name)

    try:
        devif = sdsadv.DeviceInterface(name=if_name, device=dev)
        assert None, "no SDS device provided"
    except SDSDeviceIfError:
        None

    dev.create()
    devif = sdsadv.DeviceInterface(name=if_name, device=dev)

    obj_string = str(devif)
    logging.debug(obj_string)

    dev.delete()


# -------------------------------------------------------
def test_devif_create():
    """create a device interface object in SDS"""

    sds = _connect_to_sds()
    space = sdsadv.Space(sds=sds, name=str(uuid.uuid4()))
    space.create()

    if_name = 'tdd-'+str(uuid.uuid4())
    device_name = 'tdd-'+str(uuid.uuid4())

    dev = sdsadv.Device(sds=sds, name=device_name)
    dev.create()

    devif = sdsadv.DeviceInterface(sds=sds, name=if_name, device=dev)
    devif.create()

    obj_string = str(devif)
    # logging.info(obj_string)

    # coverage no sds
    devif.sds = None
    try:
        devif.delete()
        assert None, "no sds"
    except SDSDeviceIfError:
        None
    devif.sds = sds

    # coverage no id
    oldid = devif.myid
    devif.myid = -1
    try:
        devif.delete()
        assert None, "no id"
    except SDSDeviceIfNotFoundError:
        None
    devif.myid = oldid

    devif.delete()
    dev.delete()
    space.delete()


# -------------------------------------------------------
def test_devif_create_meta():
    """create a device interface object in SDS with meta-data"""

    sds = _connect_to_sds()
    space = sdsadv.Space(sds=sds, name=str(uuid.uuid4()))
    space.create()

    if_name = 'tdd-'+str(uuid.uuid4())
    device_name = 'tdd-'+str(uuid.uuid4())

    dev = sdsadv.Device(sds=sds, name=device_name)
    dev.create()

    cparams = {
        'key1': 'ok',
        'key2': 12,
        'date': datetime.datetime.now()
    }

    devif = sdsadv.DeviceInterface(sds=sds,
                                   name=if_name,
                                   device=dev,
                                   class_params=cparams)

    devif.set_param(param='modify_time', value=int(time.time()))

    devif.create()
    check_if01 = str(devif)

    devif02 = sdsadv.DeviceInterface(sds=sds,
                                     name=if_name,
                                     device=dev)

    devif02.refresh()
    check_if02 = str(devif02)

    if check_if01 != check_if02:
        logging.error(check_if01)
        logging.error(check_if02)
        assert None, "2 device interfaces are different"

    # coverage refresh
    devif02.sds = None
    try:
        devif02.refresh()
        assert None, "no sds"
    except SDSDeviceIfError:
        None

    devif.delete()
    dev.delete()
    space.delete()


# -------------------------------------------------------
def test_devif_create_ipmac():
    """create a device interface object in SDS with ip/mac"""

    sds = _connect_to_sds()

    space_name = 'tdd-'+str(uuid.uuid4())
    space = sdsadv.Space(sds=sds, name=space_name)
    space.create()

    if_name = 'tdd-'+str(uuid.uuid4())
    device_name = 'tdd-'+str(uuid.uuid4())
    mac = _create_rnd_mac()
    ip_v4 = create_rnd_ipv4()
    # ip_v4 = '192.168.16.171'
    ip_v6 = create_rnd_ipv6()

    dev = sdsadv.Device(sds=sds, name=device_name)
    dev.create()

    # create ip address in Space
    add = sdsadv.IpAddress(sds=sds,
                           space=space,
                           ipv4=ip_v4)
    add.set_mac(mac)
    add.create()

    devif = sdsadv.DeviceInterface(sds=sds, name=if_name, device=dev)
    devif.set_ipv4(ip_v4)
    devif.set_mac(mac)
    devif.set_space(space)
    devif.create()

    obj_string = str(devif)
    # logging.info(obj_string)
    
    add.delete()
    devif.delete()
    dev.delete()
    space.delete()


# -------------------------------------------------------
def test_devif_create_errors():
    """create a device interface object in SDS through error paths"""

    sds = _connect_to_sds()
    space = sdsadv.Space(sds=sds, name=str(uuid.uuid4()))
    space.create()

    if_name = 'tdd-'+str(uuid.uuid4())
    device_name = 'tdd-'+str(uuid.uuid4())

    dev = sdsadv.Device(sds=sds, name=device_name)
    dev.create()

    devif = sdsadv.DeviceInterface(sds=sds, name=if_name, device=dev)

    # bad sds
    devif.sds = None
    try:
        devif.create()
        assert None, "should have raised no sds"
    except SDSDeviceIfError:
        None
    devif.sds = sds

    olddevid = devif.device.myid

    # bad device
    devif.device.myid = -1
    try:
        devif.create()
        assert None, "bad device id"
    except SDSDeviceIfError:
        None
    devif.device.myid = olddevid

    dev.delete()
    space.delete()


# -------------------------------------------------------
def test_devif_update():
    """update a device interface object in SDS"""

    sds = _connect_to_sds()
    space = sdsadv.Space(sds=sds, name=str(uuid.uuid4()))
    space.create()

    if_name = 'tdd-'+str(uuid.uuid4())
    device_name = 'tdd-'+str(uuid.uuid4())

    dev = sdsadv.Device(sds=sds, name=device_name)
    dev.create()

    devif = sdsadv.DeviceInterface(sds=sds, name=if_name, device=dev)
    devif.create()

    # update coverage
    devif.sds = None
    try:
        devif.update()
        assert None, "no sds"
    except SDSDeviceIfError:
        None
    devif.sds = sds

    # update
    devif.update()

    devif.set_ipv4(create_rnd_ipv4())
    devif.update()

    try:
        devif.set_ipv4(create_rnd_ipv6())
        assert None, "bad ipv4 address"
    except SDSDeviceIfError:
        None

    try:
        devif.set_space(None)
        assert None, "set space null"
    except SDSDeviceIfError:
        None

    space02 = sdsadv.Space(sds=sds, name=str(uuid.uuid4()))
    space02.myid = -1
    try:
        devif.set_space(space02)
        assert None, "set space -1"
    except SDSDeviceIfError:
        None

    ifs = dev.fetch_interfaces()

    devif.delete()
    dev.delete()
    space.delete()


# -------------------------------------------------------
def _test_devif_add_if():
    """add interface to device"""

    sds = _connect_to_sds()

    space = sdsadv.Space(sds, name=str(uuid.uuid4()))
    space.create()

    mac = _create_rnd_mac()
    ip_v4 = create_rnd_ipv4_hex()
    ip_v6 = create_rnd_ipv6_hex()

    dev = device_create(sds)

    dev.add_if(name="eth0",
               iftype="interface",
               mac=mac,
               ipaddr=ip_v4)

    # dev.delete()
    # space.delete()
