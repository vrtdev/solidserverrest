[![License](https://img.shields.io/badge/License-BSD%202--Clause-blue.svg)](https://opensource.org/licenses/BSD-2-Clause)

[![pipeline status](https://gitlab.com/efficientip/solidserverrest/badges/master/pipeline.svg)](https://gitlab.com/efficientip/solidserverrest/commits/master)
[![coverage report](https://gitlab.com/efficientip/solidserverrest/badges/master/coverage.svg)](https://codecov.io/gl/efficientip/solidserverrest)

# SOLIDserverRest

This 'SOLIDserverRest' allows to easily interact with [SOLIDserver](https://www.efficientip.com/products/solidserver/)'s REST API.
It allows managing all IPAM objects through CRUD operations.

* ***Free software***: BSD2 License

This 'SOLIDserverRest' is compatible with [SOLIDserver](https://www.efficientip.com/products/solidserver/) version 7 and ownward.

# Install
Install 'SOLIDserverRest' using pip in your virtualenv:

```
	pip install SOLIDserverRest
```

# Usage

## Using the SOLIDserverRest advanced object (recommended)

All commands and object manipulation are going through a SOLIDserver main object, handling the connection to the manager and pushing API calls. The creation of a SOLIDserver object is done like that:
```
from SOLIDserverRest import *
from SOLIDserverRest import adv as sdsadv

SDS_HOST = "192.168.254.254"
SDS_LOGIN = "foo"
SDS_PWD = "bar"

sds = sdsadv.SDS(ip_address=SDS_HOST,
                 user=SDS_LOGIN,
                 pwd=SDS_PWD)
try:
    sds.connect(method="native")
except SDSError as e:
    logging.error(e)
    exit(1)

print(adv)

```

More examples in the example directory.

## Using the SOLIDserverRest object

The raw API is mapped using the SOLIDserverRest object which handle the connection, prepare the formating and handle some errors. It can be usefull twhen the advanced library is not yet implementing an object that you require in your code.

### 1. Declare endpoint API point
Set the API endpoint you want to talk with through API. Could use an IP address
(v4 or v6) or a host name
* host = IP address of the SOLIDserver server
```
con = SOLIDserverRest("fqdn_host.org")
```

### 2. Specify connection method
You can use native connection mode using SOLIDserver default method which provide
authentication through headers in the requests with information
encoded in base64

* user = user who want to use
* password = password of the user

```python
	con.use_native_sds(user="apiuser", password="apipwd")
```

You can also use the basic authentication method for connecting the SOLIDserver.

* user = user who want to use
* password = password of the user

```python
	con.use_basicauth_sds(user="apiuser", password="apipwd")
```

### 3. Set TLS security
SSL certificate chain is validated by default, to disable it, use the set_ssl_verify method

```python
        con.set_ssl_verify(False)  # True by default
	rest_answer = con.query("method", "parameters")
```

Otherwise, you have to provide the certificate file:
```python
    con = SOLIDserverRest(SERVER)
```
If the certificate file is not valide, an exception ```SDSInitError``` is raised.

### 4. Request to SOLIDserver API

You need parameters:
* method = choose your method in the list below
* parameters = Python dictionary with parameters you want to use

```python
	rest_answer = con.query("method", "parameters")
```

### 5. Analyze answer

* rest_answer => object name
* rest_answer.status_code => current http answer code set in the object
* rest_answer.content => Answer core from SOLIDserver API set in the object

Example:
```python
	print(rest_answer)
	print(rest_answer.status_code)
	print(rest_answer.content)
```

# Methods that could be used
Methods are organized to match the ontology used in SOLIDServer, you will find:
* Sites - address spaces
* Subnets (v4 and v6)
* Pools (v4 and v6)
* Addresses (v4 and v6)
* Aliases (v4 and v6)
* DNS servers, views, zones, RR, acl, key
* application manager
* DHCP server, scope, shared net, range, static, group
* device manager
* VLAN manager

More information about supported methods in the [specific document](docs/METHODS.md)
