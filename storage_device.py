class Storage_Device:
    def __init__(self):
        self.devices = []
        self.deviceMap = {}

    def get_device_with(self, name):
        return self.get_device(self.get_index(name))
    
    def get_index(self, name):
        return self.deviceMap[name]
    
    def get_device(self, i):
        return self.devices[i]
    
    def add(self, device):
        self.deviceMap[device.name] = len(self)
        self.devices.append(device)

    def __len__(self):
        return len(self.devices)

class Storage_Device_Singleton:
    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = Storage_Device()
        return cls._instance