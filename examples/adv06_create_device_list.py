#!/usr/bin/python
# -*-coding:Utf-8 -*
#
# connects to a SOLIDserver and create IP addresses and 
# devices, should be run after adv05
# 
#
##########################################################
import logging
import pprint
import names
import random
import time
import uuid

from SOLIDserverRest import *
from SOLIDserverRest import adv as sdsadv

logging.basicConfig(format='[%(filename)s:%(lineno)d] %(levelname)s: %(message)s',
                    level=logging.INFO)

# configuration - to be adapted
SDS_HOST = "192.168.56.254"
SDS_LOGIN = "ipmadmin"
SDS_PWD = "admin"

logging.info("create a connection to the SOLIDserver")
sds = sdsadv.SDS(ip_address=SDS_HOST,
                 user=SDS_LOGIN,
                 pwd=SDS_PWD)

try:
    sds.connect(method="basicauth")
except SDSError as e:
    logging.error(e)
    exit()

logging.debug(sds)

space = sdsadv.Space(sds=sds, name="StrangeWorld")
try:
    space.create()
except SDSSpaceError:
    space.refresh()

logging.info(space)

ablock = []

# -------------------------------------------------------
def create_rnd_mac():
    return "00:25:%02x:%02x:%02x:%02x" % (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
    )

# ----------------- create block
block_start = 0
for name in ['A', 'B', 'C', 'D']:
    block = sdsadv.Network(sds=sds,
                           space=space,
                           name='pool-{}'.format(name))

    block.set_address_prefix('10.{}.0.0'.format(block_start), 10)
    block.set_is_block(True)
    try:
        block.create()
    except SDSNetworkError:
        block.refresh()
    ablock.append(block)
    block_start += 64


for block in ablock[0:]:
    nets = block.get_subnet_list(depth=0, terminal=1)
    print(nets)

    for net in nets:
        print("{:20s} {}/{}".format(net['subnet_name'],
                                    net['start_hostaddr'],
                                    net['subnet_size']))

        for idev in range(int(random.uniform(0, 12))):
            network = sdsadv.Network(sds=sds,
                                     space=space,
                                     name=net['subnet_name'])
            network.refresh()

            if_name = 'eth0'
            device_name = str(uuid.uuid4())
            mac = create_rnd_mac()
            ip_v4 = network.find_free_ip(1)[0]

            dev = sdsadv.Device(sds=sds, name=device_name)
            dev.create()

            # create ip address in Space
            add = sdsadv.IpAddress(sds=sds,
                                   space=space,
                                   ipv4=ip_v4)
            add.set_mac(mac)
            add.set_name(device_name)
            add.create()

            devif = sdsadv.DeviceInterface(sds=sds, name=if_name, device=dev)
            devif.set_ipv4(ip_v4)
            devif.set_mac(mac)
            devif.set_space(space)
            devif.create()

