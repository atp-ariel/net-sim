class Frame:
    def __init__(self, str_frame):
        f_decoded = Frame.decode(str_frame)
        self.init = f_decoded["init"]
        self.mac_dest = f_decoded["mac_dest"]
        self.mac_origin = f_decoded["mac_origin"]
        self.size_data = f_decoded["size_data"]
        self.size_detection = f_decoded["size_detection"]
        self.data = f_decoded["data"]
        self.detection_code = f_decoded["detection_code"]
    
    def __str__(self):
        return "".join([self.init,self.mac_dest, self.mac_origin, self.size_data, self.size_detection, self.data, self.detection_code])
    
    def __repr__(self):
        return str(self)
        
    @classmethod
    def decode(cls,frame):
        init = frame[0]
        mac_dest = frame[1:17]
        mac_origin = frame[17:33]
        size_data = frame[33:41]
        size_detection = frame[41:49]
        data = frame[49:49+int(size_data,2)*8 ]
        detection_code = frame[49+int(size_data,2)*8 : ]
        return {"init":init, "mac_dest": mac_dest, "mac_origin": mac_origin, "size_data": size_data, "size_detection": size_detection, "data": data, "detection_code": detection_code}