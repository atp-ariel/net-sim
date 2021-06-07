from abc import ABCMeta
from util import mult_x

class IP(metaclass=ABCMeta):
    def __init__(self):
        self._assoc_ip = []
        self._assoc_mask = []

    def assoc(self, ip, mask):
        self._assoc_ip.append(ip)
        self._assoc_mask.append(mask)
    
    def desassoc(self, ip):
        self._assoc_ip.remove(ip)

    def set_ip(self, ip, mask, interface):
        self.assoc(self.ip_bit(ip), self.ip_bit(mask))

    def get_human_repr(self, i = 0):
        _ip = self._assoc_ip[i]
        return self.bit_ip(_ip)
    
    def bit_ip(self, _ip):
        return f"{int(_ip[0:8],2)}.{int(_ip[8:16],2)}.{int(_ip[16:24],2)}.{int(_ip[24:],2)}"
    def ip_bit(self, hip):
        _bytes = hip.split(".")
        _binary = str()
        for _byte in _bytes:
            _binary += mult_x(bin(int(_byte))[2:],8)
        return _binary
