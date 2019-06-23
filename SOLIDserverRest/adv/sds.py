# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2019-06-23 18:37:03 alex>
#
# only for python v3

"""
SOLIDserver management server access
"""

import logging
import ipaddress

from json.decoder import JSONDecodeError

from SOLIDserverRest.Exception import SSDInitError, SSDAuthError
from SOLIDserverRest.Exception import SDSEmptyError
from SOLIDserverRest import SOLIDserverRest

from .class_params import ClassParams

__all__ = ["SDS"]


class SDS(ClassParams):
    """ class to get connected to a SDS server """
    # ---------------------------
    def __init__(self, ip_address=None, user=None, pwd=None):
        """init the SDS object:
        """
        super(SDS, self).__init__()

        self.sds_ip = None
        if ip_address is not None:
            self.set_server_ip(ip_address)

        self.user = None
        self.pwd = None
        if user is not None and pwd is not None:
            self.set_credentials(user, pwd)

        self.version = None

        self.auth_method = None
        self.check_certificate = False

        self.sds = None

    # ---------------------------
    def set_server_ip(self, ip_address):
        """set the SOLIDserver IP address for the connection"""
        try:
            ipaddress.IPv4Address(ip_address)
        except ipaddress.AddressValueError as error:
            raise SSDInitError(message="IPv4 address of server error: {}".
                               format(error))

        self.sds_ip = ip_address

    # ---------------------------
    def set_credentials(self, user=None, pwd=None):
        """add user and login to credentials of this session"""
        if user is None or pwd is None:
            msg = "missing user or password in credentials"
            raise SSDInitError(message=msg)
        self.user = user
        self.pwd = pwd

    # ---------------------------
    def connect(self, method="basicauth", cert_file_path=None):
        """connects to SOLIDserver and check everything is OK by
           querying the version of the admin node in the member list

           method -- basicauth (default) or native (header based)
           cert_file_path -- disable SSL check if None (default)
                             file with cert if check enabled
        """
        if self.user is None or self.pwd is None:
            msg = "missing user or password in credentials for connect"
            raise SSDInitError(message=msg)
        if self.sds_ip is None:
            raise SSDInitError(message="missing ip for server for connect")

        self.sds = SOLIDserverRest(self.sds_ip)

        if method == "basicauth":
            self.sds.use_basicauth_ssd(self.user, self.pwd)
            self.auth_method = "basic auth"
        elif method == "native":
            self.sds.use_native_ssd(self.user, self.pwd)
            self.auth_method = "native"

        # certificate & SSL check
        if cert_file_path is not None:
            self.sds.set_certificate_file(cert_file_path)
            self.check_certificate = True
        else:
            self.sds.set_ssl_verify(False)

        self.version = self.get_version()

        if self.version is None:
            raise SSDInitError(message="version of SOLIDserver not found")

    # ---------------------------
    def get_version(self):
        """get software version of the SDS based on the management platform
        returns version as a string
        """

        if self.version is not None:
            return self.version

        j = self.query("member_list",
                       params={
                           'WHERE': 'member_is_me=1',
                       },
                       option=False,
                       timeout=2)

        if j is None:
            logging.error("error in getting answer on version")
            return None

        if 'member_is_me' not in j[0]:
            logging.error("error in getting version")
            return None

        self.version = j[0]['member_version']
        return self.version

    # ---------------------------
    def query(self, method, params=None, option=False, timeout=1):
        """execute a query towards the SDS"""

        try:
            answer_req = self.sds.query(method,
                                        params=params,
                                        option=option,
                                        timeout=timeout)

            if answer_req.status_code == 401:
                raise SSDAuthError(message="authentication error")

            if answer_req.status_code == 204:
                raise SDSEmptyError(message="204 returned")

            try:
                j = answer_req.json()
                return j
            except JSONDecodeError:
                logging.error("no json in return")
                return None

        except SSDAuthError as error:
            raise SSDAuthError("{}".format(error))

        return None

    # ---------------------------
    def __str__(self):
        """return the string notation of the server object"""
        connected = "not connected"
        if self.version is not None:
            connected = "connected version={} auth={}".format(self.version,
                                                              self.auth_method)

        return "sds ip={} cred={}:{} {} [{}]".format(self.sds_ip,
                                                     self.user,
                                                     self.pwd,
                                                     connected,
                                                     self.sds)
