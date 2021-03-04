# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2020-07-26 16:20:12 alex>
#

"""
SOLIDserver device manager

"""

# import ipaddress
# import logging
# import pprint

from SOLIDserverRest.Exception import SDSError, SDSEmptyError
from SOLIDserverRest.Exception import SDSDeviceError, SDSDeviceNotFoundError

from .class_params import ClassParams

__all__ = ["Device"]


class Device(ClassParams):
    """ class to manipulate the SOLIDserver device """

    # -------------------------------------
    def __init__(self,
                 sds=None,
                 name=None,
                 class_params=None):
        """init a device object:
        - sds: object SOLIDserver, could be set afterwards
        - name: name of the device
        """

        if name is None:
            raise SDSDeviceError("no name provided at device init")

        super(Device, self).__init__(sds, name)

        # params mapping the object in SDS
        self.clean_params()

        self.set_sds(sds)
        self.set_name(name)
        self.aifs_simple = []
        self.ainterfaces = []

        if class_params is not None:
            self.set_class_params(class_params)

    # -------------------------------------
    def clean_params(self):
        """ clean the object params """
        super(Device, self).clean_params()

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

        self.aifs_simple = []
        self.ainterfaces = []

    # -------------------------------------
    def set_param(self, param=None, value=None, exclude=None, name=None):
        super(Device, self).set_param(param,
                                      value,
                                      exclude=['hostdev_id'],
                                      name='hostdev_name')

    # -------------------------------------
    def create(self):
        """ create the device in SDS """

        if self.sds is None:
            raise SDSDeviceError(message="not connected")

        params = {
            'hostdev_name': self.name,
            **self.additional_params
        }

        if 'hostdev_class_name' in self.params:
            self.add_class_params({
                'hostdev_class_name': self.params['hostdev_class_name']
            })
            params['hostdev_class_name'] = self.params['hostdev_class_name']

        self.prepare_class_params('hostdev', params)

        rjson = self.sds.query("host_device_create",
                               params=params)

        if 'errmsg' in rjson:
            raise SDSDeviceError(message="dev creation error, "
                                 + rjson['errmsg'])

        self.params['hostdev_id'] = int(rjson[0]['ret_oid'])
        self.myid = int(self.params['hostdev_id'])

        self.refresh()

    # -------------------------------------
    def update(self):
        """ update the device in SDS """

        if self.sds is None:
            raise SDSDeviceError(message="not connected")

        params = {
            'hostdev_id': self._get_id(query="host_device_list",
                                       key="hostdev"),
            'hostdev_name': self.name,
            **self.additional_params
        }

        if 'hostdev_class_name' in self.params:
            self.add_class_params({
                'hostdev_class_name': self.params['hostdev_class_name']
            })
            params['hostdev_class_name'] = self.params['hostdev_class_name']

        self.prepare_class_params('hostdev', params)

        rjson = self.sds.query("host_device_update",
                               params=params)

        if 'errmsg' in rjson:  # pragma: no cover
            raise SDSDeviceError(message="device update error, "
                                 + rjson['errmsg'])

        self.refresh()

    # -------------------------------------
    def delete(self):
        """deletes the device in the SDS"""
        if self.sds is None:
            raise SDSDeviceError(message="not connected")

        if self.params['hostdev_id'] is None:
            raise SDSDeviceNotFoundError("on delete")

        params = {
            'hostdev_id': self.params['hostdev_id'],
            **self.additional_params
        }

        try:
            rjson = self.sds.query("host_device_delete",
                                   params=params)
        except SDSEmptyError:
            raise SDSDeviceNotFoundError(message="not found")

        if 'errmsg' in rjson:  # pragma: no cover
            raise SDSDeviceNotFoundError("on delete "+rjson['errmsg'])

        self.clean_params()

    # -------------------------------------
    def refresh(self):
        """refresh content of the device from the SDS"""

        if self.sds is None:
            raise SDSDeviceError(message="not connected")

        device_id = self._get_id(query="host_device_list",
                                 key="hostdev")

        params = {
            "hostdev_id": device_id,
            **self.additional_params
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
            self.update_class_params(rjson['hostdev_class_parameters'])

    # -------------------------------------
    def fetch_interfaces(self):
        """ fetch interfaces if any"""

        if self.sds is None:  # pragma: no cover
            raise SDSDeviceError(message="not connected")

        if self.myid == -1:  # pragma: no cover
            raise SDSDeviceError(message="device refresh needed")

        params = {
            **self.additional_params,
        }

        params['WHERE'] = "hostdev_id='{}'".format(self.myid)

        rjson = self.sds.query("host_iface_list",
                               params=params)

        if 'errmsg' in rjson:  # pragma: no cover
            raise SDSDeviceError(message="interface list error, "
                                 + rjson['errmsg'])

        self.aifs_simple = []
        for interface in rjson:
            self.aifs_simple.append({
                'if': interface['hostiface_name'],
                'id': int(interface['hostiface_id'])
            })

    # -------------------------------------
    def link_interface(self, interface):
        """link back an interface object to the device"""
        if interface not in self.ainterfaces:
            self.ainterfaces.append(interface)

    # -------------------------------------
    def __str__(self):  # pragma: no cover
        """return the string notation of the device object"""

        return_val = "*device* name={}".format(self.name)

        if ('hostdev_site_name' in self.params
                and self.params['hostdev_site_name'] != ''):
            return_val += " space={}".format(self.params['hostdev_site_name'])
            return_val += " [{}]".format(self.params['hostdev_site_id'])

        return_val += self.str_params(exclude=['hostdev_id',
                                               'hostdev_name'])

        if self.aifs_simple:
            return_val += " interfaces=["
            sep = ""
            for intf in self.aifs_simple:
                return_val += sep + intf['if']
            return_val += "]"

        return_val += str(super(Device, self).__str__())

        return return_val
