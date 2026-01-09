# pylint: disable=missing-function-docstring,missing-class-docstring
"""
Main for GLPI add-on utilities
"""
import argparse
from configparser import ConfigParser
import logging
import sys
import glpi_api

LOCATION_1 = {
    "name":"Le Gourbi",
    "address":"Le Gourbi",
    "latitude":"48.01918065853973",
    "longitude":"-4.448277354240418"
}
LOCATION_2 = {
    "name": "Bordel",
    "address":"Bordel",
    "latitude": "43.967214059230514",
    "longitude":"5.576376914978028"
}
COMPUTER_1 = {
    "name": "computer_1",
    "IPAddress.name": "192.168.1.11"
}
COMPUTER_2 = {
    "name": "computer_2",
    "IPAddress.name": "192.168.2.11"
}
# see https://github.com/glpi-project/glpi/issues/15587
NETWORKPORT_1 = {
  "name": "management",
  "items_id": "XXX",
  "logical_number": 0,
  "itemtype": "Computer",
  "instantiation_type": "NetworkPortEthernet",
  "NetworkName_name": "mgmt",
  "NetworkName_fqdns_id": 0,
  "_create_children": True,
  "NetworkName__ipaddresses": {
    "-1": "XXX",
    "_xmlrpc_fckng_fix": ""
  }
}
NETWORKPORT_TEMPLATE = {
  "name": "eth0",
  "items_id": -1,
  "logical_number": 0,
  "itemtype": "Computer",
  "instantiation_type": "NetworkPortEthernet",
  "NetworkName_name": "eth0",
  "NetworkName_fqdns_id": 0,
  "_create_children": True,
  "NetworkName__ipaddresses": {
    "-1": "X.X.X.X",
    "_xmlrpc_fckng_fix": ""
  }
}
class Util:
    def __init__(self, config: ConfigParser):
        url = config.get("glpi", "url")
        apptoken = config.get("glpi", "apptoken")
        auth = config.get("glpi", "auth")
        self._glpi = None
        try:
            self._glpi = glpi_api.GLPI(url=url, apptoken=apptoken, auth=auth)
        except glpi_api.GLPIError as e:
            logging.error("cannot connect to GLPI: %s", str(e))
            sys.exit(1)
        logging.debug("connected to GLPI (%s)", str(self._glpi))

    def search_item(self, item_type: str, field: str, value: str) -> (int|None):
        criteria = [
            {
                "field": field,
                "searchtype": "contains",
                "value": "^" + value + "$",
            }
        ]
        r = self._glpi.search(item_type, criteria=criteria)
        logging.debug("search returned %s", str(r))
        if len(r) >= 1:
            return r[0]['2']
        return None

    def create_item(self, item_type: str, item: dict) -> int:
        r = self._glpi.add(item_type, item)
        logging.debug("add returned %s", str(r))
        return r[0]['id']

    def create_item_if_not_exist(self, item_type: str, item: dict) -> int:
        s = self.search_item(item_type, "name", item["name"])
        if s is not None:
            return s
        return self.create_item(item_type, item)

    def update_item(self, item_type: str, item_id: int, fields: dict):
        fields["id"] = item_id
        return self._glpi.update(item_type, fields)

def _main():
    parser = argparse.ArgumentParser(description="GLPI addon utilities", prog="glpi-addon-util")
    parser.add_argument("-c", help="give configuration file", dest="conf_file", required=True)
    options = parser.parse_args()

    config = ConfigParser()
    config.read(options.conf_file)

    logging.basicConfig(level=config.get("logging", "level", fallback="INFO"))

    u = Util(config)

    #print(glpi.list_search_options('Location'))

    c1 = u.create_item_if_not_exist("Computer", COMPUTER_1)

    l1 = u.create_item_if_not_exist("Location", LOCATION_1)

    u.update_item("Computer", c1, {"locations_id": l1})

    r = u.search_item("Computer", "IPAddress.name", COMPUTER_1["IPAddress.name"])
    if r is None:
        NETWORKPORT_TEMPLATE["items_id"] = c1
        NETWORKPORT_TEMPLATE["NetworkName__ipaddresses"]["-1"] = COMPUTER_1["IPAddress.name"]
        u.create_item("NetworkPort", NETWORKPORT_TEMPLATE)

if __name__ == "__main__":
    _main()
