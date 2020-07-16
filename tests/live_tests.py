#!/usr/bin/python
# -*-coding:Utf-8 -*
##########################################################
import sys
import os
import json
import re
import logging


_logFormat = '%(asctime)-15s [%(levelname)s] %(filename)s:%(lineno)d - %(message)s'
logging.basicConfig(format=_logFormat, level=logging.ERROR)

sys.path.append(os.getcwd())

from SOLIDserverRest import *
from SOLIDserverRest.Exception import *

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

if sys.version_info[0] == 2:
    try:
        from data import *
    except:
        from data_sample import *
else:
    try:
        from tests.data_sample import *
    except:
        from .data_sample import *


def test_socks():
    testR = SOLIDserverRest(SERVER)
    testR.set_proxy('127.0.0.1:9001')
    testR.set_certificate_file("ca.crt")
    testR.use_basicauth_sds(user=USER, password=PWD)
    testR.set_ssl_verify(True)

    if testR.get_proxies() is None:
        assert None, "no proxies found"
    
    rest_answer = testR.query("ip_site_list")
    if rest_answer.status_code != 200:
        assert None, "cannot find space list, connection not working"

