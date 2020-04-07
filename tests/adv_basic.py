import sys
import os
import random

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import SOLIDserverRest.adv as sdsadv
from SOLIDserverRest.Exception import SDSNetworkError, SDSIpAddressError

try:
    from tests.data_sample import *
except:
    from .data_sample import *

__all__ = ["_create_net",
           "_create_rnd_mac",
           "_create_ip_add"]


# -------------------------------------------------------
def _create_net(sds, space, name, net, prefix, is_block, is_terminal=False, parent=None):
    net01 = sdsadv.Network(sds=sds,
                           space=space,
                           name=name)

    net01.set_address_prefix(net, prefix)
    net01.set_is_block(is_block)
    net01.set_is_terminal(is_terminal)
    if parent:
        net01.set_parent(parent)

    try:
        net01.create()
    except SDSNetworkError:
        net01.refresh()

    return net01


# -------------------------------------------------------
def _create_ip_add(sds, space, ipv4, name=None, mac=None):
    add = sdsadv.IpAddress(sds=sds,
                           space=space,
                           ipv4=ipv4)

    if mac:
        add.set_mac(mac)

    if name:
        add.set_name(name)

    try:
        add.create()
    except SDSIpAddressError:
        add.refresh()

    return add


# -------------------------------------------------------
def _create_rnd_mac():
    return "00:25:9D:%02x:%02x:%02x" % (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
    )

