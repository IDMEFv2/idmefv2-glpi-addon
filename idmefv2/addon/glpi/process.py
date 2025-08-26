"""
IDMEFv2 message processors
"""

import abc
from typing import Any
import dns.resolver
import dns.reversename


class Processor(abc.ABC):
    def __init__(self, context: Any):
        self._context = context

    @abc.abstractmethod
    def transform(self, message: dict) -> dict:
        """
        Message modification method, implemented in sub-classes

        Args:
            message (dict): the input IDMEFv2 message

        Returns:
            dict: the transformed message
        """
        raise NotImplementedError()


class NullProcessor(Processor):
    def transform(self, message: dict) -> dict:
        return message


class IPProcessor(Processor):
    def transform(self, message: dict) -> dict:
        for k in ["Source", "Target"]:
            for host in message.get(k, []):
                self.transformHost(message, host)
        return message

    @abc.abstractmethod
    def transformHost(self, message: dict, host: dict):
        raise NotImplementedError()


class ReverseDNSProcessor(IPProcessor):

    def transformHost(self, message: dict, host: dict):
        if "Hostname" in host or "IP" not in host:
            return
        addr = dns.reversename.from_address(host["IP"])
        ptr = dns.resolver.resolve(addr, "PTR")
        if ptr:
            host["Hostname"] = str(ptr[0])


class DNSProcessor(IPProcessor):

    def transformHost(self, message: dict, host: dict):
        if "IP" in host or "Hostname" not in host:
            return
        ip = dns.resolver.resolve(host["Hostname"])
        if ip:
            host["IP"] = str(ip[0])


class GLPIProcessor(IPProcessor):

    ADDRESS_ID = "101"
    LATITUDE_ID = "998"
    LONGITUDE_ID = "999"

    def transformHost(self, message: dict, host: dict):
        print(host)
        if "IP" not in host:
            return
        criteria = [
            {
                "field": "IPAddress.name",
                "searchtype": "contains",
                "value": "^" + host["IP"] + "$",
            }
        ]
        forcedisplay = ["Location.address", "Location.latitude", "Location.longitude"]
        r = self._context.search(
            "Computer", criteria=criteria, forcedisplay=forcedisplay
        )
        if len(r) < 1:
            return
        computer = r[0]
        if GLPIProcessor.ADDRESS_ID in computer:
            host["Location"] = computer[GLPIProcessor.ADDRESS_ID]
        if GLPIProcessor.LATITUDE_ID in computer and GLPIProcessor.LONGITUDE_ID in computer:
            geoloc = computer[GLPIProcessor.LATITUDE_ID] + "," + computer[GLPIProcessor.LONGITUDE_ID]
            host["GeoLocation"] = geoloc
