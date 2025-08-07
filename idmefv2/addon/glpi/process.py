'''
IDMEFv2 message processors
'''
import abc
from typing import Any
import jsonpath_ng as jsonpath

class Processor(abc.ABC):
    def __init__(self, context : Any):
        self._context = context

    @abc.abstractmethod
    def process(self, message : dict) -> dict:
        '''
        Message processing method, implemented in sub-classes

        Args:
            message (dict): the input IDMEFv2 message

        Returns:
            dict: the processed message

        Raises:
            NotImplementedError: must be implemented in concrete sub-classes
        '''
        raise NotImplementedError()

class NullProcessor(Processor):
    def process(self, message : dict) -> dict:
        '''
        Message processing method
        Does nothing

        Args:
            message (dict): the input IDMEFv2 message

        Returns:
            dict: the processed message
        '''
        return message

class JSONPathProcessor(Processor):
    def __init__(self, context: Any, path: str):
        super().__init__(context)
        self._jsonpath = jsonpath.parse(path)

    def process(self, message: dict) -> dict:
        if self._jsonpath.find(message):
            return self.transform(message)
        return message

    @abc.abstractmethod
    def transform(self, message: dict) -> dict:
        raise NotImplementedError()

class DNSProcessor(JSONPathProcessor):
    def __init__(self, context: Any):
        super().__init__(context, '$.Source[*].IP')

    def transform(self, message: dict) -> dict:
        message['foobar'] = 123
        return message
