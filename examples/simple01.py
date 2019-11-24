#!/usr/bin/python
# -*-coding:Utf-8 -*
#
# connects to a SOLIDserver, get the first space and print its name
#
##########################################################
import logging
import pprint

from SOLIDserverRest import *

logging.basicConfig(format='[%(filename)s:%(lineno)d] %(levelname)s: %(message)s',
                    level=logging.INFO)

# configuration - to be adapted
SDS_HOST = "192.168.56.254"
SDS_LOGIN = "ipmadmin"
SDS_PWD = "admin"


logging.info("create a connection to the SOLIDserver")
SDS = SOLIDserverRest(SDS_HOST)
try:
    SDS.use_native_sds(user=SDS_LOGIN, password=SDS_PWD)
except SDSInitError:
    exit()

SDS.set_ssl_verify(False)

logging.info("sds = %s", SDS)

req_ans = SDS.query('ip_site_list')
logging.debug(req_ans.status_code)
logging.debug(req_ans.headers)
logging.debug(req_ans.encoding)

json_ans = req_ans.json()
logging.debug(json_ans)

if len(json_ans) == 0:
    logging.info("SOLIDserver empty, no space")
    exit(-1)

space_id = int(json_ans[0]['site_id'])
space_name = json_ans[0]['site_name']
logging.info("first space = %s", space_name)

logging.info("close SOLIDserver connexion")
del SDS
