# -*- Mode: Python; python-indent-offset: 4 -*-
# -*-coding:Utf-8 -*
#
# Time-stamp: <2019-06-23 15:00:18 alex>
#
# disable naming convention issue
# pylint: disable=C0103
##########################################################

"""
init of the SOLIDserver module
"""

import sys

if sys.version_info[0] == 2:
    # pylint: disable=F0401, W0406
    from SOLIDserverRest import *
    from mapper import *
    from Exception import *
    # pylint: enable=F0401, W0406
else:
    from .mapper import *
    from .SOLIDserverRest import *
    from .Exception import *
