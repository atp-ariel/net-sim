from strategy_detection import IStrategy_Detection
from frame import Frame
from util import mult_x

class Parity_Detection(IStrategy_Detection):
    def check(self, frame):
        f = Frame(frame)
        return f.detection_code[-1] == self.apply(f.data)[1][-1]
    
    def apply(self, data):
        count_one = data.count('1')
        parity = "0"*7 + '1' if count_one %2 != 0 else "0"*8
        return ["0"*7 + '1', parity]
