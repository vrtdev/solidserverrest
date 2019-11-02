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
    return '.'.join('%s'%random.randint(0, 255) for i in range(4))

# -------------------------------------------------------
def create_rnd_ipv4_hex():
    return ''.join('%x'%random.randint(0, 255) for i in range(4))

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
def test_devif_add_if():
    """add interface to device"""

    sds = _connect_to_sds()

    space = sdsadv.Space(sds, name=str(uuid.uuid4()))

    mac = create_rnd_mac()
    ip_v4 = create_rnd_ipv4_hex()
    ip_v6 = create_rnd_ipv6_hex()

    dev = device_create(sds)

    dev.add_if(name="eth0",
               iftype="interface",
               mac=mac,
               ipaddr=ip_v4)

    dev.delete()
    space.delete()
