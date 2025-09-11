# idmefv2-glpi-addon

This repository provides a IDMEFv2 enrichment add-on using GLPI to add location and inventory information to a IDMEFv2 message. This add-on runs as a web server providing a REST API to enrich IDMEFv2 messages.

## Prerequisites

The following prerequisites must be installed on your system to install and use this library:

- Python 3.10 or later
- The Python [setuptools](https://pypi.org/project/setuptools/) package (usually available as a system package under the name `python3-setuptools`)

Python dependencies are:
- Flask
- dnspython
- glpi-api

## Installation

### Installation from local sources

It is highly recommended to install the library in a Python *virtualenv* https://virtualenv.pypa.io/en/latest/, unless running inside a container.

Installing the dependencies using `requirements.txt` is not supported; this repository provides a `pyproject.toml` which is the recommended alternative.

To install all modules, simply run in the root directory of the git clone:

``` sh
. /PATH/TO/YOUR/VIRTUALENV/bin/activate  # only if using a virtualenv
pip install --editable .
```

This will install as well the dependencies.

### Installation from packages

`idmefv2-glpi-addon` provides packages currently hosted on [TestPyPI](https://test.pypi.org/).

To install using TestPyPI, use the following command:

```
pip install --extra-index-url https://test.pypi.org/simple/ idmefv2-glpi-addon
```

### Installation from github

`idmefv2-glpi-addon` releases can be installed directly from github repository without first cloning the repository. To install the latest release, run the following command:

``` sh
pip install git+https://github.com/IDMEFv2/idmefv2-glpi-addon@latest
```

It is also possible to install a specific release:

``` sh
pip install git+https://github.com/IDMEFv2/idmefv2-glpi-addon@V0.0.2
```

## Testing

Python unit tests using [`pytest`](https://docs.pytest.org/en/stable/) are provided:

``` sh
$ pytest -vv
========================================================================= test session starts ==========================================================================
platform linux -- Python 3.12.3, pytest-8.4.1, pluggy-1.6.0 -- /home/francois/virtualenvs/idmefv2-glpi-addon/bin/python
cachedir: .pytest_cache
rootdir: /home/francois/projects/SAFE4SOC/work/idmefv2-glpi-addon
configfile: pyproject.toml
collected 3 items

idmefv2/addon/glpi/process_test.py::test_null PASSED                                                                                                             [ 33%]
idmefv2/addon/glpi/process_test.py::test_reverse_dns_1 PASSED                                                                                                    [ 66%]
idmefv2/addon/glpi/process_test.py::test_dns_1 PASSED                                                                                                            [100%]

========================================================================== 3 passed in 0.05s ===========================================================================
```

## Running

The Python package `idmefv2.addon.glpi` is directly runnable:

Usage:
``` sh
$ python -m idmefv2.addon.glpi -h
usage: glpi-addon [-h] -c CONF_FILE

Launch the IDMEFv2 GLPI addon

options:
  -h, --help            show this help message and exit
  -c CONF_FILE, --conf CONF_FILE
                        give configuration file
```

Running:
``` sh
$ python3 -m idmefv2.addon.glpi -c /etc/glpi-addon.conf
DEBUG:urllib3.connectionpool:Starting new HTTP connection (1): glpi:80
DEBUG:urllib3.connectionpool:http://glpi:80 "GET /apirest.php/initSession HTTP/1.1" 200 52
DEBUG:root:connected to GLPI (<glpi_api.GLPI object at 0x798d2c034680>)
 * Serving Flask app '__main__'
 * Debug mode: on
INFO:werkzeug:WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://172.18.0.2:5000
INFO:werkzeug:Press CTRL+C to quit
INFO:werkzeug: * Restarting with stat
DEBUG:urllib3.connectionpool:Starting new HTTP connection (1): glpi:80
DEBUG:urllib3.connectionpool:http://glpi:80 "GET /apirest.php/initSession HTTP/1.1" 200 52
DEBUG:root:connected to GLPI (<glpi_api.GLPI object at 0x7c5ab9035b50>)
WARNING:werkzeug: * Debugger is active!
INFO:werkzeug: * Debugger PIN: 869-947-691
DEBUG:root:received request <Request 'http://127.0.0.1:5000/glpi' [POST]> [b'{"Source":[{"IP":"192.168.1.11"}],"Target":[{"IP": "192.168.2.11"}]}']
DEBUG:root:processing {'Source': [{'IP': '192.168.1.11'}], 'Target': [{'IP': '192.168.2.11'}]} with <idmefv2.addon.glpi.process.GLPIProcessor object at 0x7c5ab9036e10>
DEBUG:urllib3.connectionpool:Resetting dropped connection: glpi
DEBUG:urllib3.connectionpool:http://glpi:80 "GET /apirest.php/listSearchOptions/Computer HTTP/1.1" 200 None
DEBUG:urllib3.connectionpool:http://glpi:80 "GET /apirest.php/search/Computer?forcedisplay%5B0%5D=2&forcedisplay%5B1%5D=101&forcedisplay%5B2%5D=998&forcedisplay%5B3%5D=999&criteria%5B0%5D%5Bfield%5D=126&criteria%5B0%5D%5Bsearchtype%5D=contains&criteria%5B0%5D%5Bvalue%5D=%5E192.168.1.11%24 HTTP/1.1" 200 197
DEBUG:urllib3.connectionpool:http://glpi:80 "GET /apirest.php/search/Computer?forcedisplay%5B0%5D=2&forcedisplay%5B1%5D=101&forcedisplay%5B2%5D=998&forcedisplay%5B3%5D=999&criteria%5B0%5D%5Bfield%5D=126&criteria%5B0%5D%5Bsearchtype%5D=contains&criteria%5B0%5D%5Bvalue%5D=%5E192.168.2.11%24 HTTP/1.1" 200 194
INFO:werkzeug:172.18.0.1 - - [11/Sep/2025 13:29:02] "POST /glpi HTTP/1.1" 200 -
```

Run in another terminal:
``` sh
$ curl -X POST -H "Content-Type: application/json" -d '{"Source":[{"IP":"192.168.1.11"}],"Target":[{"IP": "192.168.2.11"}]}' http://127.0.0.1:5000/glpi
{
  "Attachment": [
    {
      "ExternalURI": "http://glpi/front/computer.form.php?id=2",
      "Name": "glpi_computer_link_2"
    },
    {
      "ExternalURI": "http://glpi/front/computer.form.php?id=1",
      "Name": "glpi_computer_link_1"
    }
  ],
  "Source": [
    {
      "Attachment": [
        "glpi_computer_link_2"
      ],
      "GeoLocation": "48.01918065853973,-4.448277354240418",
      "IP": "192.168.1.11",
      "Location": "Le Gourbi"
    }
  ],
  "Target": [
    {
      "Attachment": [
        "glpi_computer_link_1"
      ],
      "GeoLocation": "43.967214059230514,5.576376914978028",
      "IP": "192.168.2.11",
      "Location": "Bordel"
    }
  ]
}
```

### REST API endpoints

The add-on accepts HTTP POST requests with a `Content-Type` set to `application/json`, the content being the IDMEFv2 message. It provides the following endpoints:

- `/null`: returns the message without modification
- `/dns`: process the `Source` and `Target` elements of the message:
  - if element has a `Hostname` and no `IP` fields: queries the DNS to get the IP corresponding to the hostname
  - if element has a `IP` and no `Hostname` fields: queries the reverse DNS to get the hostname corresponding to the IP
- `/glpi`: process the `Source` and `Target` elements of the message:
  - if element has a `IP` field, queries GLPI to search a computer having this IP and retrieves the `Location` associated to this computer in GLPI
  - if location exists, add the geolocation to the element and add an attachment specifying the link to the computer in GLPI web interface

# Contributions

All contributions must be licensed under the BSD 3-Clause License. See the LICENSE file inside this repository for more information.

To improve coordination between the various contributors, we kindly ask that new contributors subscribe to the [IDMEFv2 mailing list](https://www.freelists.org/list/idmefv2) as a way to introduce themselves.
