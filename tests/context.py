import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import SOLIDserverRest.adv as sdsadv

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
        sds.connect(method="basicauth", cert_file_path="ca.crt")
    except SDSError as e:
        logging.debug(e)
        assert None, "connection error, probable certificate issue"

    return sds
