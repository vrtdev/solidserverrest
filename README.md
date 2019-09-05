[![License](https://img.shields.io/badge/License-BSD%202--Clause-blue.svg)](https://opensource.org/licenses/BSD-2-Clause)

[![Python 3](https://pyup.io/repos/github/gregocgt/SOLIDserverRest/python-3-shield.svg)](https://pyup.io/repos/github/gregocgt/SOLIDserverRest/)
[![Updates](https://pyup.io/repos/github/gregocgt/SOLIDserverRest/shield.svg)](https://pyup.io/repos/github/gregocgt/SOLIDserverRest/)
[![pipeline status](https://gitlab.com/efficientip/solidserverrest/badges/master/pipeline.svg)](https://gitlab.com/efficientip/solidserverrest/commits/master)
[![coverage report](https://gitlab.com/efficientip/solidserverrest/badges/master/coverage.svg)](https://codecov.io/gl/efficientip/solidserverrest)
[![Documentation Status](https://readthedocs.org/projects/solidserverrest/badge/?version=latest)](https://solidserverrest.readthedocs.io/en/latest/?badge=latest)

# SOLIDserverRest

This 'SOLIDserverRest' allows to easily interact with [SOLIDserver](https://www.efficientip.com/products/solidserver/)'s REST API.
It allows managing all IPAM objects through CRUD operations.

* ***Free software***: BSD2 License

This 'SOLIDserverRest' is compatible with [SOLIDserver](https://www.efficientip.com/products/solidserver/) version 6.0.1P3 and higher.

# Install
Install 'SOLIDserverRest' using pip in your virtualenv:

```
	pip install SOLIDserverRest
```

# Usage
## Using the SOLIDserverRest object

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

More information about supported methods in the [specific document](docs/METHODS.md)

## Supported SOLIDserver modules in methods are:
* ip (IPAM - IP Address Management)
* app (Application and GSLB management) - starting with release 7.1 of SOLIDserver