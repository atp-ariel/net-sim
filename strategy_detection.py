from abc import ABCMeta, abstractmethod

class IStrategy_Detection(metaclass=ABCMeta):
    @abstractmethod
    def do(self, frame):
        pass
    
    def decode(self,frame):
        init = frame[0]
        mac_dest = frame[1:16]
        mac_origin = frame[]
        size_data = frame[]
        size_detection = frame[]
        data = frame[]
        detection = frame[]
        return {"init":init, "mac_dest": mac_dest, "mac_origin": mac_origin, "size_data": size_data, "size_detection": size_detection, "data": data, "detection": detection}