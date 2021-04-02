import abc
from exception import *
from devices import *
from event import *

#region Instruction
class Instruction(metaclass=abc.ABCMeta):
    ''' Abstract class that represent an instruction '''

    def __init__(self, time, args):
        self.time = time
        self.args = args

    @staticmethod
    def getAllFactory():
        ''' this function returns a dictionary where the key 
        is the name of the class inheriting from Instruction 
        and an instance of the factory of that class ''' 

        factories = {}
        # get dinamically subclasses of instruction factory
        for factory in InstructionFactory.__subclasses__():
            temp = factory()
            factories[temp.name] = temp
        return factories

    @staticmethod
    def getInstruction(time, IType, args):
        ''' Receive time, type of instructions and args of 
        instructions, and return an object of this instruction '''

        factory = Instruction.getAllFactory()
        return factory[IType].getInstance(time, args)

    @abc.abstractmethod
    def execute(self):
        ''' This function execute the instruction '''
        pass
    @abc.abstractmethod
    def __str__(self):
        pass
    @abc.abstractmethod
    def __repr__(self):
        pass

class Mac(Instruction):
    def __init__(self, time, args):
        super().__init__(time, args)
        self.host = args[0]
        self.mac = args[1]
        self.macEvent = EventHook()

    def execute(self):
        return self.macEvent.fire(self)

    def __str__(self):
        return f"{self.time} mac {list_to_str(self.args)}"

    def __repr__(self):
        return f"{self.time} mac {list_to_str(self.args)}"

class Create(Instruction):
    ''' Represent create instruction '''

    def __init__(self, time, args): 
        super().__init__(time, args)

        if len(args) < 2:
            raise CorruptInstructionException("Miss args to create")

        # hub is true if args[0] is hub
        self.hub = args[0] == 'hub'
        # name of device 
        self.name = args[1]
        # number of ports
        if self.hub:
            if len(args) < 3:
                raise CorruptInstructionException("Miss ports number to create hub")
            self.no_ports = int(args[2])
        else:
            self.no_ports = 1
        self.createEvent = EventHook()

    def execute(self):
        new_device = Hub(self.name, self.no_ports) if self.hub else Host(self.name)
        self.createEvent.fire(new_device)
        return True

    def __str__(self):
        return f"{self.time} create {list_to_str(self.args)}"
    
    def __repr__(self):
        return f"{self.time} create {list_to_str(self.args)}"

class Connect(Instruction):
    ''' Represent connect instruction '''
    def __init__(self, time, args):
        super().__init__(time, args)
        
        if not len(args) == 2:
            raise CorruptInstructionException("Miss args to connect")
        self.name_1=args[0]
        self.name_2=args[1]

        self.device_1,self.port_1 = self.name_1.split('_')
        self.device_2,self.port_2 = self.name_2.split('_')
        
        self.port_1, self.port_2 = int(self.port_1) - 1, int(self.port_2) - 1
        self.connectEvent = EventHook()

    def execute(self):
        self.connectEvent.fire(self)
        return True

    def __str__(self):
        return f"{self.time} connect {list_to_str(self.args)}"
    
    def __repr__(self):
        return f"{self.time} connect {list_to_str(self.args)}"

class Send(Instruction):
    ''' Represent send instruction '''
    def __init__(self, time, args):
        super().__init__(time, args)

        if not len(args) == 2:
            raise CorruptInstructionException("Miss args to send")
        self.host = args[0]
        self.data = args[1]
        self.sendEvent = EventHook()

    def execute(self):
        return self.sendEvent.fire(self)
        

    def __str__(self):
        return f"{self.time} send {list_to_str(self.args)}"
    
    def __repr__(self):
        return f"{self.time} send {list_to_str(self.args)}"

class Disconnect(Instruction):
    ''' Represent disconnect instruction '''
    def __init__(self, time,args):
        super().__init__(time, args)
        if not len(args) == 1:
            raise CorruptInstructionException("Miss args to disconnect")

        self.device_1, self.port_1 = args[0].split('_')
        self.port_1=int(self.port_1)-1
        self.disconnectEvent = EventHook()

    def execute(self):
        self.disconnectEvent.fire(self)
        return True

    def __str__(self):
        return f"{self.time} disconnect {list_to_str(self.args)}"
    
    def __repr__(self):
        return f"{self.time} disconnect {list_to_str(self.args)}"

class SendFrame(Instruction):
    ''' Represent send instruction data frame '''
    def __init__(self, time, args):
        super().__init__(time, args)
        if not len(args) == 1:
            raise CorruptInstructionException("Miss args to disconnect")

        self.mac_to = args[1]
        self.host = args[0]
        self.dataSend = args[2]
        self.sendframeEvent = EventHook()

    def execute(self):
        return self.sendframeEvent.fire(self)
    
    def __str__(self):
        return f"{self.time} send_frame {list_to_str(self.args)}"
    
    def __repr__(self):
        return f"{self.time} send_frame {list_to_str(self.args)}"
#endregion

#region Instructions Factory
class InstructionFactory(metaclass=abc.ABCMeta):
    ''' Represent a factory of instructions '''
    @abc.abstractmethod
    def getInstance(self, time, args):
        ''' Return an instance of Instruction '''
        pass

class CreateFactory(InstructionFactory):
    ''' Represent a factory of create '''
    def __init__(self):
        self.name = 'create'

    def getInstance(self, time, args):
        return Create(time, args)

class DisconnectFactory(InstructionFactory):
    ''' Represent a factory of disconnect '''
    def __init__(self):
        self.name = 'disconnect'

    def getInstance(self, time, args):
        return Disconnect(time, args)

class ConnectFactory(InstructionFactory):
    ''' Represent a factory of connect '''
    def __init__(self):
        self.name = 'connect'

    def getInstance(self, time, args):
        return Connect(time, args)

class SendFactory(InstructionFactory):
    ''' Represent a factory of send '''
    def __init__(self):
        self.name = 'send'

    def getInstance(self, time, args):
        return Send(time, args)

class MacFactory(InstructionFactory):
    def __init__(self):
        self.name = "mac"

    def getInstance(self, time, args):
        return Mac(time, args)
        
class SendFrameFactory(InstructionFactory):
    def __init__(self):
        self.name = "send_frame"
    
    def getInstance(self, time, args):
        return SendFrame(time, args)
#endregion 