#!/usr/bin/python
# -*-coding:Utf-8 -*
#
# disable naming convention issue
# pylint: disable=C0103
##########################################################
"""
Exceptions for the SOLIDServer modules
"""

__all__ = ["SSDError",
           "SSDInitError",
           "SSDServiceError",
           "SSDRequestError",
           "SDSEmptyError",
           "SSDAuthError"]


class SSDError(Exception):
    """ generic class for any exception in SOLIDServer communication """
    def __init__(self, message=""):
        super(SSDError, self).__init__()
        self.message = message

    def __str__(self):
        return "{}".format(self.message)


class SSDInitError(SSDError):
    """ raised when action on non initialized SSD connection """
    def __init__(self, message=""):
        super(SSDInitError, self).__init__("[init] {}".format(message))


class SSDServiceError(SSDError):
    """ raised on unknown service """

    def __init__(self, service_name, message=""):
        super(SSDServiceError, self).__init__(message)
        self.service = service_name

    def __str__(self):
        return "{} on service {}".format(self.message, self.service)


class SSDRequestError(SSDError):
    """ raised when urllib request is failing """

    def __init__(self, method, url, headers, message=""):
        super(SSDRequestError, self).__init__(message)
        self.method = method
        self.url = url
        self.headers = headers

    def __str__(self):
        return "{} with {} {}".format(self.message, self.method, self.url)


class SSDAuthError(SSDError):
    """ raised when auth on request is wrong """

    def __init__(self, message=""):
        super(SSDAuthError, self).__init__("authent: {}".format(message))


class SDSEmptyError(SSDError):
    """ raised when empty answer """

    def __init__(self, message=""):
        super(SDSEmptyError, self).__init__("empty answer: {}".format(message))
