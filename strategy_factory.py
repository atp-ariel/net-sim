from abc import ABCMeta, abstractmethod
from hash_strategy import Hash_Detection
from parity_strategy import Parity_Detection
from crc_strategy import CRC16_Detection

def get_factory():
    _factory = {}
    for subclass_strategy in StrategyFactory.__subclasses__():
        _s = subclass_strategy()
        _factory[_s.name] = _s
    return _factory
    
class StrategyFactory(metaclass=ABCMeta):
    @abstractmethod
    def get_instance(self):
        pass

class HashFactory(StrategyFactory):
    def __init__(self):
        self.name = "hash-sum"

    def get_instance(self):
        return Hash_Detection()

class ParityFactory(StrategyFactory):
    def __init__(self):
        self.name = "parity"
    
    def get_instance(self):
        return Parity_Detection()

class CRC16Factory(StrategyFactory):
    def __init__(self):
        self.name = "crc16"
    
    def get_instance(self):
        return CRC16_Detection()