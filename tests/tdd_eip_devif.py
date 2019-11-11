# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2019-11-01 17:55:42 alex>
#

"""test for device manager interfaces


"""

import logging
import sys
import uuid
import datetime
import random

from SOLIDserverRest.Exception import SDSInitError, SDSRequestError
from SOLIDserverRest.Exception import SDSAuthError, SDSError
from SOLIDserverRest.Exception import SDSEmptyError
from SOLIDserverRest.Exception import SDSDeviceError, SDSDeviceNotFoundError
from SOLIDserverRest.Exception import SDSDeviceIfError
from SOLIDserverRest.Exception import SDSDeviceIfNotFoundError

from .context import sdsadv
from .context import _connect_to_sds


# -------------------------------------------------------
def create_rnd_mac():
    return "00:25:9D:%02x:%02x:%02x" % (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
    )


# -------------------------------------------------------
def create_rnd_ipv4():
    return '.'.join('%s' % random.randint(0, 255) for i in range(4))


# -------------------------------------------------------
def create_rnd_ipv4_hex():
    return ''.join('%x' % random.randint(0, 255) for i in range(4))


# -------------------------------------------------------
def create_rnd_ipv6():
    return ':'.join('{:x}'.format(random.randint(0, 2**16 - 1)) for i in range(8))


# -------------------------------------------------------
def create_rnd_ipv6_hex():
    return ''.join('{:x}'.format(random.randint(0, 2**16 - 1)) for i in range(8))


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
    logging.info(obj_string)

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

    # space = sdsadv.Space(sds=sds, name='Local')
    # space.refresh()

    if_name = 'tdd-'+str(uuid.uuid4())
    device_name = 'tdd-'+str(uuid.uuid4())
    mac = create_rnd_mac()
    ip_v4 = create_rnd_ipv4()
    ip_v4 = '192.168.16.171'
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
    logging.info(obj_string)

    add.delete()
    devif.delete()
    dev.delete()
    space.delete()


# -------------------------------------------------------
def _test_devif_add_if():
    """add interface to device"""

    sds = _connect_to_sds()

    space = sdsadv.Space(sds, name=str(uuid.uuid4()))
    space.create()

    mac = create_rnd_mac()
    ip_v4 = create_rnd_ipv4_hex()
    ip_v6 = create_rnd_ipv6_hex()

    dev = device_create(sds)

    dev.add_if(name="eth0",
               iftype="interface",
               mac=mac,
               ipaddr=ip_v4)

    # dev.delete()
    # space.delete()
