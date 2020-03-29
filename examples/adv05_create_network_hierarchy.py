#!/usr/bin/python
# -*-coding:Utf-8 -*
#
# connects to a SOLIDserver, create a space and a full net
# hierarchy with 4 block and around 1000 networks
#
##########################################################
import logging
import pprint
import names
import random
import time

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

def add_subnet_in_block(name, parent, size, terminal=False):
    aip_proposals = parent.find_free(size)
    if aip_proposals is None:
        return None

    # ----------------- create net in block
    net = sdsadv.Network(sds=sds,
                         space=space,
                         name=name)

    net.set_address_prefix(aip_proposals[0], size)
    net.set_parent(parent)
    net.set_is_terminal(terminal)

    try:
        net.create()
    except SDSNetworkError:
        return None

    return net

space = sdsadv.Space(sds=sds, name="StrangeWorld")
try:
    space.create()
except SDSSpaceError:
    space.refresh()

logging.info(space)

ablock = []

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

for block in ablock:
    for netx in range(int(random.uniform(6, 12))):
        sizex = int(random.uniform(14, 17))
        subnetx = add_subnet_in_block(names.get_full_name(),
                                      block, sizex, False)

        if subnetx is not None:
            print(" {}".format(sizex))
            for nety in range(int(random.uniform(4, 18))):
                sizey = int(random.uniform(sizex+4, sizex+7))
                subnety = add_subnet_in_block(names.get_full_name(),
                                              subnetx, sizey, bool(sizey>=20))
                if subnety is not None:
                    print("   {}".format(sizey))

                    if sizey < 20:
                        for netz in range(int(random.uniform(4, 8))):
                            sizez = int(random.uniform(sizey+3, sizey+7))
                            subnetz = add_subnet_in_block(names.get_full_name(),
                                                          subnety, sizez, True)

                            if subnetz is not None:
                                print("     {}".format(sizez))

# add_subnet_in_block(names.get_full_name(), blockA, 16, False)

# del sds
