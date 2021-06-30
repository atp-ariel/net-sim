from strategy_detection import IStrategy_Detection
from frame import Frame
from util import mult_x

class Hash_Detection(IStrategy_Detection):
    def check(self, frame):
        f = Frame(frame)
        return f.detection_code == self.apply(f.data)[1]
    
    def apply(self, data):
        """Apply a hash sum over data
        
        By example, if data is 01110111011101110111011101110111 then 476 is the hash sum,
        and detection code is 0000000111011100, with length 16 on bit and 2 on bytes.

        The result list must be ["00000010", "0000000111011100"]

        Args:
            data (str): Data to send on a frame

        Returns:
            [list]: In the first item contain a length of detection code, and in the second item contain the detection code
        """
        list_int = list(map(lambda x: int(x, 2), Hash_Detection.split_bytes(data)))
        _s = mult_x(bin(sum(list_int))[2:], 8)
        return [mult_x(bin(len(_s)//8)[2:], 8), _s]

    @staticmethod
    def chunk(s, n):
        for start in range(0, len(s), n):
            yield s[start:start+n]

    @staticmethod
    def split_bytes(data):
        return list(Hash_Detection.chunk(data, 8))
