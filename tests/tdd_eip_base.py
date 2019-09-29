# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2019-09-27 16:07:01 alex>
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
    strb = str(bobject)
    logging.debug(strb)

# ------ SDS base object with class params ---
def test_create_base_cp():
    """create a basic object with class params"""
    bobject = sdsadv.ClassParams()
    strb = str(bobject)
    logging.debug(strb)

# -----------------
def test_base_set_cp():
    """set class param on object"""
    bobject = sdsadv.ClassParams()
    bobject.set_class_params({'a': 1, 'b': 2})
    strb = str(bobject)
    logging.debug(strb)

# -----------------
def test_base_decode_cp():
    """decode class param on object"""
    bobject = sdsadv.ClassParams()
    params = {'a': 1, 'b': 2}

    bobject.set_class_params(params)

    bobject.decode_class_params(params, 'c=3')
    if 'c' not in params or params['c'] != "3":
        assert None, "params not updated from string"

    bobject.decode_class_params(params, '')

    stre = bobject.encode_class_params('error')
    stre = bobject.encode_class_params({'domain_list': 'a1;a2;a3'})

    bobject.decode_class_params(params, stre)

    if not isinstance(params['domain_list'], list):
        assert None, "domain list should be a list"

    if not 'a3' in params['domain_list']:
        assert None, "missing a domain"

    strb = str(bobject)
    logging.debug(strb)

# -----------------
def test_base_getset_cp():
    """get and set class param on object"""
    bobject = sdsadv.ClassParams()
    params = {'a': 1, 'b': 2}

    if bobject.set_class_params() is not None:
        assert None, "set class empty failed"

    if bobject.add_class_params() is not None:
        assert None, "add class empty failed"

    if bobject.set_class_params('error') is not None:
        assert None, "set class bad format failed"

    if bobject.add_class_params('error') is not None:
        assert None, "add class bad format failed"

    bobject.set_class_params(params)
    
    if int(bobject.get_class_params('a')) != 1:
        assert None, "get class param failed"

    a_cp = bobject.get_class_params()
    if not isinstance(a_cp, dict):
        assert None, "full class params set should be a dict"

    if bobject.get_class_params(12) is not None:
        assert None, "get class param failed"

    if bobject.get_class_params('c') is not None:
        assert None, "get class param failed"

    bobject.add_class_params({'d':1})
    s_cp = bobject.get_class_params('d')
    if s_cp != 1:
        assert None, "add class param failed"

# -----------------
def test_base_prepare_cp():
    """prepare class param on object"""
    bobject = sdsadv.ClassParams()
    params = {'a': 1, 'b': 2}

    if bobject.prepare_class_params('key', params) is not None:
        assert None, "prepare class w/o cp failed"

    if bobject.set_class_params() is not None:
        assert None, "set class empty failed"

    if bobject.prepare_class_params() is not None:
        assert None, "prepare class empty failed"

    if bobject.prepare_class_params('key') is not None:
        assert None, "prepare class no params failed"

    if bobject.prepare_class_params('key', 'test') is not None:
        assert None, "prepare class not dict failed"

    if bobject.set_class_params(params) is not True:
        assert None, "set class empty failed"

    if bobject.prepare_class_params('key', params) is not True:
        assert None, "prepare class w cp failed"

# -----------------
def test_base_update_cp():
    """update class param on object"""
    bobject = sdsadv.ClassParams()
    params = {'a': 1, 'b': 2}

    if bobject.set_class_params(params) is not True:
        assert None, "set class param failed"

    if bobject.update_class_params() is not None:
        assert None, "update class empty failed"

    if bobject.update_class_params("") is not None:
        assert None, "update class empty string failed"

    if bobject.update_class_params("c=3&d=4") is not True:
        assert None, "update class with string failed"
    if params['c'] != "3":
        assert None, "update class with string failed"

    if bobject.update_class_params({'e':5}) is not True:
        assert None, "update class with dict failed"
    if params['e'] != 5:
        assert None, "update class with string failed"
