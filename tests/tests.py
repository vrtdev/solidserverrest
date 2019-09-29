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

logging.info('START => test.py')

def test_no_server():
    logging.info('TEST: Test no server')
    try:
        testR = SOLIDserverRest(None)
        testR.use_native_sds('soliduser', 'solidpass')
        logging.info('Test = NO-OK')
        assert None, "test without server, should have failed"
    except SDSError as e:
        logging.info('Test = OK {}'.format(str(e)))
        None

def test_auto_dico_native_srv():
    fct_auto_dico()

def test_auto_dico_native_no_srv():
    fct_auto_dico(srv=None)

def test_auto_dico_basic_srv():
    fct_auto_dico(SOLIDserverRest.CNX_BASIC)

def test_auto_dico_basic_nosrv():
    fct_auto_dico(SOLIDserverRest.CNX_BASIC, None)

def fct_auto_dico(auth=SOLIDserverRest.CNX_NATIVE, srv=SERVER, options=False):
    logging.info('================================')
    logging.info('TESTS AUTO')
    logging.info('================================')
    testR = SOLIDserverRest(srv)
    sds_str = str(testR)
    testR.set_ssl_verify(False)

    try:
        if auth==SOLIDserverRest.CNX_NATIVE:
            testR.use_native_sds(USER, PWD)
        elif auth==SOLIDserverRest.CNX_BASIC:
            testR.use_basicauth_sds(USER, PWD)
    except SDSInitError as error:
        logging.info(error)
        if srv is not None:
            assert None, "server connect error {}".format(srv)
        return

    logging.info('IP of th server: {}'.format(SERVER))
    logging.info('User: {}'.format(USER))
    logging.info('Password: {}'.format(PWD))

    total_services = 0
    check_services = 0
    total_methods = len(set(METHOD_MAPPER.values()))
    total_services = len(SERVICE_MAPPER)

    method_tested = []

    for cle in SERVICE_MAPPER:
        serviceR = cle
        parameters = PARAMETERS

        method = None
        for verb in METHOD_MAPPER:
            _q = ".*_{}$".format(verb)
            if re.match(_q, cle) is not None:
                method = METHOD_MAPPER[verb]
                break

        logging.info('--------------------------------')
        logging.info('Sub Test: {}'.format(serviceR))
        logging.info('Parameters: {}'.format(parameters))
        logging.info('method: {}'.format(method))
            
        try:
            answerR = testR.query(serviceR, parameters, option=options, timeout=0.2)
            logging.info('Answer: {}'.format(answerR))
            logging.info('Answer: {}'.format(answerR.status_code))
            logging.info('Answer:')
            logging.debug(answerR.content)
        except SDSError as e:
            logging.info("error on SDS query - {}".format(str()))
            None

        if method not in method_tested:
            method_tested.append(method)

        logging.info('--------------------------------')
        check_services += 1

        if len(method_tested) == total_methods:
            break

    logging.info('RESULTAT')
    logging.info('{} services checked / {} total services'.format(check_services, total_services))

    logging.info('END of TEST AUTO')


def test_ukn_svc(auth=SOLIDserverRest.CNX_NATIVE, srv=SERVER):
    logging.info('================================')
    logging.info('TEST UKN service')
    logging.info('================================')
    testR = SOLIDserverRest(srv)

    if auth==SOLIDserverRest.CNX_NATIVE:
        testR.use_native_sds(USER, PWD)
    elif auth==SOLIDserverRest.CNX_BASIC:
        testR.use_basicauth_sds(USER, PWD)

    try:
        answerR = testR.query('ukn_service_list', PARAMETERS, timeout=1)
        logging.info('Answer: {}'.format(answerR))
        logging.info('Answer: {}'.format(answerR.status_code))
        logging.info('Answer:')
        logging.info(answerR.content)
    except SDSServiceError as e:
        logging.info("unknown service - {}".format(str(e)))        
        return

    assert None, "ukn service should have raised an error"

def test_no_params(auth=SOLIDserverRest.CNX_NATIVE, srv=SERVER):
    logging.info('================================')
    logging.info('TEST no params')
    logging.info('================================')
    testR = SOLIDserverRest(srv)

    if auth==SOLIDserverRest.CNX_NATIVE:
        testR.use_native_sds(USER, PWD)
    elif auth==SOLIDserverRest.CNX_BASIC:
        testR.use_basicauth_sds(USER, PWD)

    try:
        answerR = testR.query('ukn_service_list')
        logging.info('Answer: {}'.format(answerR))
        logging.info('Answer: {}'.format(answerR.status_code))
        logging.info('Answer:')
        logging.info(answerR.content)
    except SDSServiceError:
        logging.info("error on SDS query in test_no_params")
        None

def test_method_none():
    logging.info('================================')
    logging.info('TEST method none')
    logging.info('================================')
    testR = SOLIDserverRest(SERVER)

    testR.use_basicauth_sds(USER, PWD)

    try:
        answerR = testR.query('ukn_service_none', timeout=1)
        logging.info('Answer: {}'.format(answerR))
        logging.info('Answer: {}'.format(answerR.status_code))
        logging.info('Answer:')
        logging.info(answerR.content)
    except SDSServiceError:
        logging.info("error on SDS query in test_no_params")
        None

def test_get_headers():
    logging.info('================================')
    logging.info('TEST get headers')
    logging.info('================================')
    testR = SOLIDserverRest(SERVER)
    testR.use_basicauth_sds(USER, PWD)

    testR.get_headers()

def test_get_status():
    logging.info('================================')
    logging.info('TEST get status')
    logging.info('================================')
    testR = SOLIDserverRest(SERVER)
    testR.use_basicauth_sds(USER, PWD)

    testR.get_status()

def test_get_string():
    logging.info('================================')
    logging.info('TEST get string')
    logging.info('================================')
    testR = SOLIDserverRest(SERVER)
    testR.use_basicauth_sds(USER, PWD)
    # print(testR)

def test_options():
    fct_auto_dico(SOLIDserverRest.CNX_BASIC, SERVER, options=True)


def test_get_memberme():
    logging.info('================================')
    logging.info('TEST get memberme')
    logging.info('================================')
    testR = SOLIDserverRest(SERVER)
    testR.use_basicauth_sds(USER, PWD)
    parameters = {
        'WHERE': 'member_is_me=1',
    }

    j = None
    try:
        answerR = testR.query("member_list", params=parameters, option=False, timeout=1)
        logging.info('Answer: {}'.format(answerR))
        logging.info('Answer: {}'.format(answerR.status_code))
        #logging.info('Answer:')
        #logging.info(answerR.content)
        j = json.loads(answerR.content)
    except SDSError as e:
        logging.info("error on SDS query - {}".format(str(e)))
        return

    if j is None:
        assert None, "no json result from member_list request"
        return

    if j[0]['member_is_me'] != '1':
        assert None, "member list should have a me item"
        return

def test_use_validcert():
    testR = SOLIDserverRest(SERVER)
    testR.set_certificate_file("ca.crt")

def test_use_invalidcert():
    testR = SOLIDserverRest(SERVER)
    try:
        testR.set_certificate_file("ca-invalid.crt")
    except SDSInitError:
        return

    assert None, "no certificate file provided, should have failed"

def test_use_missingcert():
    testR = SOLIDserverRest(SERVER)
    try:
        testR.set_certificate_file("ca-missing.crt")
    except SDSInitError:
        return

    assert None, "no certificate file provided, should have failed"

def test_ssl_verify_bad_param():
    testR = SOLIDserverRest(SERVER)
    try:
        testR.set_ssl_verify("test")
    except SDSError:
        return

    assert None, "bool check to ssl_verify"

if __name__ == '__main__':
    # test_get_string()
    test_auto_dico_native_srv()

logging.info('END => test.py')
