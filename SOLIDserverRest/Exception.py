#!/usr/bin/python
# -*-coding:Utf-8 -*
##########################################################
"""
Exceptions for the SOLIDServer modules
"""

__all__ = ["SSDError",
           "SSDInitError",
           "SSDServiceError",
           "SSDRequestError"]


class SSDError(Exception):
    """ generic class for any exception in SOLIDServer communication """
    def __init__(self, message=""):
        self.message = message

    def __str__(self):
        return "{}".format(self.message)


class SSDInitError(SSDError):
    """ raised when action on non initialized SSD connection """
    pass


class SSDServiceError(SSDError):
    """ raised on unknown service """

    def __init__(self, service_name, message=""):
        self.service = service_name
        self.message = message

    def __str__(self):
        return "{} on service {}".format(self.message, self.service)

class SSDRequestError(SSDError):
    """ raised when urllib request is failing """

    def __init__(self, method, url, headers, message=""):
        self.message = message
        self.method = method
        self.url = url
        self.headers = headers

    def __str__(self):
        return "{} with {} {}".format(self.message, self.method, self.url)
