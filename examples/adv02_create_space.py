#!/usr/bin/python
# -*-coding:Utf-8 -*
#
# connects to a SOLIDserver, create a new space
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

sds = sdsadv.SDS(ip_address=SDS_HOST,
                 user=SDS_LOGIN,
                 pwd=SDS_PWD)

try:
    sds.connect(method="native")
except SDSError as e:
    logging.error(e)
    exit()

space_name = 'ex_'+str(uuid.uuid4())

space = sdsadv.Space(sds=sds, name=space_name)
space.create()

logging.info(space)
