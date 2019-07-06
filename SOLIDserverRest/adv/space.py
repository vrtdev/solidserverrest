#
# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2019-07-06 18:47:28 alex>
#

"""
SOLIDserver space management
"""

# import logging

from SOLIDserverRest.Exception import SDSInitError, SDSError
from SOLIDserverRest.Exception import SDSEmptyError

from .class_params import ClassParams


class Space(ClassParams):
    """ class to manipulate the SOLIDserver spaces """

    def __init__(self, sds=None, name="Local"):
        """init the space object:
        - sds: object SOLIDserver, could be set afterwards
        - name: space name, default Local
        """
        self.name = name
        self.sds = sds

        self.space_params = {
            'site_is_template': None,
            'site_id': None,
            'tree_level': None,
            'site_name': None,
            'site_description': None,
            'parent_site_id': None,
            'parent_site_name': None,
            'site_class_name': None,
            'parent_site_class_name': None,
            'row_enabled': None,
            'multistatus': None,
        }

        super(Space, self).__init__()

    def create(self):
        """creates the space in the SDS"""
        if self.sds is None:
            raise SDSInitError(message="not connected")

        space_id = self._get_siteid_by_name(self.name)
        if space_id is not None:
            raise SDSError(message="already existant space")

    def _get_siteid_by_name(self, name):
        """get the space ID from its name, return None if non existant"""

        try:
            rjson = self.sds.query("ip_site_list",
                                   params={
                                       "WHERE": "site_name='{}'".
                                                format(name),
                                   })
        except SDSEmptyError:
            return None

        if rjson[0]['errno'] != '0':
            raise SDSError("errno raised")

        return rjson[0]['site_id']

    def refresh(self):
        """refresh content of the object from the SDS"""
        if self.sds is None:
            raise SDSInitError(message="not connected")

        space_id = self._get_siteid_by_name(self.name)
        if space_id is None:
            raise SDSEmptyError(message="non existant space")

        rjson = self.sds.query("ip_site_info",
                               params={
                                   "site_id": space_id,
                               })

        rjson = rjson[0]

        for label in ['site_is_template',
                      'site_id',
                      'tree_level',
                      'site_name',
                      'site_description',
                      'parent_site_id',
                      'parent_site_name',
                      'site_class_name',
                      'parent_site_class_name',
                      'row_enabled',
                      'multistatus']:
            if label not in rjson:
                raise SDSError("parameter {} not found in space".format(label))
            self.space_params[label] = rjson[label]

        if 'site_class_parameters' in rjson:
            self.decode_class_params(self.space_params,
                                     rjson['site_class_parameters'],
                                     )

    def __str__(self):
        """return the string notation of the space object"""
        return "space name={}".format(self.name)
