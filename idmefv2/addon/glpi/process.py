"""
IDMEFv2 message processors
"""

import abc
import urllib.parse
import dns.resolver
import dns.reversename
import dns.exception


class Processor(abc.ABC):
    @abc.abstractmethod
    def process(self, message: dict) -> dict:
        """
        Message processing method, implemented in sub-classes

        Args:
            message (dict): the input IDMEFv2 message

        Returns:
            dict: the processed message
        """
        raise NotImplementedError()


class NullProcessor(Processor):
    def process(self, message: dict) -> dict:
        return message


class DNSProcessor(Processor):

    def process(self, message: dict) -> dict:
        for k in ["Source", "Target"]:
            for host in message.get(k, []):
                try:
                    if "Hostname" in host and "IP" not in host:
                        answer = dns.resolver.resolve(host["Hostname"])
                        if answer:
                            host["IP"] = str(answer[0])
                    if "IP" in host and "Hostname" not in host:
                        addr = dns.reversename.from_address(host["IP"])
                        ptr = dns.resolver.resolve(addr, "PTR")
                        if ptr:
                            host["Hostname"] = str(ptr[0])
                except dns.exception.DNSException:
                    continue
        return message


class GLPIProcessor(Processor):

    ID = "2"
    ADDRESS = "101"
    LATITUDE = "998"
    LONGITUDE = "999"

    def __init__(self, glpi):
        self._glpi = glpi

    def _add_glpi_attachment(self, message: dict, computer_id: int) -> str:
        if "Attachment" not in message:
            message["Attachment"] = []
        name = "glpi_computer_link_" + str(computer_id)
        r = urllib.parse.urlparse(self._glpi.url)
        url = (
            r.scheme
            + "://"
            + r.netloc
            + "/front/computer.form.php?id="
            + str(computer_id)
        )
        a = {
            "Name": name,
            "ExternalURI": url,
        }
        message["Attachment"].append(a)
        return name

    def _process_host(self, message: dict, host: dict):
        criteria = [
            {
                "field": "IPAddress.name",
                "searchtype": "contains",
                "value": "^" + host["IP"] + "$",
            }
        ]
        forcedisplay = [
            "id",
            "Location.address",
            "Location.latitude",
            "Location.longitude",
        ]
        r = self._glpi.search("Computer", criteria=criteria, forcedisplay=forcedisplay)
        if len(r) < 1:
            return
        computer = r[0]
        if GLPIProcessor.ADDRESS in computer:
            host["Location"] = computer[GLPIProcessor.ADDRESS]
        if GLPIProcessor.LATITUDE in computer and GLPIProcessor.LONGITUDE in computer:
            geoloc = (
                computer[GLPIProcessor.LATITUDE]
                + ","
                + computer[GLPIProcessor.LONGITUDE]
            )
            host["GeoLocation"] = geoloc
        if "Attachment" not in host:
            host["Attachment"] = []
        attachment_name = self._add_glpi_attachment(message, computer[GLPIProcessor.ID])
        host["Attachment"].append(attachment_name)

    def process(self, message: dict) -> dict:
        for k in ["Source", "Target"]:
            for host in message.get(k, []):
                if "IP" in host:
                    self._process_host(message, host)
        return message
