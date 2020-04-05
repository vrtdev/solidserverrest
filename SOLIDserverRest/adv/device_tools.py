# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2020-04-05 18:30:58 alex>
#

"""
SOLIDserver device manager

"""

import ipaddress
import re

# import logging
import pprint
import time

from SOLIDserverRest.Exception import SDSError, SDSInitError
from SOLIDserverRest.Exception import SDSDeviceError, SDSDeviceNotFoundError
from SOLIDserverRest.Exception import SDSEmptyError

from .class_params import ClassParams
from . import Device
from . import DeviceInterface

# ------------------------------------------
def apply_filter_metadata(filter, dev_raw):
    """apply metadata value filter"""

    k = "tag_hostdev_{}".format(filter['name'])

    return dev_raw[k] == str(filter['val'])

# ------------------------------------------
def apply_filter_of_class(filter, dev_raw):
    """apply class parameter filter"""
    return dev_raw['hostdev_class_name'] == filter['val']

# ------------------------------------------
def apply_filter_in_subnet(filter, dev_raw):
    """apply ip address filter"""
    ipv4_re = r'(((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?))'
    result = True

    if not '_ipnet' in filter:
        ipnet = ipaddress.ip_network(filter['val'])
        filter['_ipnet'] = ipnet
    else:
        ipnet = filter['_ipnet']

    if not '_ipadd' in dev_raw:
        dev_raw['_ipadd'] = []
        ip_raw = re.findall(ipv4_re, dev_raw['hostdev_ip_formated'])
        for host_if_ip in ip_raw:
            if host_if_ip[0] not in dev_raw['_ipadd']:
                dev_raw['_ipadd'].append(host_if_ip[0])

    ip_raw = dev_raw['_ipadd']

    for host_if_ip in ip_raw:
        ipadd = ipaddress.ip_address(host_if_ip)

        if ipadd in ipnet:
            result = True
            break
        else:
            result = False

    return result


# ------------------------------------------
def apply_filter_space(filter, dev_raw):
    """apply space on ip address filter"""
    space_re = r'&([^,;]+)[,;]'

    spaces = re.findall(space_re, dev_raw['hostdev_ip_addr'])
    for space in spaces:
        if space == filter['val']:
            return True

    return False


# ------------------------------------------
def apply_list_filters(filters, dev_raw):
    """apply the list filters to the device and return True if all match"""
    result = True

    # print("check device {}".format(dev_raw['hostdev_name']))

    for filter in filters:
        if filter['type'] == "in_subnet":
            result = apply_filter_in_subnet(filter, dev_raw)
            if result == False:
                return False

        if filter['type'] == "of_class":
            result = apply_filter_of_class(filter, dev_raw)
            if result == False:  # pragma: no cover
                return False

        if filter['type'] == "metadata":
            result = apply_filter_metadata(filter, dev_raw)
            if result == False:  # pragma: no cover
                return False

        if filter['type'] == "space":
            result = apply_filter_space(filter, dev_raw)
            if result == False:
                return False

    return result


# ------------------------------------------
def list_devices_page(sds=None,
                      filters=[],
                      offset=0, page=25):
    """list devices from the space"""
    # print("list_devices_page", offset, page)
    
    if sds is None:
        raise SDSInitError("list device requires connection")
 
    params = {
        'limit': page,
        'offset': offset
    }

    # check if we have a of_class filter
    for filter in filters:
        if 'type' not in filter:
            raise SDSDeviceError(message="list filter without type")
        if filter['type'] == "of_class":
            _class_filter = "hostdev_class_name='{}'".format(filter['val'])
            if 'WHERE' in params:
                params['WHERE'] += " and " + _class_filter
            else:
                params['WHERE'] = _class_filter

        if filter['type'] == "metadata":
            _metadata_filter = "hostdev.{}".format(filter['name'])
            if 'TAGS' in params:
                params['TAGS'] += "&"+_metadata_filter
            else:
                params['TAGS'] = _metadata_filter

            _metadata_filter = "tag_hostdev_{}='{}'".format(filter['name'], str(filter['val']))
            if 'WHERE' in params:
                params['WHERE'] += " and " + _metadata_filter
            else:
                params['WHERE'] = _metadata_filter

    try:
        rjson = sds.query("host_device_list",
                          params=params)
    except SDSEmptyError:
        return None

    if 'errmsg' in rjson:  # pragma: no cover
        raise SDSError(message="device list, "
                       + rjson['errmsg'])

    adevs = []
    for dev in rjson:
        # check the filters

        # dev_detail = Device(sds, name=dev['hostdev_name'])
        # try:
        #     dev_detail.refresh()
        # except SDSDeviceError:
        #     continue
        # print(dev_detail)
        # exit()

        if apply_list_filters(filters, dev):
            r = {
                'name': dev['hostdev_name'],
            }
            if '_ipadd' in dev:
                r['extracted_ips'] = dev['_ipadd']
            else:
                r['hostdev_ip_formated'] = dev['hostdev_ip_formated']

            adevs.append(r)

        # ici - supprimer le refresh device et le reporter 
        # sur les tests le nécessitant


    return adevs


# ------------------------------------------
def list_devices(sds=None,
                 filters=[],
                 limit=10):
    """ limit: max number of device to return, 0 for all
        filters: returned device should match all filters
            {'type':'in_subnet', 'val': '10.149.0.0/16'},
            {'type':'of_class', 'val': 'AWS-EC2'},
            {'type':'metadata', 'name': 'cores', 'val': '1'},
            {'type':'space', 'val': 'ex-space-01'},
    """
    
    offset = 0
    collected = 0
    page = 500
    alldevs = []

    while limit == 0 or collected < limit:
        adevs = list_devices_page(sds, filters, 
                                  offset=offset, 
                                  page=page)

        if adevs is None:
            break

        collected += len(adevs)
        alldevs += adevs

        offset += page

    if limit and len(alldevs) > limit:
        alldevs = alldevs[:limit]

    return alldevs


# --------

        # dev_detail.fetch_interfaces()

        # for intf in dev_detail.aifs_simple:
        #     interface = DeviceInterface(sds,
        #                                 name=intf['if'],
        #                                 device=dev_detail)
        #     interface.myid = intf['id']
        #     interface.refresh()


            # for dev_if in device.ainterfaces:
            #     ipadd = ipaddress.ip_address(dev_if.ipv4)
            #     #print("check {} in {} {}".format(ipadd, ipnet, ipadd in ipnet))
            #     if ipadd in ipnet:
            #         result = True
            #         break
            #     else:
            #         result = False

