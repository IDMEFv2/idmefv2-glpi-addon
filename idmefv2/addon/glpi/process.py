'''
IDMEFv2 message processors
'''
import abc
import jsonpath_ng as jsonpath

class IDMEFv2Processor(abc.ABC):
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

class NullProcessor(IDMEFv2Processor):
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
