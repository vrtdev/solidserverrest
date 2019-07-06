# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2019-07-06 18:53:30 alex>
#

"""test file for the eip advance suite package, base class object"""

import logging
import sys

from SOLIDserverRest.Exception import SDSInitError, SDSRequestError, SDSAuthError, SDSError

try:
    from tests.data_sample import *
except:
    from .data_sample import *

from .context import sdsadv

# ------ SDS base object ---------------------
def test_create_base():
    """create a basic object"""
    bobject = sdsadv.Base()
    logging.info(bobject)

# ------ SDS base object with class params ---
def test_create_base_cp():
    """create a basic object with class params"""
    bobject = sdsadv.ClassParams()
    logging.info(bobject)
