from sortedcontainers import SortedSet
from util import mult_x

class Route:
    def __init__(self, destination="0.0.0.0", mask="0.0.0.0", gateway="0.0.0.0", interface=0):
        self.__destination = "".join([mult_x(str(bin(int(i)))[2:], 8) for i in destination.split(".")])
        self.__mask = "".join([mult_x(str(bin(int(i)))[2:], 8) for i in mask.split(".")])
        self.__gateway = "".join([mult_x(str(bin(int(i)))[2:], 8) for i in gateway.split(".")])
        self.__interface = interface

    @property
    def destination(self) -> str:
        return self.__destination

    @property
    def mask(self) -> str:
        return self.__mask

    @property
    def gateway(self) -> str:
        return self.__gateway

    @property
    def interface(self) -> int:
        return self.__interface

    @property
    def priority(self) -> int:
        return str().join([mult_x(str(bin(int(i)))[2:], 8) for i in self.mask.split(".")]).count("0")

    def __eq__(self, other):
        if not isinstance(other, Route):
            return False
        return self.destination == other.destination and self.mask == other.mask and self.gateway == other.gateway and self.interface == other.interface

    def __hash__(self):
        return hash(".".join([self.destination, self.mask, self.gateway, str(self.interface)]))

    def __str__(self):
        return f"{self.priority} {self.destination} {self.mask} {self.gateway} {self.interface}"

    def __repr__(self):
        return f"{self.priority} {self.destination} {self.mask} {self.gateway} {self.interface}"

class RouterTable:
    def __init__(self):
        self.__routes = SortedSet(key=lambda x: x.priority)

    # O(log n)
    def add(self, route: Route):
        self.__routes.add(route)

    # O(n)
    def clean(self):
        self.__routes.clear()

    # O(n)
    def _get(self, route: Route):
        for item in self.__routes:
            if item == route:
                return item

    # O(n)
    def delete(self, route: Route):
        _route = self._get(route)
        if _route is not None:
            self.__routes.remove(_route)

    def enroute(self, ip: str) -> Route:
        for route in self:
            if route.destination == RouterTable._and_(ip, route.mask):
                return route
        return None

    def __iter__(self):
        return self.__routes.__iter__()

    def __str__(self):
        return self.__routes.__str__()

    def __repr__(self):
        return self.__routes.__str__()

    @staticmethod
    def _and_(ip1: str, ip2: str) -> str:
        and_result = str()
        for index in range(len(ip1)):
            and_result += str(int(ip1[index]) & int(ip2[index]))
        return and_result
