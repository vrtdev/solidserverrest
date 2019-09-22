#
# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2019-09-22 15:31:16 alex>
#

"""
SOLIDserver device manager

"""

import logging

from SOLIDserverRest.Exception import SDSInitError, SDSError
from SOLIDserverRest.Exception import SDSDeviceError, SDSDeviceNotFoundError

from .class_params import ClassParams


class Device(ClassParams):
    """ class to manipulate the SOLIDserver device """

    # -------------------------------------
    def __init__(self, sds=None, name=None):
        """init a device object:
        - sds: object SOLIDserver, could be set afterwards
        - name: name of the device
        """

        if name is None:
            raise SDSDeviceError("no name provided at device init")

        self.name = name
        self.sds = sds

        # params mapping the object in SDS
        self.params = {}
        self.class_params = {}

        self.clean_params()

        super(Device, self).__init__()

    # -------------------------------------
    def clean_params(self):
        """ clean the object params """
        self.params = {
            'hostdev_id': None,
            'hostdev_name': None,
            'hostdev_class_name': None,
            'iplnetdev_id': None,
            'row_enabled': None,
            'iplnetdev_name': None,
            'hostdev_ip_addr': None,
            'hostdev_ip_formated': None,
            'hostdev_site_id': None,
            'hostdev_site_name': '',
            'port_total': None,
            'port_used': None,
            'port_used_percent': None,
            'port_free': None,
            'iface_total': None,
            'iface_used': None,
            'iface_used_percent': None,
            'iface_free': None
        }

    # -------------------------------------
    def create(self):
        """ create the device in SDS """

        if self.sds is None:
            raise SDSInitError(message="not connected")

        params = {
            'hostdev_name': self.name
        }

        rjson = self.sds.query("host_device_create",
                               params=params)

        if 'errmsg' in rjson:
            raise SDSDeviceError(message="dev creation error, "
                                 + rjson['errmsg'])

        self.params['hostdev_id'] = int(rjson[0]['ret_oid'])
        self.refresh()

    # -------------------------------------
    def delete(self):
        """deletes the device in the SDS"""
        if self.sds is None:
            raise SDSDeviceError(message="not connected")

        if self.params['hostdev_id'] is None:
            raise SDSDeviceNotFoundError("on delete")

        params = {
            'hostdev_id': self.params['hostdev_id']
        }

        self.sds.query("host_device_delete",
                       params=params)

        self.clean_params()

    # -------------------------------------
    def _get_id_by_name(self, name):
        """get the device ID from its name, return None if non existant"""

        params = {
            "WHERE": "hostdev_name='{}'".format(name),
        }

        try:
            rjson = self.sds.query("host_device_list",
                                   params=params)
        except SDSError as err_descr:
            msg = "cannot found device by name {}".format(name)
            msg += " / "+str(err_descr)
            raise SDSDeviceError(msg)

        if rjson[0]['errno'] != '0':  # pragma: no cover
            raise SDSDeviceError("errno raised on get id by name")

        return rjson[0]['hostdev_id']

    # -------------------------------------
    def refresh(self):
        """refresh content of the device from the SDS"""

        if self.sds is None:
            raise SDSDeviceError(message="not connected")

        if self.params['hostdev_id'] is None:
            device_id = self._get_id_by_name(self.name)
        else:
            device_id = self.params['hostdev_id']

        params = {
            "hostdev_id": device_id,
        }

        try:
            rjson = self.sds.query("host_device_info",
                                   params=params)
        except SDSError as err_descr:
            msg = "cannot get device info on id={}".format(device_id)
            msg += " / "+str(err_descr)
            raise SDSDeviceError(msg)

        rjson = rjson[0]

        for label in ['hostdev_id',
                      'hostdev_name',
                      'hostdev_class_name',
                      'iplnetdev_id',
                      'row_enabled',
                      'iplnetdev_name',
                      'hostdev_ip_addr',
                      'hostdev_ip_formated',
                      'hostdev_site_id',
                      'hostdev_site_name',
                      'port_total',
                      'port_used',
                      'port_used_percent',
                      'port_free',
                      'iface_total',
                      'iface_used',
                      'iface_used_percent',
                      'iface_free']:
            if label not in rjson:  # pragma: no cover
                msg = "parameter {} not found in device".format(label)
                raise SDSDeviceError(msg)
            self.params[label] = rjson[label]

        if 'hostdev_class_parameters' in rjson:
            if rjson['hostdev_class_parameters'] != "":
                self.decode_class_params(self.class_params,
                                         rjson['hostdev_class_parameters'])
                logging.info(rjson['hostdev_class_parameters'])
                # logging.info(self.params)

    # -------------------------------------
    def __str__(self):  # pragma: no cover
        """return the string notation of the device object"""
        return_val = "*device* name={}".format(self.name)

        if self.params['hostdev_id'] is not None:
            return_val += " id={}".format(self.params['hostdev_id'])

        if self.params['hostdev_site_name'] != '':
            return_val += " site={}".format(self.params['hostdev_site_name'])
            return_val += " [{}]".format(self.params['hostdev_site_id'])

        return return_val
