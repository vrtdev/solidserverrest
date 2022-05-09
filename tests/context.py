import sys
import os
import logging

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

from SOLIDserverRest import *   # nopep8
import SOLIDserverRest.adv as sdsadv   # nopep8

try:
    from tests.data_sample import *
except:
    from .data_sample import *

# -------------------------------------------------------


def _connect_to_sds():
    sds = sdsadv.SDS()
    sds.set_server_ip(SERVER)
    sds.set_credentials(user=USER, pwd=PWD)

    try:
        sds.connect(method="basicauth", cert_file_path="ca.crt", timeout=10)
        return sds
    except SDSError as e:
        logging.debug("certificate error, fallback to no TLS validation")

    try:
        sds.connect(method="basicauth", timeout=10)
        return sds
    except SDSError as e:
        logging.debug(e)
        assert None, "connection error"
