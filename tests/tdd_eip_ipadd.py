# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2020-03-29 14:36:10 alex>
#

"""test ip address

* test_ipadd_new_address_obj
* test_ipadd_new_address_obj_badip
* test_ipadd_new_orphan_address
* test_ipadd_new_in_block
* test_ipadd_mac
* test_ipadd_new_in_block_and_update
* test_ipadd_create_with_classparams
* test_ipadd_new_address_no_mandatory
* test_ipadd_refresh_ukn
* test_ipadd_no_sds
* test_ipadd_free
* test_ipadd_free_empty

"""

import logging
import sys
import uuid
import datetime

from SOLIDserverRest.Exception import SDSInitError, SDSRequestError
from SOLIDserverRest.Exception import SDSAuthError, SDSError
from SOLIDserverRest.Exception import SDSEmptyError
from SOLIDserverRest.Exception import SDSNetworkError, SDSNetworkNotFoundError
from SOLIDserverRest.Exception import SDSIpAddressError
from SOLIDserverRest.Exception import SDSIpAddressNotFoundError

from .context import sdsadv
from .context import _connect_to_sds
from .adv_basic import _create_net


def test_ipadd_new_address_obj():
    """create an ip address object"""

    add = sdsadv.IpAddress(sds=None,
                           space=None,
                           ipv4='192.168.16.10')

    obj_string = str(add)
    logging.debug(obj_string)


def test_ipadd_new_address_obj_badip():
    """create an ip address object with a bad ip"""

    try:
        add = sdsadv.IpAddress(sds=None,
                               space=None,
                               ipv4='192.168.16')
        assert None, "ip address bad format not detected"
    except SDSIpAddressError:
        None

    add = sdsadv.IpAddress(sds=None,
                           space=None,
                           ipv4='192.168.16.0')

    try:
        add.set_ipv4('192.168.16')
        assert None, "ip address bad format not detected"
    except SDSIpAddressError:
        None

    add.set_ipv4('192.168.16.10')


def test_ipadd_new_orphan_address():
    """create an ip address object"""

    # connect to the SDS
    sds = _connect_to_sds()

    name = str(uuid.uuid4())

    space = sdsadv.Space(sds=sds, name=str(uuid.uuid4()))
    space.create()

    add = sdsadv.IpAddress(sds=sds,
                           space=space,
                           ipv4='192.168.16.10')
    add.create()

    obj_string = str(add)
    logging.debug(obj_string)

    add.delete()
    space.delete()


def test_ipadd_new_in_block():
    """create an ip address object in a block and validate heritage"""

    # connect to the SDS
    sds = _connect_to_sds()

    space = sdsadv.Space(sds=sds, name=str(uuid.uuid4()))
    space.create()

    network = sdsadv.Network(sds=sds,
                             space=space,
                             name=str(uuid.uuid4()))

    network.set_address_prefix('192.168.0.0', 16)
    network.set_is_block(True)
    network.create()

    net01 = sdsadv.Network(sds=sds,
                           space=space,
                           name=str(uuid.uuid4()))

    net01.set_address_prefix('192.168.16.0', 24)
    net01.set_parent(network)
    net01.set_is_terminal(True)
    net01.create()

    add = sdsadv.IpAddress(sds=sds,
                           space=space,
                           ipv4='192.168.16.10')
    add.create()

    obj_string = str(add)

    add.delete()
    network.delete()
    space.delete()


def test_ipadd_mac():
    """create an ip address object with mac address"""

    add = sdsadv.IpAddress(sds=None,
                           space=None,
                           ipv4='192.168.16.10')

    add.set_mac("010203040506")
    add.set_mac("01:02:03:04:05:06")
    add.set_mac("01-02-03-04-05-06")
    add.set_mac("f1-a2-b3-c4-d5-e6")

    try:
        add.set_mac("f1-a2-b3-c4-d5")
        assert None, "mac bad format not catched"
    except SDSIpAddressError:
        None


def test_ipadd_new_in_block_and_update():
    """create an ip address object in a block and validate heritage"""

    # connect to the SDS
    sds = _connect_to_sds()

    space = sdsadv.Space(sds=sds, name=str(uuid.uuid4()))
    space.create()

    network = sdsadv.Network(sds=sds,
                             space=space,
                             name=str(uuid.uuid4()))

    network.set_address_prefix('192.168.0.0', 16)
    network.set_is_block(True)
    network.create()

    net01 = sdsadv.Network(sds=sds,
                           space=space,
                           name=str(uuid.uuid4()))

    net01.set_address_prefix('192.168.16.0', 24)
    net01.set_parent(network)
    net01.set_is_terminal(True)
    net01.create()

    add = sdsadv.IpAddress(sds=sds,
                           space=space,
                           ipv4='192.168.16.10')
    add.create()

    add.set_mac('010203040506')
    add.update()

    try:
        add.set_name(None)
        assert None, "bad name format"
    except SDSError:
        None

    add.set_name('ip_name')
    add.update()

    obj_string = str(add)
    logging.debug(obj_string)

    add.delete()
    network.delete()
    space.delete()


def test_ipadd_create_with_classparams():
    """create an ip address with cp and delete it"""

    # connect to the SDS
    sds = _connect_to_sds()

    # creates a space
    space = sdsadv.Space(sds=sds, name=str(uuid.uuid4()))
    space.create()

    params = {
        'key1': 'ok',
        'key2': 12,
        'date': datetime.datetime.now()
    }

    add01 = sdsadv.IpAddress(sds=sds,
                             space=space,
                             ipv4='192.168.16.10',
                             class_params=params)
    add01.create()
    check01 = str(add01)

    add02 = sdsadv.IpAddress(sds=sds,
                             space=space,
                             ipv4='192.168.16.10')
    add02.refresh()
    check02 = str(add02)

    if check01 != check02:
        logging.error(check01)
        logging.error(check02)
        assert None, "2 ip are different"

    add01.set_param('mac_address', '01:02:01:02:01:02')

    add01.delete()
    space.delete()


def test_ipadd_new_address_no_mandatory():
    """create an ip address object and check errors"""

    # connect to the SDS
    sds = _connect_to_sds()

    # creates a space
    space = sdsadv.Space(sds=sds, name=str(uuid.uuid4()))
    space.create()

    try:
        add = sdsadv.IpAddress()
        add.create()
        assert None, "no sds not catched"
    except SDSIpAddressError:
        None

    try:
        add = sdsadv.IpAddress(sds=sds)
        add.create()
        assert None, "no space not catched"
    except SDSIpAddressError:
        None

    try:
        add = sdsadv.IpAddress(sds=sds,
                               space=space)
        add.create()
        assert None, "no ip not catched"
    except SDSIpAddressError:
        None

    add = sdsadv.IpAddress(sds=sds,
                           space=space,
                           ipv4='192.168.16.10')
    add.set_name("chgeck_name")
    add.create()
    add.create()

    try:
        add2 = sdsadv.IpAddress(sds=sds,
                                space=space,
                                ipv4='192.168.16.10')
        add2.set_name("chgeck_name")
        add2.create()
        assert None, 'duplicate ip address'
    except SDSIpAddressError:
        None

    # coverage for delete wo id
    _id = add.myid
    add.myid = -1

    try:
        add.delete()
        assert None, "delete with id cleared"
    except SDSIpAddressNotFoundError:
        None

    add.myid = _id
    add.delete()

    space.delete()


def test_ipadd_refresh_ukn():
    """refresh on unknown ip address"""

    sds = _connect_to_sds()

    # creates a space
    space = sdsadv.Space(sds=sds, name=str(uuid.uuid4()))
    space.create()

    add = sdsadv.IpAddress(sds=sds,
                           space=space,
                           ipv4='192.168.16.10')

    try:
        add.refresh()
        assert None, "ip not found not catched"
    except SDSIpAddressNotFoundError:
        None

    space.delete()


def test_ipadd_no_sds():
    """action wo sds set"""

    add = sdsadv.IpAddress(sds=None,
                           space=None,
                           ipv4='192.168.16.10')

    try:
        add.refresh()
        assert None, "ip refresh no sds"
    except SDSIpAddressError:
        None

    try:
        add.delete()
        assert None, "ip delete no sds"
    except SDSIpAddressError:
        None

    try:
        add.update()
        assert None, "ip update no sds"
    except SDSIpAddressError:
        None


def test_ipadd_free():
    """check if an ip address is free"""

    # connect to the SDS
    sds = _connect_to_sds()

    space = sdsadv.Space(sds=sds, name=str(uuid.uuid4()))
    space.create()

    network = _create_net(sds, space, 
                          name=str(uuid.uuid4()),
                          net='192.168.0.0', prefix=16, 
                          is_block=True)

    net01 = _create_net(sds, space, 
                        name=str(uuid.uuid4()),
                        net='192.168.0.0', prefix=24, 
                        is_block=False,
                        is_terminal=True,
                        parent=network)

    afreeip = net01.find_free_ip()

    if afreeip[0] != '192.168.0.1':
        assert None, 'bad free address returned'

    add = sdsadv.IpAddress(sds=sds,
                           space=space,
                           ipv4=afreeip[0])
    add.create()

    afreeip = net01.find_free_ip()

    if afreeip[0] != '192.168.0.2':
        assert None, 'bad free address returned'

    add.delete()
    network.delete()
    space.delete()
    
    
def test_ipadd_free_empty():
    """check if an ip address is free in a full net"""

    # connect to the SDS
    sds = _connect_to_sds()

    space = sdsadv.Space(sds=sds, name=str(uuid.uuid4()))
    space.create()

    network = _create_net(sds, space, 
                          name=str(uuid.uuid4()),
                          net='192.168.0.0', prefix=29, 
                          is_block=True)

    net01 = _create_net(sds, space, 
                        name=str(uuid.uuid4()),
                        net='192.168.0.0', prefix=30, 
                        is_block=False,
                        is_terminal=True,
                        parent=network)

    add1 = sdsadv.IpAddress(sds=sds,
                            space=space,
                            name=str(uuid.uuid4()),
                            ipv4='192.168.0.1')
    add1.create()

    afreeip = net01.find_free_ip()

    add2 = sdsadv.IpAddress(sds=sds,
                            space=space,
                            name=str(uuid.uuid4()),
                            ipv4='192.168.0.2')
    add2.create()

    afreeip = net01.find_free_ip()
    if afreeip:
        assert None, "free pool should be empty"


    add1.delete()
    add2.delete()
    network.delete()
    space.delete()
