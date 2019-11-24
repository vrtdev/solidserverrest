#!/usr/bin/python
# -*-coding:Utf-8 -*
#
# connects to a SOLIDserver, get the first space and print its name
#
##########################################################
import logging
import pprint

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
    sds.connect(method="native")
except SDSError as e:
    logging.error(e)
    exit()

logging.debug(sds)

space = sdsadv.Space(sds=sds, name="Local")
space.refresh()

logging.debug(space.myid)

logging.info("space = %s / %d", space.name, space.myid)

del sds
