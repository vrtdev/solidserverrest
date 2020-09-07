# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2020-05-14 21:46:44 alex>
#
# only for python v3

"""
SOLIDserver base object
"""

# import logging

from SOLIDserverRest.Exception import SDSError


__all__ = ["Base"]


# just container class, no need for methods
# pylint: disable=R0903
class Base:
    """ standard class for all objects in SDS """
    # ---------------------------

    def __init__(self, sds=None, name=None):
        """init the base object:
        """

        # if true, modification on object are pushed to SDS
        self.in_sync = False

        self.sds = sds
        self.set_sds(sds)
        self.myid = -1
        self.name = name
        self.set_name(name)
        self.params = {}
        self.additional_params = {}

    # -------------------------------------
    def clean_params(self):
        """ clean the object params """
        self.in_sync = False
        self.sds = None
        self.myid = -1
        self.name = None
        self.params = {}

    # ---------------------------
    def set_sds(self, sds=None):
        """set the sds connection for this object"""
        self.sds = sds

    # ---------------------------
    def set_name(self, name=None):
        """set the name for this object"""
        if name is None:
            self.name = None
            return

        if isinstance(name, str):
            self.name = name
        else:
            self.name = None
            raise SDSError("name format not valid")

    # ---------------------------
    def set_sync(self):
        """set the object modification sync with SDS"""
        self.in_sync = True

    # ---------------------------
    def set_async(self):
        """set the object modification async with SDS,
           calling update() required"""
        self.in_sync = False

    # ---------------------------
    def __str__(self):
        """return the string notation of the base object"""
        return " sync: {}".format(self.in_sync)

    # -------------------------------------
    def _get_id_by_name(self, query, key, name):
        """get the ID from its name, return None if non existant"""

        params = {
            "WHERE": "{}_name='{}'".format(key, name),
            "limit": 1,
        }

        # pylint: disable=E1101
        if hasattr(self, 'space'):
            if self.space:
                params['WHERE'] += " and site_id={}".format(self.space.myid)

        # logging.info(query)
        # logging.info(params)

        try:
            rjson = self.sds.query(query,
                                   params=params)
        except SDSError as err_descr:
            msg = "cannot found object by name {}={}".format(key, name)
            msg += " / "+str(err_descr)
            raise SDSError(msg)

        if rjson[0]['errno'] != '0':  # pragma: no cover
            raise SDSError("errno raised on get id by name")

        return rjson[0]['{}_id'.format(key)]

    # -------------------------------------
    def _get_id(self, query, key):
        """get the ID for the current object based
           on its current name
        """

        if self.myid >= 0:
            return self.myid

        if self.params['{}_id'.format(key)] is None:
            _id = self._get_id_by_name(query=query,
                                       key=key,
                                       name=self.name)

        self.myid = int(_id)

        return self.myid

    # -------------------------------------
    def set_param(self, param=None, value=None, exclude=None, name=None):
        """ set a specific param value """
        if param is None or not isinstance(param, str):
            return

        if value is None:
            return

        if param not in self.params:
            return

        b_do_set = True

        # exclude
        if exclude is not None:
            if param in exclude:
                b_do_set = False

        if b_do_set:
            self.params[param] = value
            if param == name:
                self.name = value

        if self.in_sync:
            self.update()

    # -------------------------------------
    def set_additional_params(self, **kwargs):
        """set any kind of additionnal parameter, may need to filter entries"""
        self.additional_params = kwargs

    # -------------------------------------
    def clean_additional_params(self):
        """clean additionnal parameters on this object"""
        self.additional_params = {}

    # -------------------------------------
    def update(self):
        """ update template """

    # -------------------------------------
    def str_params(self, exclude=None):
        """ add params value to str"""

        return_val = " id={}".format(self.myid)

        sep = " "
        for key, value in self.params.items():
            if exclude is not None:
                if key in exclude:
                    continue

            if value == "":
                continue

            return_val += "{}{}={}".format(sep, key, value)
            sep = ", "

        return return_val
