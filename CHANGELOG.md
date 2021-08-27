# 2.3.0
  * add update to DNS record object (for ttl and values)
  * update packages version for security

# 2.2.2
  * fix: dns zone not restricted to its dns server (in smart)

# 2.2.1
  * add mapper for guardian params

# 2.2.0
  * add DNS zone object
  * add DNS record object

# 2.1.10
  * fix 16: add hostname as class param on IP
  * add check on space type in IP and network creation

# 2.1.9
  * class params str() sort the metadata
  * fix network search to limit to same hierarchy
  * suppress some mapping for dhcp shared network (duplicates)

# 2.1.8
  * fix API call with release of SDS < 7
  * add network find new capacities and example

# 2.1.7
  * fix network name issue

# 2.1.6
  * fix 14: can connect using name with adv lib
  * refactor get space id
  * fix 9: doc review + generator

# 2.1.5
  * fix get version in advanced module
  * added vlan in mapping (thx to Bruno LABOUR)
  * upgrade libs
  * higher timeout by default in tdd testing
