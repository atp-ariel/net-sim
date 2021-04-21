from strategy_detection import IStrategy_Detection

class Hash_Detection(IStrategy_Detection):
    def do(self, frame):
        f_decoded = self.decode(frame)
        list_int = map(lambda x: int(x, 2), self.split_2bytes(f_decoded["data"]))
        return int(f_decoded["detection"], 2) == sum(list_int)
    
    def chunk(self, s, n):
        for start in range(0, len(s), n):
            yield s[start:start+n]
    
    def self.split_2bytes(self, data):
        return list(chunk(data, 16))
