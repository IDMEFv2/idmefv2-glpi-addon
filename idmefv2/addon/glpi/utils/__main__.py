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
IPADDRESS_1 = {
    "name": "192.168.2.11"
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

    def create_item(self, item_type: str, item: dict) -> int:
        r = self._glpi.add(item_type, item)
        return r[0]['id']

    def create_item_if_not_exist(self, item_type: str, item: dict) -> int:
        criteria = [
            {
                "field": "name",
                "searchtype": "contains",
                "value": "^" + item["name"] + "$",
            }
        ]
        r = self._glpi.search(item_type, criteria=criteria)
        if len(r) >= 1:
            return r[0]['2']
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

    l1 = u.create_item_if_not_exist("Location", LOCATION_1)
    print(f"location id {l1}")

    c1 = u.create_item_if_not_exist("Computer", COMPUTER_1)
    print(f"computer id {c1}")

    u.update_item("Computer", c1, {"locations_id": l1})

    # link_1 = {
    #     "itemtype": "Computer",
    #     "items_id": 1,
    #     "locations_id": 1
    # }
    # r = u.create_item("Item_Location", link_1)
    # print(f'link id {r}')

if __name__ == "__main__":
    _main()
