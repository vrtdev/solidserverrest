# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2019-08-13 17:58:13 alex>
#

"""example file used in the blog: https://www.efficientip.com/python-library/
    get a subnet from the Local space and print informations
    get a free address
    create an entry

pip install pyopenssl
pip install requests

"""

import sys
import json
import logging
import math
import ipaddress
import uuid

import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pprint

from SOLIDserverRest import SOLIDserverRest

logging.basicConfig(format='%(asctime)-15s [%(levelname)s] %(filename)s:%(lineno)d - %(message)s',
                    level=logging.INFO)

SDS_CON = SOLIDserverRest('192.168.56.254')
SDS_CON.set_ssl_verify(False)
SDS_CON.use_basicauth_sds(user='api', password='apipwd')


def get_space(name):
    """get a space by its name from the SDS"""
    parameters = {
        "WHERE": "site_name='{}'".format(name),
        "limit": "1"
    }

    rest_answer = SDS_CON.query("ip_site_list", parameters)

    if rest_answer.status_code != 200:
        logging.error("cannot find space %s", name)
        return None

    rjson = json.loads(rest_answer.content)

    return {
        'type': 'space',
        'name': name,
        'is_default': rjson[0]['site_is_default'],
        'id': rjson[0]['site_id']
    }


def get_subnet_v4(name, space_id=None):
    """get a subnet by its name from the SDS"""
    parameters = {
        "WHERE": "subnet_name='{}' and is_terminal='1'".format(name),
        "TAGS": "network.gateway"
    }

    if space_id is not None:
        parameters['WHERE'] = parameters['WHERE'] + " and site_id='{}'".format(int(space_id))

    rest_answer = SDS_CON.query("ip_subnet_list", parameters)

    if rest_answer.status_code != 200:
        logging.error("cannot find subnet %s", name)
        return None

    rjson = json.loads(rest_answer.content)
    # pprint.pprint(rjson)
    return {
        'type': 'terminal_subnet',
        'name': name,
        'addr': rjson[0]['start_hostaddr'],
        'cidr': 32-int(math.log(int(rjson[0]['subnet_size']), 2)),
        'gw': rjson[0]['tag_network_gateway'],
        'used_addresses': rjson[0]['subnet_ip_used_size'],
        'free_addresses': rjson[0]['subnet_ip_free_size'],
        'space': rjson[0]['site_id'],
        'id': rjson[0]['subnet_id']
    }


def get_next_free_address(subnet_id, number=1, start_address=None):
    """get a set of free address, by default one is returned"""

    parameters = {
        "subnet_id": str(subnet_id),
        "max_find": str(number),
        "begin_addr": "192.168.16.100",
    }

    if start_address is not None:
        parameters['begin_addr'] = str(ipaddress.IPv4Address(start_address))

    rest_answer = SDS_CON.query("ip_address_find_free", parameters)

    if rest_answer.status_code != 200:
        logging.error("cannot find subnet %s", name)
        return None

    rjson = json.loads(rest_answer.content)

    result = {
        'type': 'free_ip_address',
        'available': len(rjson),
        'address': []
    }

    for address in rjson:
        result['address'].append(address['hostaddr'])

    return result


def add_ip_address(ip, name, space_id):
    """add an IP address and its name in the IPAM"""

    parameters = {
        "site_id": str(space_id),
        "hostaddr": str(ipaddress.IPv4Address(ip)),
        "name": str(name)
    }

    rest_answer = SDS_CON.query("ip_address_create", parameters)

    if rest_answer.status_code != 201:
        logging.error("cannot add IP node %s", name)
        return None

    rjson = json.loads(rest_answer.content)

    return {
        'type': 'add_ipv4_address',
        'name': str(name),
        'id': rjson[0]['ret_oid'],
    }


space = get_space("Local")
# print(space)

subnet = get_subnet_v4("home", space_id=space['id'])
# print(subnet)

ipstart = ipaddress.IPv4Address(subnet['addr'])+100
free_address = get_next_free_address(subnet['id'], 5, ipstart)
pprint.pprint(free_address)

node = add_ip_address(free_address['address'][2],
                      uuid.uuid4(),
                      space['id'])
print(node)

del(SDS_CON)
