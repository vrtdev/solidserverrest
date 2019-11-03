# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2019-11-03 17:38:20 alex>
#

"""test network

* test_net_new_network
* test_net_create_network_no_mandatory
* test_net_create_block
* test_net_create_block_refresh_error
* test_net_refresh_non_exist
* test_net_delete_block_wo_mandatory
* test_net_create_block_wo_sds
* test_net_refresh_block_wo_sds
* test_net_create_block_collision
* test_net_update_block
* test_net_create_block_with_classparams
* test_net_block_net_subnets_wo_parent

"""

import logging
import sys
import uuid
import datetime

from SOLIDserverRest.Exception import SDSInitError, SDSRequestError
from SOLIDserverRest.Exception import SDSAuthError, SDSError
from SOLIDserverRest.Exception import SDSEmptyError
from SOLIDserverRest.Exception import SDSNetworkError, SDSNetworkNotFoundError

from .context import sdsadv
from .context import _connect_to_sds

# -------------------------------------------------------
def test_net_new_network():
    """create a network object"""

    net_name = str(uuid.uuid4())

    network = sdsadv.Network(space=None,
                             name=net_name)

    obj_string = str(network)
    logging.debug(obj_string)
    
    network = None


# -------------------------------------------------------
def test_net_create_network_no_mandatory():
    """create a network object"""

    # connect to the SDS
    sds = _connect_to_sds()

    # creates a space
    space = sdsadv.Space(sds=sds, name=str(uuid.uuid4()))
    space.create()

    net_name = str(uuid.uuid4())

    # no sds
    network = sdsadv.Network(space=None,
                             name=net_name)

    try:
        network.create()
        assert None, "create network without sds connection"
    except SDSNetworkError:
        None

    # no space
    network = sdsadv.Network(sds=sds,
                             space=None,
                             name=net_name)

    try:
        network.create()
        assert None, "create network without space"
    except SDSNetworkError:
        None

    # no address
    network = sdsadv.Network(sds=sds,
                             space=space,
                             name=net_name)

    try:
        network.create()
        assert None, "create network without address"
    except SDSNetworkError:
        None

    # no prefix
    network = sdsadv.Network(sds=sds,
                             space=space,
                             name=net_name)
    network.subnet_addr = "192.168.16.0"

    try:
        network.create()
        assert None, "create network without prefix"
    except SDSNetworkError:
        None

    space.delete()


# -------------------------------------------------------
def test_net_create_block():
    """create a block and delete it"""

    # connect to the SDS
    sds = _connect_to_sds()

    # creates a space
    space = sdsadv.Space(sds=sds, name=str(uuid.uuid4()))
    space.create()

    # create a network object
    net_name = str(uuid.uuid4())
    network = sdsadv.Network(sds=sds,
                             space=space,
                             name=net_name)

    network.set_address_prefix('172.16.0.0', 16)
    network.set_is_block(True)
    network.create()

    obj_string = str(network)

    network.delete()
    space.delete()


# -------------------------------------------------------
def test_net_create_block_refresh_error():
    """create a block, delete it direct and try a refresh"""

    # connect to the SDS
    sds = _connect_to_sds()

    # creates a space
    space = sdsadv.Space(sds=sds, name=str(uuid.uuid4()))
    space.create()

    # create a network object
    net_name = str(uuid.uuid4())
    network = sdsadv.Network(sds=sds,
                             space=space,
                             name=net_name)

    network.set_address_prefix('172.16.0.0', 16)
    network.set_is_block(True)
    network.create()

    # delete using direct API
    params = {
        'subnet_id': network.params['subnet_id']
    }

    sds.query("ip_subnet_delete",
              params=params)

    try:
        network.refresh()
        assert None, "refresh non existing network"
    except SDSNetworkError:
        None

    space.delete()


# -------------------------------------------------------
def test_net_refresh_non_exist():
    """refresh a block not existing"""

    # connect to the SDS
    sds = _connect_to_sds()

    # creates a space
    space = sdsadv.Space(sds=sds, name=str(uuid.uuid4()))
    space.create()

    # create a network object
    net_name = str(uuid.uuid4())
    network = sdsadv.Network(sds=sds,
                             space=space,
                             name=net_name)

    network.set_address_prefix('172.16.0.0', 16)

    try:
        network.refresh()
        assert None, "refresh non existing network"
    except SDSNetworkError:
        None

    space.delete()


# -------------------------------------------------------
def test_net_delete_block_wo_mandatory():
    """delete-refresh a block without mandatory"""

    sds = _connect_to_sds()

    # create a network object
    net_name = str(uuid.uuid4())

    network = sdsadv.Network(name=net_name)

    try:
        network.delete()
        network.refresh()
        assert None, "delete network without SDS connection"
    except SDSNetworkError:
        None

    network = sdsadv.Network(sds=sds,
                             name=net_name)

    try:
        network.delete()
        assert None, "delete network without SDS connection"
    except SDSNetworkNotFoundError:
        None


# -------------------------------------------------------
def test_net_create_block_wo_sds():
    """try to update a block without SDS connection"""

    # create a network object
    network = sdsadv.Network(space="test",
                             name="test")

    try:
        network.update()
        assert None, "update network without SDS connection"
    except SDSNetworkError:
        None


# -------------------------------------------------------
def test_net_refresh_block_wo_sds():
    """try to refresh a block without SDS connection"""

    # create a network object
    network = sdsadv.Network(space="test",
                             name="test")

    try:
        network.refresh()
        assert None, "refresh network without SDS connection"
    except SDSNetworkError:
        None


# -------------------------------------------------------
def test_net_create_block_collision():
    """create a block and delete it"""

    sds = _connect_to_sds()

    space = sdsadv.Space(sds=sds, name=str(uuid.uuid4()))
    space.create()

    name01 = str(uuid.uuid4())
    network01 = sdsadv.Network(sds=sds,
                               space=space,
                               name=name01)

    network01.set_address_prefix('172.16.0.0', 16)
    network01.set_is_block(True)
    network01.create()

    # collision inside the network object
    network01.create()

    name02 = str(uuid.uuid4())
    network02 = sdsadv.Network(sds=sds,
                               space=space,
                               name=name02)

    network02.set_address_prefix('172.16.0.0', 16)
    network02.set_is_block(True)

    try:
        network02.create()
        assert None, "this subnet should already exists"
    except SDSNetworkError:
        None

    network01.delete()

    space.delete()


# -------------------------------------------------------
def test_net_update_block():
    """create a block, update it and delete it"""

    # connect to the SDS
    sds = _connect_to_sds()

    # creates a space
    space = sdsadv.Space(sds=sds, name=str(uuid.uuid4()))
    space.create()

    # create a network object
    net_name = str(uuid.uuid4())
    network = sdsadv.Network(sds=sds,
                             space=space,
                             name=net_name)

    network.set_address_prefix('172.16.0.0', 16)
    network.set_is_block(True)
    network.create()

    network.set_async()

    # change
    network.set_param(param='subnet_name', value='test')
    network.set_param(param='description', value='test description')
    network.update()

    # clean
    network.delete()
    space.delete()


# -------------------------------------------------------
def test_net_create_block_with_classparams():
    """create a block with cp and delete it"""

    # connect to the SDS
    sds = _connect_to_sds()

    # creates a space
    space = sdsadv.Space(sds=sds, name=str(uuid.uuid4()))
    space.create()

    # create a network object
    net_name = str(uuid.uuid4())
    params = {
        'key1': 'ok',
        'key2': 12,
        'date': datetime.datetime.now()
    } 

    network = sdsadv.Network(sds=sds,
                             space=space,
                             name=net_name,
                             class_params=params)

    network.set_address_prefix('172.16.0.0', 16)
    network.set_is_block(True)
    network.create()

    check_net01 = str(network)

    network02 = sdsadv.Network(sds=sds,
                               space=space,
                               name=net_name)
    network02.refresh()

    check_net02 = str(network02)

    if check_net01 != check_net02:
        logging.error(check_net01)
        logging.error(check_net02)
        assert None, "2 networks are different"
    
    network.delete()
    space.delete()


# -------------------------------------------------------
def test_net_block_net_subnets():
    """create a hierarchy of block/net/terms"""

    # connect to the SDS
    sds = _connect_to_sds()

    # creates a space
    space = sdsadv.Space(sds=sds, name=str(uuid.uuid4()))
    space.create()

    # create a network object
    net01 = sdsadv.Network(sds=sds,
                             space=space,
                             name=str(uuid.uuid4()))

    net01.set_address_prefix('172.16.0.0', 16)
    net01.set_is_block(True)
    net01.create()

    net02 = sdsadv.Network(sds=sds,
                               space=space,
                               name=str(uuid.uuid4()))

    net02.set_address_prefix('172.16.0.0', 24)
    net02.set_parent(net01)
    net02.set_is_terminal(False)
    net02.create()

    net03 = sdsadv.Network(sds=sds,
                               space=space,
                               name=str(uuid.uuid4()))

    net03.set_address_prefix('172.16.0.0', 25)
    net03.set_parent(net02)
    net03.set_is_terminal(True)
    net03.create()
    
    net03.delete()
    net02.delete()
    net01.delete()

    space.delete()

# -------------------------------------------------------
def test_net_block_net_subnets_wo_parent():
    """create a subnet in a not defined parent"""

    # connect to the SDS
    sds = _connect_to_sds()

    # creates a space
    space = sdsadv.Space(sds=sds, name=str(uuid.uuid4()))
    space.create()

    # create a network object
    net01 = sdsadv.Network(sds=sds,
                             space=space,
                             name=str(uuid.uuid4()))

    net01.set_address_prefix('172.16.0.0', 16)
    net01.set_is_block(True)


    net02 = sdsadv.Network(sds=sds,
                               space=space,
                               name=str(uuid.uuid4()))

    net02.set_address_prefix('172.16.0.0', 24)

    try:
        net02.set_parent(net01)
        assert None, "should not be able to link to unk parent"
    except SDSNetworkError:
        None

    space.delete()

# -------------------------------------------------------
def _test_none():
    """test only"""

    sds = _connect_to_sds()

    try:
        space = sdsadv.Space(sds=sds, name="test")
        space.create()
    except SDSError:
        space.refresh()
        None

    # create block
    net_name = "test_block"
    block = sdsadv.Network(sds=sds,
                             space=space,
                             name=net_name)

    block.set_address_prefix('172.16.0.0', 16)
    block.set_is_block(True)

    try:
        block.create()
    except SDSNetworkError:
        block.refresh()
        None

    network = sdsadv.Network(sds=sds,
                             space=space,
                             name="t01")

    network.set_address_prefix('172.16.0.0', 23)
    network.set_parent(block)
    try:
        network.create()
    except SDSNetworkError:
        network.refresh()
        None

    logging.info(network)

    network02 = sdsadv.Network(sds=sds,
                               space=space,
                               name="t02")

    network02.set_address_prefix('172.16.0.0', 24)
    network02.set_parent(network)
    network02.create()

    network03 = sdsadv.Network(sds=sds,
                               space=space,
                               name="t03")

    network03.set_address_prefix('172.16.0.0', 25)
    network03.set_parent(network02)
    network03.set_is_terminal(True)
    network03.create()

    return

    # delete
    block.delete()
    space.delete()
