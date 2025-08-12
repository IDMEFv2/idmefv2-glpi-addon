'''
IDMEFv2 message processors
'''

import abc
from typing import Any
import dns.resolver
import dns.reversename


class Processor(abc.ABC):
    def __init__(self, context: Any):
        self._context = context

    def process(self, message: dict) -> dict:
        if self.filter(message):
            return self.transform(message)
        return message

    @abc.abstractmethod
    def filter(self, message: dict) -> bool:
        '''
        Message filtering method, implemented in sub-classes

        Args:
            message (dict): the input IDMEFv2 message

        Returns:
            bool: True if message must be further processed, false if not

        Raises:
            NotImplementedError: must be implemented in concrete sub-classes
        '''
        raise NotImplementedError()

    def transform(self, message: dict) -> dict:
        '''
        Message modification method, redefined in sub-classes
        Base class implementation does nothing

        Args:
            message (dict): the input IDMEFv2 message

        Returns:
            dict: the message
        '''
        return message


class NullProcessor(Processor):
    def filter(self, message: dict) -> bool:
        return False


class BaseDNSProcessor(Processor):
    def __init__(self, context: Any, must_be_there: str, must_not_be_there: str):
        super().__init__(context)
        self._must_be_there = must_be_there
        self._must_not_be_there = must_not_be_there

    def filter(self, message: dict) -> bool:
        for a in ['Source', 'Target']:
            if isinstance(message.get(a), list):
                for h in message[a]:
                    if self._must_be_there in h and not self._must_not_be_there in h:
                        return True
        return False


class ReverseDNSProcessor(BaseDNSProcessor):
    def __init__(self, context : Any):
        super().__init__(context, 'IP', 'Hostname')

    def transform(self, message: dict) -> dict:
        for a in ['Source', 'Target']:
            for h in message[a]:
                if 'Hostname' in h or not 'IP' in h:
                    continue
                addr = dns.reversename.from_address(h['IP'])
                ptr = dns.resolver.resolve(addr, 'PTR')
                if ptr:
                    h['Hostname'] = str(ptr[0])
        return message


class DNSProcessor(BaseDNSProcessor):
    def __init__(self, context : Any):
        super().__init__(context, 'Hostname', 'IP')

    def transform(self, message: dict) -> dict:
        for a in ['Source', 'Target']:
            for h in message[a]:
                if 'IP' in h or not 'Hostname' in h:
                    continue
                a = dns.resolver.resolve(h['Hostname'])
                if a:
                    h['IP'] = str(a[0])
        return message
