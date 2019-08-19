# -*- Mode: Python; python-indent-offset: 4 -*-
# -*-coding:Utf-8 -*
#
# Time-stamp: <2019-07-06 19:04:08 alex>
#
# disable naming convention issue
# pylint: disable=C0103
##########################################################
# Request example:
# http://<SOLIDserver-IP>/rest/<service>?<param> [param=URLencode(value)]
###########################################################

"""
Efficient IP low level SOLIDServer API binding
"""

import sys
import base64
import re
import logging
import urllib
from OpenSSL import crypto

import requests
# pylint: disable=F0401, E1101
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# pylint: enable=F0401, E1101

if sys.version_info[0] == 2:
    # pylint: disable=F0401
    from mapper import SERVICE_MAPPER, METHOD_MAPPER
    from Exception import SDSInitError, SDSError
    from Exception import SDSServiceError, SDSRequestError
    # pylint: enable=F0401
else:
    from .mapper import SERVICE_MAPPER, METHOD_MAPPER
    from .Exception import SDSInitError, SDSError
    from .Exception import SDSServiceError, SDSRequestError

__all__ = ["SOLIDserverRest"]

##########################################################################


# effectively few variables in this class, just disabling the warning
# pylint: disable=R0902
class SOLIDserverRest:
    """ main SDS class """
    CNX_NATIVE = 1
    CNX_APIKEY = 2
    CNX_BASIC = 3

    def __init__(self, host, debug=False):
        """ initialize connection with SDS host,
            this function is not active,
            just set host and parameters
        """

        self.auth = None
        self.cnx_type = None
        self.debug = debug
        self.headers = None
        self.host = host
        self.last_url = ''
        self.password = None
        self.resp = None
        self.user = None
        self.session = None
        self.prefix_url = 'https://{}/rest/'.format(host)
        self.python_version = 0
        self.fct_url_encode = None
        self.fct_b64_encode = None
        self.ssl_verify = True

        # set specific features for python v2 (<=2020, not supported after)
        if sys.version_info[0] == 2:
            # pylint: disable=E1101
            self.python_version = 2
            self.fct_url_encode = urllib.urlencode
            self.fct_b64_encode = base64.standard_b64encode
            # pylint: enable=E1101
        else:
            self.python_version = 3
            self.fct_url_encode = urllib.parse.urlencode
            self.fct_b64_encode = base64.b64encode

        self.last_url = ''
        self.resp = None

        self.session = requests.Session()
        # self.session.verify = "cert.pem"

    def __del__(self):
        self.clean()

    def use_native_sds(self, user, password):
        """ propose to use a native EfficientIP SDS connection with Username
        and password encoded in the headers of each requests
        """
        logging.debug("useNativeSDS %s %s", user, password)

        # check if SDS connection is established
        if self.host is None:
            raise SDSInitError()

        self.user = user
        self.password = password
        self.cnx_type = self.CNX_NATIVE

        # Encryption management in function of Python version
        self.headers = {
            'X-IPM-Username': self.fct_b64_encode(user.encode()),
            'X-IPM-Password': self.fct_b64_encode(password.encode()),
            'content-type': 'application/json'
        }

    def use_basicauth_sds(self, user, password):
        """ propose to use the basic auth implementation on the SDS
        """
        logging.debug("useBasicAuthSDS %s %s", user, password)

        # check if SDS connection is established
        if self.host is None:
            raise SDSInitError()

        self.user = user
        self.password = password

        self.cnx_type = self.CNX_BASIC
        self.session.auth = requests.auth.HTTPBasicAuth(user, password)

        self.headers = {
            'content-type': 'application/json'
        }

    def set_certificate_file(self, file_path):
        """set the certificate that will be used to authenticate the server"""
        try:
            file_content = open(file_path, 'r').read()
            crypto.load_certificate(crypto.FILETYPE_PEM,
                                    file_content)
        except IOError:
            logging.error("cannot load CA file")
            raise SDSInitError("cannot load CA file {}".format(file_path))
        except crypto.Error as error:
            logging.error(error)
            raise SDSInitError("invalid CA file {}".format(file_path))

        self.session.verify = file_path
        self.ssl_verify = True

    def set_ssl_verify(self, value):
        """allows to enable or disable the certificate validation"""
        if isinstance(value, bool):
            self.ssl_verify = value
        else:
            logging.error("bad type when calling set_ssl_verify")
            raise SDSError("requested bool on set_ssl_verify")

    def query(self, service,
              params=None,
              timeout=2,
              option=False):
        """ send request to the API endpoint, returns request result """

        if params is not None:
            params = "?"+self.fct_url_encode(params)
        else:
            params = ''

        # choose method
        method = None
        if option:
            method = 'OPTIONS'
            params = ''
        else:
            for verb in METHOD_MAPPER:
                _q = ".*_{}$".format(verb)
                if re.match(_q, service) is not None:
                    method = METHOD_MAPPER[verb]
                    break

        if method is None:
            msg = "no method available for request {}".format(service)
            logging.error("no method available for request %s", service)
            raise SDSServiceError(service,
                                  message=msg)

        logging.debug("method %s selected for service %s", method, service)

        # flag_add management
        if method == 'POST':
            params = "{}{}".format(params, '&add_flag=new_only')
        elif method == 'PUT':
            params = "{}{}".format(params, '&add_flag=edit_only')

        # choose service
        svc_mapped = SERVICE_MAPPER.get(service)
        if svc_mapped is None:
            logging.error("unknown service %s", service)
            raise SDSServiceError(service)

        self.last_url = "{}{}".format(svc_mapped, params).strip()
        url = "{}{}".format(self.prefix_url, self.last_url)

        try:
            logging.debug("m=%s u=%s h=%s v=%s a=%s",
                          method,
                          url,
                          self.headers,
                          self.ssl_verify,
                          self.auth)

            return self.session.request(
                method,
                url,
                headers=self.headers,
                verify=self.ssl_verify,
                timeout=timeout,
                auth=self.auth)
        except requests.exceptions.SSLError:
            raise SDSRequestError(method,
                                  url,
                                  self.headers,
                                  message="SSL certificate error")
        except BaseException as error:
            raise SDSRequestError(method, url, self.headers, message=error)

    def get_headers(self):
        """ returns the headers attached to this connection """
        return self.headers

    def get_status(self):
        """ returns status of the SDS connection """
        _r = {
            'host': self.host,
            'python_version': self.python_version
        }
        return _r

    def clean(self):
        """ clean all status of the SDS connection """
        self.auth = None
        self.cnx_type = None
        self.debug = None
        self.headers = None
        self.host = None
        self.last_url = ''
        self.password = None
        self.prefix_url = None
        self.python_version = None
        self.resp = None
        self.user = None
        self.session = None
        self.ssl_verify = True

    def __str__(self):
        _s = "SOLIDserverRest: API={}, user={}"
        return(_s.format(self.prefix_url,
                         self.user))

    # deprecated method to be suppressed

    def use_native_ssd(self, user, password):
        """deprecated version of use_native_sds"""
        logging.critical("deprecated method use_native_ssd")
        self.use_native_sds(user, password)

    def use_basicauth_ssd(self, user, password):
        """deprecated version of use_basicauth_ssd"""
        logging.critical("deprecated method use_basicauth_ssd")
        self.use_basicauth_sds(user, password)