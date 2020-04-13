#!/usr/bin/python
# -*-coding:Utf-8 -*
#
# connects to a SOLIDserver and list all devices
#  with some filters
#
# python -m cProfile -s cumtime
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
SDS_HOST = "192.168.16.117"
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

space = sdsadv.Space(sds=sds, name="StrangeWorld")
space.refresh()

adevs = sdsadv.list_devices(sds, limit=10,
                            filters=[
                                # { 'type':'in_subnet', 'val': '10.156.48.0/24'},
                                # {'type':'in_subnet', 'val': '10.149.0.0/16'},
                                # {'type':'of_class', 'val': 'AWS-EC2'},
                                # {'type':'metadata', 'name': 'cores', 'val': '1'},
                                # {'type':'metadata', 'name': 'monitoring', 'val': 'on'},
                                # {'type':'space', 'val': 'ex-space-01'},

                                # {'type':'metadata', 'name': 'key01', 'val': '1'},
                                # {'type':'space', 'val': 'ex-space-01'},
                                # {'type':'of_class', 'val': 'tdd'},
                            ],
                            metadatas=['monitoring'] 
                            # metadatas=['env']
                            )

print("found ", len(adevs))
pprint.pprint(adevs[:5])
