from abc import ABCMeta

class IP(metaclass=ABCMeta):
    def __init__(self):
        self._assoc_ip = []

    def assoc(self, ip):
        self._assoc_ip.append(ip)
    
    def desassoc(self, ip):
        self._assoc_ip.remove(ip)

    def get_human_repr(self, i = 0):
        _ip = self._assoc_ip[i]
        return f"{int(_ip[0:8],2)}.{int(_ip[8:16],2)}.{int(_ip[16:24],2)}.{int(_ip[24:],2)}"
