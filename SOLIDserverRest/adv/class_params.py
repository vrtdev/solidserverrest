# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2019-06-23 18:41:05 alex>
#
# only for python v3

"""
SOLIDserver base object with class parameters
"""

import base64
import urllib
# import logging

from .base import Base

__all__ = ["ClassParams"]


class ClassParams(Base):
    """ standard class for all objects in SDS with class parameters """
    # ---------------------------
    def __init__(self):
        """init the object:
        """
        super(ClassParams, self).__init__()

        self.fct_url_encode = urllib.parse.urlencode
        self.fct_b64_encode = base64.b64encode

        self.dclasses = {}

    # ---------------------------
    def __str__(self):
        """return the string notation of the base object
           with class parameters"""
        return "ClassParams"

    # ---------------------------
    @classmethod
    def decode_class_params(cls, params, site):
        """push decoded parameters in the params structure"""
        if site == "":
            return

        dir_site = urllib.parse.parse_qsl(site)

        params.update(dir_site)

        if 'domain_list' in params:
            dlist = str.split(params['domain_list'], ';')
            params['domain_list'] = dlist
