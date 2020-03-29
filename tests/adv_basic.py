import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import SOLIDserverRest.adv as sdsadv
from SOLIDserverRest.Exception import SDSNetworkError

try:
    from tests.data_sample import *
except:
    from .data_sample import *

# -------------------------------------------------------
def _create_net(sds, space, name, net, prefix, is_block, is_terminal=False, parent=None):
    net01 = sdsadv.Network(sds=sds,
                           space=space,
                           name=name)

    net01.set_address_prefix(net, prefix)
    net01.set_is_block(is_block)
    net01.set_is_terminal(is_terminal)
    if parent:
        net01.set_parent(parent)

    try:
        net01.create()
    except SDSNetworkError:
        net01.refresh()

    return net01
