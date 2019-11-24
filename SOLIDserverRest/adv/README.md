# Advanced python library for SOLIDserver

In addition to the standard library exposing API, the advanced section allows object manipulation for easier coding.

## connecting SOLIDserver

set the credentials and server variable or put these directly in the SDS call:
```
from SOLIDserverRest import *
from SOLIDserverRest import adv as sdsadv

sds = sdsadv.SDS(ip_address=SDS_HOST,
                 user=SDS_LOGIN,
                 pwd=SDS_PWD)

try:
   sds.connect(method="native")
except SDSError as e:
   logging.error(e)
   exit()
```

## Space

get an existing space
```
space = sdsadv.Space(sds=sds, name="Local")
space.refresh()
```

create a specific space
```
space_name = 'ex_'+str(uuid.uuid4())

space = sdsadv.Space(sds=sds, name=space_name)
space.create()

logging.info(space)
```

typical output:
```
[adv02_create_space.py:37] INFO: *space* name=ex_06b1e083-067d-4f64-bc23-eae06bbfb42a id=1681 parent=0
```

## Block
```
block = sdsadv.Network(sds=sds,
                       space=space,
                       name='ex-block-'+str(uuid.uuid4()))

block.set_address_prefix('172.16.0.0', 16)
block.set_is_block(True)
block.create()

logging.info(block)
```

typical output:
```
[adv03_create_nets.py:48] INFO: *network* name=ex-block-4955bc8c-e364-40c2-82ef-e69297a4f85e [block] [network] id=573 start_hostaddr=172.16.0.0, end_hostaddr=172.16.255.255, subnet_size=65536, subnet_level=0, parent_subnet_id=0, is_terminal=0, subnet_allocated_size=0, subnet_allocated_percent=0.0, subnet_used_size=0, subnet_used_percent=0.0, subnet_ip_used_size=0, subnet_ip_used_percent=0.0, subnet_ip_free_size=65534, is_in_orphan=0, lock_network_broadcast=1, tree_level=0
```

## Network in the block
```
net02 = sdsadv.Network(sds=sds,
                       space=space,
                       name='ex-net-'+str(uuid.uuid4()))

net02.set_address_prefix('172.16.10.0', 24)
net02.set_parent(block)
net02.set_is_terminal(False)
net02.create()

logging.info(net02)
```

typical output:
```
[adv03_create_nets.py:60] INFO: *network* name=ex-net-5e1d6d4f-eab6-4973-885c-7b9605cba219 [network] id=574 start_hostaddr=172.16.10.0, end_hostaddr=172.16.10.255, subnet_size=256, subnet_level=1, parent_subnet_id=573, is_terminal=0, subnet_allocated_size=0, subnet_allocated_percent=0.0, subnet_used_size=0, subnet_used_percent=0.0, subnet_ip_used_size=0, subnet_ip_used_percent=0.0, subnet_ip_free_size=254, is_in_orphan=0, lock_network_broadcast=1, tree_level=0
```

## Terminal subnetwork
```
net03 = sdsadv.Network(sds=sds,
                       space=space,
                       name='ex-term-'+str(uuid.uuid4()))

net03.set_address_prefix('172.16.10.128', 25)
net03.set_parent(net02)
net03.set_is_terminal(True)
net03.create()

logging.info(net03)
```

typical output:
```
[adv03_create_nets.py:72] INFO: *network* name=ex-term-e6fcaaaf-75a1-4921-8ca8-c92654ae47f4 [terminal] id=575 start_hostaddr=172.16.10.128, end_hostaddr=172.16.10.255, subnet_size=128, subnet_level=2, parent_subnet_id=574, is_terminal=1, subnet_allocated_size=0, subnet_allocated_percent=0.0, subnet_used_size=0, subnet_used_percent=0.0, subnet_ip_used_size=0, subnet_ip_used_percent=0.0, subnet_ip_free_size=126, is_in_orphan=0, lock_network_broadcast=1, tree_level=0
```

## IP Address
```
add = sdsadv.IpAddress(sds=sds,
                       space=space,
                       ipv4='172.16.10.135')
add.create()

logging.info(add)
```

typical output:
```
[adv04_create_ip.py:78] INFO: *ip address* 172.16.10.135 id=378 subnet_id=584, subnet_size=128, subnet_is_terminal=1, parent_subnet_start_hostaddr=172.16.10.0, parent_subnet_end_hostaddr=172.16.10.255, subnet_start_ip_addr=ac100a80, subnet_end_ip_addr=ac100aff
```
