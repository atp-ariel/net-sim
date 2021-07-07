from abc import ABCMeta
from logger import Logger

class PayLoad(metaclass=ABCMeta):
    def __init__(self, name):
        self.payload_logger = Logger(name + "_payload.txt")