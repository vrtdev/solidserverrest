#!/usr/bin/python
# -*-coding:Utf-8 -*
#
# connects to a SOLIDserver
#
##########################################################


import pprint
import logging
import random

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from SOLIDserverRest import *
from SOLIDserverRest import adv as sdsadv

logging.basicConfig(format='[%(filename)s:%(lineno)d] %(levelname)s: %(message)s',
                    level=logging.INFO)

# configuration - to be adapted
SDS_HOST_IP = "192.168.24.253"
SDS_LOGIN = "ipmadmin"
SDS_PWD = "admin"
SPACE = "Local"

SPACE = "t0"


def create_nets(data, sds, space, net=None):
    for _net in data:
        logging.info('{} {}/{}'.format(_net['name'], _net['address'], _net['prefix']))

        _netobject = sdsadv.Network(sds=sds,
                                    space=space,
                                    name=_net['name'])
        _netobject.set_async()
        # _netobject.set_additional_params(start_hostaddr=_net['address'])
        _netobject.set_address_prefix(_net['address'], _net['prefix'])

        if net is not None:
            _netobject.set_param('parent_subnet_id', net.myid)

        _bneedcreate = False
        try:
            _netobject.refresh()
        except SDSNetworkError:
            _bneedcreate = True

        if _bneedcreate:
            _netobject.set_address_prefix(_net['address'], _net['prefix'])
            _netobject.set_is_block(_net['type'] == 'block')

            if net is not None:
                _netobject.set_parent(net)

            if 'terminal' in _net:
                _netobject.set_is_terminal(_net['terminal'] == 1)

            if 'meta' in _net:
                for _m in _net['meta']:
                    _netobject.add_class_params({_m['key']: _m['val']})

            # logging.info(_netobject)
            _netobject.create()
            logging.info(" created")

        if 'data' in _net:
            create_nets(_net['data'], sds, space, _netobject)


def init(sds, space):
    """init the space data if needed"""
    data = [{
        'type': "block", 'address': "10.0.0.0", 'prefix': 8, 'name': "top",
        'data': [
            {
                'type': "subnet", 'terminal': 0, 'address': "10.0.16.0", 'prefix': 20, 'name': "a2",
                'data':  [{
                    'type': "subnet", 'terminal': 1, 'address': "10.0.16.32", 'prefix': 28, 'name': "b2",
                }]
            },
            {
                'type':  "subnet", 'terminal':  0, 'address':  "10.0.32.0", 'prefix':  20, 'name':  "cloud-apps",
                'meta':  [{'key': "block_type", 'val': "apps"}],
                'data':  [
                    {
                        'type':  "subnet", 'terminal':  0, 'address':  "10.0.32.0", 'prefix':  22, 'name':  "web",
                        'meta': [{'key': "block_type", 'val': "apps-web"}]
                    },
                    {
                        'type':  "subnet", 'terminal':  0, 'address':  "10.0.36.0", 'prefix':  22, 'name':  "mobile",
                        'meta': [{'key':  "block_type", 'val':  "apps-mob"}]
                    }
                ]
            },
            {
                'type':  "subnet", 'terminal':  0, 'address':  "10.0.48.0", 'prefix':  20, 'name':  "cloud-infra",
                'meta':  [{'key': "block_type", 'val': "infra"}],
            },
            {
                'type':  "subnet", 'terminal':  0, 'address':  "10.0.64.0", 'prefix':  20, 'name':  "cloud-middleware",
                'meta':  [{'key': "block_type", 'val': "middleware"}],
            },
            {
                'type':  "subnet", 'terminal':  0, 'address':  "10.0.80.0", 'prefix':  20, 'name':  "cloud-backend",
                'meta':  [{'key': "block_type", 'val': "backend"}],
            },
            {
                'type':  "subnet", 'terminal':  0, 'address':  "10.0.96.0", 'prefix':  20, 'name':  "cloud-db",
                'meta':  [{'key': "block_type", 'val': "db"}],
                'data':  [
                    {
                        'type':  "subnet", 'terminal':  0, 'address':  "10.0.98.0", 'prefix':  24, 'name':  "mobile",
                        'meta': [{'key': "block_type", 'val': "db"}]
                    }
                ]
            }
        ]
    }]

    create_nets(data, sds, space)


logging.info("create a connection to the SOLIDserver using IP")

sds = sdsadv.SDS(ip_address=SDS_HOST_IP,
                 user=SDS_LOGIN,
                 pwd=SDS_PWD)

try:
    sds.connect()
except SDSError as e:
    logging.error(e)
    exit()

logging.info(sds)

logging.info("get the space named {}".format(SPACE))
space = sdsadv.Space(sds=sds, name=SPACE)
space.refresh()

init(sds, space)

logging.info("get the block named top")

net01 = sdsadv.Network(sds=sds,
                       space=space,
                       name="top")
net01.refresh()

logging.info(net01)

# get possible networks with /24 in the block
possible_net = net01.find_free(24)
logging.info(possible_net)

# get subnet list with specific class param
net01.set_additional_params(TAGS="network.block_type",
                            WHERE="tag_network_block_type like 'db'")
apps_subnets = net01.get_subnet_list(depth=0)
net01.clean_additional_params()
logging.info(apps_subnets)

# get free subnet in found networks
for _avail_net in apps_subnets:
    _net_app = sdsadv.Network(sds=sds,
                              space=space,
                              name=_avail_net['subnet_name'])

    # search by name is not enough, add subnet IP
    _net_app.set_additional_params(start_hostaddr=_avail_net['start_hostaddr'])
    _net_app.clean_additional_params()
    _net_app.refresh()

    possible_net = _net_app.find_free(24)
    if len(possible_net) > 0:
        logging.info(possible_net)
        random.shuffle(possible_net)
        proposed_net = possible_net[0]

        logging.info("selected free subnet = {}".format(proposed_net))
        break


del sds
