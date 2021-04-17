import abc
from exception import *
from event import *
from executor import Connector, Setter_Mac, Disconnector, Sender, SenderFrame, Creator

#region Instruction
class Instruction(metaclass=abc.ABCMeta):
    ''' Abstract class that represent an instruction '''

    def __init__(self, time, args):
        self.time = time
        self.args = args

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

    def execute(self):
        return Setter_Mac().execute(self)

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

        #device type
        self.type=args[0]
        # sender is true if args[0] is hub or switch
        self.sender = args[0] == 'hub' or args[0] == 'switch'
        # name of device
        self.name = args[1]
        # number of ports
        if self.sender:
            if len(args) < 3:
                raise CorruptInstructionException("Miss ports number to create resender")
            self.no_ports = int(args[2])
        else:
            self.no_ports = 1

    def execute(self):
        return Creator().execute(self)

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

    def execute(self):
        return Connector().execute(self)

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

    def execute(self):
        return Sender().execute(self)
        

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

    def execute(self):
        return Disconnector().execute(self)

    def __str__(self):
        return f"{self.time} disconnect {list_to_str(self.args)}"
    
    def __repr__(self):
        return f"{self.time} disconnect {list_to_str(self.args)}"

class SendFrame(Instruction):
    ''' Represent send instruction data frame '''
    def __init__(self, time, args):
        super().__init__(time, args)
        
        self.mac_to = args[1]
        self.host = args[0]
        self.dataSend = args[2]

    def execute(self):
        return SenderFrame().execute(self)
    
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