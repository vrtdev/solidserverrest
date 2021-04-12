# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2020-04-13 16:11:14 alex>
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
* test_net_block_net_subnets
* test_net_block_net_subnets_wo_parent
* test_net_find_free

"""

import logging
import sys
import uuid
import datetime
import ipaddress

from SOLIDserverRest.Exception import SDSInitError, SDSRequestError
from SOLIDserverRest.Exception import SDSAuthError, SDSError
from SOLIDserverRest.Exception import SDSEmptyError
from SOLIDserverRest.Exception import SDSNetworkError, SDSNetworkNotFoundError

from .context import sdsadv
from .context import _connect_to_sds
from .adv_basic import _create_net

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

    network.set_address_prefix('172.16.254.0', 24)

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

    # check network name
    if network02.name != net_name:
        logging.error(check_net02)
        assert None, "network name altered"

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
def test_net_find_free():
    """find a free subnet"""

    # connect to the SDS
    sds = _connect_to_sds()

    # creates a space
    space = sdsadv.Space(sds=sds, name=str(uuid.uuid4()))
    space.create()
    # space = sdsadv.Space(sds=sds, name='test')
    # space.refresh()

    # create a network object
    net01 = _create_net(sds, space,
                        # name=str(uuid.uuid4()),
                        name="test",
                        net='172.16.0.0', prefix=16,
                        is_block=True)

    possible_net = net01.find_free(24)

    # check array is not empty
    if len(possible_net) == 0:
        assert None, "free subnets should not be empty"

    # check wether nets are in the appropriate subnet
    supernet = ipaddress.ip_network('{}/{}'.format('172.16.0.0', 16)).network_address
    for pnet in possible_net:
        pnet_add = ipaddress.ip_network('{}/{}'.format(pnet, 16), False).network_address
        if supernet != pnet_add:
            assert None, "proposed subnet not valid for pnet"

    # error coverage
    possible_net = net01.find_free(15)
    if possible_net:
        assert None, "free list should be empty"

    space.delete()


# -------------------------------------------------------
def test_net_list():
    """list subnets"""

    # connect to the SDS
    sds = _connect_to_sds()

    # creates a space
    space = sdsadv.Space(sds=sds, name=str(uuid.uuid4()))
    space.create()
    # space = sdsadv.Space(sds=sds, name='test')
    # space.refresh()

    # create a network object
    net01 = _create_net(sds, space,
                        # name=str(uuid.uuid4()),
                        name="test",
                        net='172.16.0.0', prefix=16,
                        is_block=True)

    supernet = ipaddress.ip_network('{}/{}'.format('172.16.0.0', 16))

    # i = 1
    for n in supernet.subnets(prefixlen_diff=4):
        net = _create_net(sds, space,
                          name=str(uuid.uuid4()),
                          # name = "net-{}".format(i),
                          net=n.network_address,
                          prefix=n.prefixlen,
                          is_block=False,
                          is_terminal=False,
                          parent=net01)
        # i += 1

    anet = net01.get_subnet_list()
    anet = sorted(anet, key=lambda k: ipaddress.ip_address(k['start_hostaddr']).packed)
    if len(anet) != 16:
        assert None, "bad net list size 16 != {}".format(len(anet))
    if anet[1]['start_hostaddr'] != '172.16.16.0':
        logging.info(anet[1])
        assert(None, "bad net list content,"
                     "expecting 1=172.16.16.0, got {}".format(anet[1]['start_hostaddr']))

    # pagination
    anet = net01.get_subnet_list(limit=4)
    anet = sorted(anet, key=lambda k: ipaddress.ip_address(k['start_hostaddr']).packed)
    if len(anet) != 4:
        logging.info(anet)
        assert None, "bad net list size 4 != {}".format(len(anet))
    if anet[1]['start_hostaddr'] != '172.16.16.0':
        logging.info(anet[1])
        assert(None, "bad net list content, first page, "
                     "expecting 172.16.16.0 and got {}".format(anet[1]['start_hostaddr']))

    anet = net01.get_subnet_list(limit=4, offset=4)
    anet = sorted(anet, key=lambda k: ipaddress.ip_address(k['start_hostaddr']).packed)
    if len(anet) != 4:
        assert None, "bad net list size 4 != {}".format(len(anet))
    if anet[0]['start_hostaddr'] != '172.16.64.0':
        logging.info(anet[0])
        assert(None, "bad net list content, second page, "
                     "expecting 172.16.64.0 and got {}".format(anet[0]['start_hostaddr']))

    anet = net01.get_subnet_list(limit=8, page=4)
    anet = sorted(anet, key=lambda k: ipaddress.ip_address(k['start_hostaddr']).packed)
    if len(anet) != 8:
        logging.info(anet)
        assert None, "bad net list size 8 != {}".format(len(anet))

    anet = net01.get_subnet_list(limit=8, page=3, offset=1)
    anet = sorted(anet, key=lambda k: ipaddress.ip_address(k['start_hostaddr']).packed)
    if len(anet) != 8:
        assert None, "bad net list size 8 != {}".format(len(anet))
    if anet[0]['start_hostaddr'] != '172.16.16.0':
        logging.info(anet)
        assert None, "bad net list content"

    anet = net01.get_subnet_list(limit=8, page=4, offset=9)
    anet = sorted(anet, key=lambda k: ipaddress.ip_address(k['start_hostaddr']).packed)
    if len(anet) != 7:
        assert None, "bad net list size 7 != {}".format(len(anet))
    if anet[0]['start_hostaddr'] != '172.16.144.0':
        logging.info(anet)
        assert None, "bad net list content"

    # coverage
    anet = net01.get_subnet_list(terminal=1)
    if anet:
        assert None, "bad net list, no terminal"

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
