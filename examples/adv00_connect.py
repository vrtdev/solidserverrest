#!/usr/bin/python
# -*-coding:Utf-8 -*
#
# connects to a SOLIDserver
#
##########################################################
import logging
import pprint

import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from SOLIDserverRest import *
from SOLIDserverRest import adv as sdsadv

logging.basicConfig(format='[%(filename)s:%(lineno)d] %(levelname)s: %(message)s',
                    level=logging.INFO)

# configuration - to be adapted
SDS_HOST_IP = "192.168.16.117"
SDS_HOST_NAME = "sds117.home"
SDS_LOGIN = "ipmadmin"
SDS_PWD = "admin"

logging.info("create a connection to the SOLIDserver using IP")

sds = sdsadv.SDS(ip_address=SDS_HOST_IP,
                 user=SDS_LOGIN,
                 pwd=SDS_PWD)

try:
    sds.connect()
except SDSError as e:
    logging.error(e)
    exit()

logging.info(sds)

del sds

logging.info("create a connection to the SOLIDserver using FQDN")

sds = sdsadv.SDS(user=SDS_LOGIN,
                 pwd=SDS_PWD)
sds.set_server_name(SDS_HOST_NAME)

try:
    sds.connect()
except SDSError as e:
    logging.error(e)
    exit()

logging.info(sds)

del sds
