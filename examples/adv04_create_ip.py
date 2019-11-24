#!/usr/bin/python
# -*-coding:Utf-8 -*
#
# connects to a SOLIDserver, create space & nets
#
##########################################################
import logging
import pprint
import uuid

from SOLIDserverRest import *
from SOLIDserverRest import adv as sdsadv

logging.basicConfig(format='[%(filename)s:%(lineno)d] %(levelname)s: %(message)s',
                    level=logging.INFO)

# configuration - to be adapted
SDS_HOST = "192.168.56.254"
SDS_LOGIN = "ipmadmin"
SDS_PWD = "admin"


def adv03():
    global sds, space, block, net02, net03

    sds = sdsadv.SDS(ip_address=SDS_HOST,
                     user=SDS_LOGIN,
                     pwd=SDS_PWD)

    try:
        sds.connect(method="native")
    except SDSError as e:
        logging.error(e)
        exit()

    space_name = 'ex-space-'+str(uuid.uuid4())

    space = sdsadv.Space(sds=sds, name=space_name)
    space.create()

    # ----------------- create block
    block = sdsadv.Network(sds=sds,
                           space=space,
                           name='ex-block-'+str(uuid.uuid4()))

    block.set_address_prefix('172.16.0.0', 16)
    block.set_is_block(True)
    block.create()

    # ----------------- create net in block
    net02 = sdsadv.Network(sds=sds,
                           space=space,
                           name='ex-net-'+str(uuid.uuid4()))

    net02.set_address_prefix('172.16.10.0', 24)
    net02.set_parent(block)
    net02.set_is_terminal(False)
    net02.create()

    # ----------------- create terminal net in previous super net
    net03 = sdsadv.Network(sds=sds,
                           space=space,
                           name='ex-term-'+str(uuid.uuid4()))

    net03.set_address_prefix('172.16.10.128', 25)
    net03.set_parent(net02)
    net03.set_is_terminal(True)
    net03.create()


adv03()

add = sdsadv.IpAddress(sds=sds,
                       space=space,
                       ipv4='172.16.10.135')
add.create()

logging.info(add)
