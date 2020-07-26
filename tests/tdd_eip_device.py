# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2020-07-26 16:11:40 alex>
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
* test_device_delete_empty
* test_device_list

"""

import logging
import sys
import uuid
import datetime

from SOLIDserverRest.Exception import SDSInitError, SDSRequestError
from SOLIDserverRest.Exception import SDSAuthError, SDSError, SDSDeviceIfError
from SOLIDserverRest.Exception import SDSEmptyError, SDSSpaceError
from SOLIDserverRest.Exception import SDSDeviceError, SDSDeviceNotFoundError

from .context import sdsadv
from .context import _connect_to_sds
from .adv_basic import *


# -------------------------------------------------------
def test_device_new_object():
    """create a device object"""

    device_name = "tdd-"+str(uuid.uuid4())

    dev = sdsadv.Device(name=device_name)

    obj_string = str(dev)
    logging.debug(obj_string)


# -------------------------------------------------------
def test_device_refresh_not_connected():
    """refresh an object not connected"""

    device_name = "tdd-"+str(uuid.uuid4())

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

    device_name = "tdd-"+str(uuid.uuid4())

    sds = _connect_to_sds()

    dev = sdsadv.Device(sds=sds, name=device_name)

    dev.create()
    dev.delete()


# -------------------------------------------------------
def test_device_with_classparams():
    """create a device in SDS with meta-data, refresh and delete"""

    device_name = "tdd-"+str(uuid.uuid4())

    sds = _connect_to_sds()

    classparams = {
        'a': 12,
        'b': "string",
    }

    dev01 = sdsadv.Device(name=device_name,
                          sds=sds,
                          class_params=classparams)

    dev01.add_class_params({'c': 'new add'})
    dev01.create()

    dev02 = sdsadv.Device(sds=sds, name=device_name)
    dev02.refresh()

    if int(dev02.get_class_params('a')) != int(classparams['a']):
        assert None, "class params not correct"

    dev01.delete()


# -------------------------------------------------------
def test_device_delete_not_connected():
    """delete a device while not connected to SDS"""

    device_name = "tdd-"+str(uuid.uuid4())

    dev = sdsadv.Device(name=device_name)
    try:
        dev.delete()
        assert None, "not detecting delete on not connected"
    except SDSDeviceError:
        None


# -------------------------------------------------------
def test_device_update_not_connected():
    """update a device while not connected to SDS"""

    device_name = "tdd-"+str(uuid.uuid4())

    dev = sdsadv.Device(name=device_name)
    try:
        dev.update()
        assert None, "not detecting delete on not connected"
    except SDSDeviceError:
        None


# -------------------------------------------------------
def test_device_refresh():
    """create a device in SDS and refresh"""

    device_name = "tdd-"+str(uuid.uuid4())

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

    device_name = "tdd-"+str(uuid.uuid4())

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

    device_name = "tdd-"+str(uuid.uuid4())

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

    device_name = "tdd-"+str(uuid.uuid4())

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

    device_name = "tdd-"+str(uuid.uuid4())

    sds = _connect_to_sds()

    dev = sdsadv.Device(name=device_name, sds=sds)

    dev.create()

    dev02 = sdsadv.Device(name=device_name, sds=sds)
    dev02.refresh()

    dev.delete()
    try:
        dev02.delete()
        assert None, "delete ukn device"
    except SDSDeviceNotFoundError:
        None


# -------------------------------------------------------
def test_device_async():
    """async modification are not pushed"""

    device_name = "tdd-"+str(uuid.uuid4())
    sds = _connect_to_sds()
    dev01 = sdsadv.Device(name=device_name, sds=sds)

    # sync mode
    dev01.set_sync()

    dev01.create()
    device_name = str(uuid.uuid4())

    # coverage test also
    dev01.set_sync()
    dev01.set_param(param='notexistant')
    dev01.set_param(param={'test': 1})
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


# -------------------------------------------------------
def test_device_delete_empty():
    """create a device and delete it without in SDS"""

    device_name = "tdd-"+str(uuid.uuid4())

    sds = _connect_to_sds()

    dev = sdsadv.Device(sds=sds, name=device_name)

    try:
        dev.delete()
        assert None, "should not be able to delete empty device"
    except SDSDeviceNotFoundError:
        None


# -------------------------------------------------------
def _subtest_device_list_01(sds, space_name):
    """ search space + net01 """
    logging.info("search space + net01 (expected 2 results)")
    adevs = sdsadv.list_devices(sds, limit=0,
                                filters=[
                                    {'type':'in_subnet', 'val': '172.16.1.0/24'},
                                    {'type':'space', 'val': space_name},
                                    {'type':'of_class', 'val': 'tdd'},
                                ])

    if len(adevs) != 2:
        logging.info(len(adevs))
        assert None, "invalid result"

# -------------------------------------------------------
def _subtest_device_list_02(sds, space_name):
    """  search space + net02 """
    logging.info("search space + net02 (expected 4 result)")
    adevs = sdsadv.list_devices(sds, limit=0,
                                filters=[
                                    {'type':'in_subnet', 'val': '172.16.2.0/24'},
                                    {'type':'space', 'val': space_name},
                                    {'type':'of_class', 'val': 'tdd'},
                                ])
    if len(adevs) != 4:
        logging.info(adevs)
        assert None, "invalid result"

# -------------------------------------------------------
def _subtest_device_list_03(sds, space_name):
    """ search space + metadata """
    logging.info("search space + metadata (expected 1 result)")
    adevs = sdsadv.list_devices(sds, limit=0,
                                filters=[
                                    {'type':'metadata', 'name': 'key01', 'val': '1'},
                                    {'type':'space', 'val': space_name},
                                    {'type':'of_class', 'val': 'tdd'},
                                ])
    if len(adevs) != 1:
        logging.info(len(adevs))
        assert None, "invalid result"

# -------------------------------------------------------
def _subtest_device_list_04(sds, space_name):
    """ search space + metadata """
    logging.info("search space + metadata (expected 0 result)")
    adevs = sdsadv.list_devices(sds, limit=0,
                                filters=[
                                    {'type':'metadata', 'name': 'key01', 'val': '2'},
                                    {'type':'space', 'val': space_name},
                                    {'type':'of_class', 'val': 'tdd'},
                                ])
    if len(adevs) != 0:
        logging.info(len(adevs))
        assert None, "invalid result"


# -------------------------------------------------------
def _subtest_device_list_05(sds, space_name):
    """ search space with limit """
    logging.info("search space with limit")
    adevs = sdsadv.list_devices(sds, limit=2,
                                filters=[
                                    {'type':'space', 'val': space_name},
                                    {'type':'of_class', 'val': 'tdd'},
                                ])
    if len(adevs) != 2:
        logging.info(len(adevs))
        assert None, "invalid result"

# -------------------------------------------------------
def _subtest_device_list_06(sds):
    """ search w/o space """
    logging.info("search w/o space")
    adevs = sdsadv.list_devices(sds, limit=0,
                                filters=[
                                    {'type':'of_class', 'val': 'tdd'},
                                ])
    if len(adevs) != 6:
        logging.info(len(adevs))
        assert None, "invalid result"


# -------------------------------------------------------
def _subtest_device_list_07(sds):
    """ search with unknown space """
    logging.info("search with unknown space")
    adevs = sdsadv.list_devices(sds, limit=0,
                                filters=[
                                    {'type':'of_class', 'val': 'tdd'},
                                    {'type':'space', 'val': 'unknown'},
                                ])
    if len(adevs) != 0:
        logging.info(len(adevs))
        assert None, "invalid result"


# -------------------------------------------------------
def _subtest_device_list_08(sds, space_name):
    """ search space + 2 metadata """
    logging.info("search space + 2 metadata (expected 0 result)")
    adevs = sdsadv.list_devices(sds, limit=0,
                                filters=[
                                    {'type':'metadata', 'name': 'key01', 'val': '1'},
                                    {'type':'metadata', 'name': 'key02', 'val': '1'},
                                    {'type':'space', 'val': space_name},
                                    {'type':'of_class', 'val': 'tdd'},
                                ])
    if len(adevs) != 0:
        logging.info(len(adevs))
        assert None, "invalid result"

# -------------------------------------------------------
def _subtest_device_list_09(sds, space_name):
    """ expose metadata """
    logging.info("expose metadata")
    adevs = sdsadv.list_devices(sds, limit=0,
                                filters=[
                                    {'type':'space', 'val': space_name},
                                    {'type':'metadata', 'name': 'key01', 'val': '1'},
                                ],
                                metadatas=['key01'])
    if len(adevs) != 1:
        logging.info(len(adevs))
        assert None, "invalid result"

    if 'key01' not in adevs[0]:
        assert None, "missing metadata"


# -------------------------------------------------------
def _subtest_device_list_10(sds, space_name):
    """ expose multiple metadata """
    logging.info("expose multiple metadata")
    adevs = sdsadv.list_devices(sds, limit=0,
                                filters=[
                                    {'type':'space', 'val': space_name},
                                    {'type':'metadata', 'name': 'key01', 'val': '1'},
                                ],
                                metadatas=['key02', 'key01'])
    if len(adevs) != 1:
        logging.info(len(adevs))
        assert None, "invalid result"

    if 'key01' not in adevs[0]:
        assert None, "missing metadata"


# -------------------------------------------------------
def _subtest_device_list_11(sds, space_name):
    """ expose metadata and no filter """
    logging.info("expose metadata w/o filter")
    adevs = sdsadv.list_devices(sds, limit=0,
                                filters=[
                                    {'type':'space', 'val': space_name},
                                ],
                                metadatas=['key02', 'key01'])

    if len(adevs) != 6:
        logging.info(len(adevs))
        assert None, "invalid result"


# -------------------------------------------------------
def test_device_list():
    """list devices in the SDS with filters"""

    sds = _connect_to_sds()

    space_name = 'tdd-'+str(uuid.uuid4())
    # space_name = 'ex-space-01'

    space = sdsadv.Space(sds=sds, name=space_name)
    try:
        space.create()
    except SDSSpaceError:
        space.refresh()

    net01 = _create_net(sds, space, 
                        name=str(uuid.uuid4()),
                        # name="net01",
                        net='172.16.0.0', prefix=16, 
                        is_block=True)

    net02 = _create_net(sds, space, 
                        name=str(uuid.uuid4()),
                        # name="net03",
                        net='172.16.1.0', prefix=24, 
                        is_block=False,
                        is_terminal=True,
                        parent=net01)

    net03 = _create_net(sds, space, 
                        name=str(uuid.uuid4()),
                        # name="net03",
                        net='172.16.2.0', prefix=24, 
                        is_block=False,
                        is_terminal=True,
                        parent=net01)

    # ------ device ---------
    def create_dev(name, ip, mac, param):
        add = _create_ip_add(sds, space,
                             ipv4=ip,
                             mac=mac)

        dev = sdsadv.Device(name=name,
                            sds=sds)

        dev.set_class_name('tdd')
        dev.add_class_params(param)
        try:
            dev.create()
        except SDSDeviceError:
            dev.refresh()

        devif = sdsadv.DeviceInterface(sds=sds, name='eth0', device=dev)
        devif.set_ipv4(ip)
        devif.set_mac(mac)
        devif.set_space(space)

        try:
            devif.create()
        except SDSDeviceIfError:
            devif.refresh()

        return (add, dev, devif)
        
    
    (add01, dev01, devif01) = create_dev(name = 'tdd-{}'.format(str(uuid.uuid4())),
                                         ip = '172.16.1.135',
                                         mac = '00:00:00:00:01:01',
                                         param = {'key01': '1'})

    (add02, dev02, devif02) = create_dev(name = 'tdd-{}'.format(str(uuid.uuid4())),
                                         ip = '172.16.1.137',
                                         mac = '00:00:00:00:01:02',
                                         param = {'key02': '2'})

    (add03, dev03, devif03) = create_dev(name = 'tdd-{}'.format(str(uuid.uuid4())),
                                         ip = '172.16.2.139',
                                         mac = '00:00:00:00:02:03',
                                         param = None)

    (add04, dev04, devif04) = create_dev(name = 'tdd-{}'.format(str(uuid.uuid4())),
                                         ip = '172.16.2.1',
                                         mac = '00:00:00:00:02:04',
                                         param = None)

    (add05, dev05, devif05) = create_dev(name = 'tdd-{}'.format(str(uuid.uuid4())),
                                         ip = '172.16.2.2',
                                         mac = '00:00:00:00:02:05',
                                         param = None)

    (add06, dev06, devif06) = create_dev(name = 'tdd-{}'.format(str(uuid.uuid4())),
                                         ip = '172.16.2.3',
                                         mac = '00:00:00:00:02:06',
                                         param = None)

    try:
        adevs = sdsadv.list_devices()
        assert None, "sds needed but not trapped"
    except SDSInitError:
        None

    try:
        adevs = sdsadv.list_devices(sds, limit=0,
                                    filters=[
                                        {},
                                    ])
        assert None, "unknown filter not trapped"
    except SDSDeviceError:
        None

    _subtest_device_list_01(sds, space_name)
    _subtest_device_list_02(sds, space_name)
    _subtest_device_list_03(sds, space_name)
    _subtest_device_list_04(sds, space_name)
    _subtest_device_list_05(sds, space_name)
    _subtest_device_list_06(sds)
    _subtest_device_list_07(sds)
    _subtest_device_list_08(sds, space_name)
    _subtest_device_list_09(sds, space_name)
    _subtest_device_list_10(sds, space_name)
    _subtest_device_list_11(sds, space_name)

    dev01.delete()
    dev02.delete()
    dev03.delete()
    dev04.delete()
    dev05.delete()
    dev06.delete()

    space.delete()

