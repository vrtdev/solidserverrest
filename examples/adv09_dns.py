#!/usr/bin/python
# -*-coding:Utf-8 -*
#
# connects to a SOLIDserver, create dns server, zone and records
#
##########################################################

import logging
import pprint
import os, sys
import uuid

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

from SOLIDserverRest import *
from SOLIDserverRest import adv as sdsadv

logging.basicConfig(format='[%(filename)s:%(lineno)d] %(levelname)s: %(message)s',
                    level=logging.INFO)

# configuration - to be adapted
SDS_HOST = "192.168.24.230"
SDS_LOGIN = "ipmadmin"
SDS_PWD = "admin"

logging.info("create a connection to the SOLIDserver")

sds = sdsadv.SDS(ip_address=SDS_HOST,
                 user=SDS_LOGIN,
                 pwd=SDS_PWD)

try:
    sds.connect(method="native")
except SDSError as e:
    logging.error(e)
    exit()

logging.info(sds)

# --------------------------
logging.info("create DNS SMARTArchitecture server")
dns = sdsadv.DNS(name="test-{}.labo".format(str(uuid.uuid4())[0:8]),
                 sds=sds)
dns.set_type('vdns', 'single')
dns.create()

logging.info(dns)

# --------------------------
logging.info("create DNS zone")
dns_zone = sdsadv.DNS_zone(sds=sds,
                           name="test-{}.labo".format(str(uuid.uuid4())[0:8]))

dns_zone.set_dns(dns)
dns_zone.set_type(dns_zone.TYPE_MASTER)
dns_zone.create()

logging.info(dns_zone)

# --------------------------
logging.info("create DNS record")
name = "{}.{}".format(str(uuid.uuid4())[0:8],
                          dns_zone.name)
dns_rr = sdsadv.DNS_record(sds, name)
dns_rr.set_zone(dns_zone)
dns_rr.set_type('A', ip='127.1.2.3')
dns_rr.create()

logging.info(dns_rr)
dns_rr.delete()

dns_rr = sdsadv.DNS_record(sds, name)
dns_rr.set_zone(dns_zone)
dns_rr.set_type('TXT', txt='test')
dns_rr.create()

logging.info(dns_rr)
dns_rr.delete()

dns_rr = sdsadv.DNS_record(sds, name)
dns_rr.set_zone(dns_zone)
dns_rr.set_type('MX', priority=10, target="foo.bar")
dns_rr.create()

logging.info(dns_rr)
dns_rr.delete()

# --------------------------
logging.info("cleaning")
dns_zone.delete()
dns.delete()

del sds
