from exception import NoneInstructionFileException, NonExistentInstructionFileException
from instruction import *
from os import path
from collections import deque

class Simulator:
    ''' the simulator class represents the structure in charge of simulating the network '''
    def __init__(self, signal_time=10, instruction_file="./script.txt"):
        # load signal time
        self.signal_time = signal_time
        if instruction_file == None:
            raise NoneInstructionFileException()
        # load instructions from file
        self.instructions = self.load_instruction(instruction_file)
        # simulation time in ms
        self.simulation_time = 0
        # list of device on the networks
        self.devices = []
        # dictionary of name device to index in devices list
        self.deviceMap = {}
        # pending instruction to execute
        self.pending = []
        # sending device
        self.sending_device = set()
        # instructions to execution at current time
        self.time_instruction = []
    
    #region Instructions methods
    def disconnect_device(self, di):
        ''' disconnect devices from the network '''
        index_1=self.deviceMap[di.device_1]
        if self.devices[index_1].ports[di.port_1]=='':
            print('Unconnected port. Ignored action')
        else:
            name_cable,port_cable=self.devices[index_1].ports[di.port_1].split('_')
            cable=self.deviceMap[name_cable]
            index_2,port_2=get_device_port(self.deviceMap[cable.ports[0]])
            if index_1==index_2:
                index_2,port_2=get_device_port(self.deviceMap[cable.ports[1]])
            port_2=int(port_2)-1
            self.devices[index_1].ports[di.port_1]=''
            self.devices[index_2].ports[port_2]=''

    def add_device(self, new_device):
        ''' this method adds a new device to the network and subscribes 
        the simulator to all device events ''' 

        # add name to device map
        self.deviceMap[new_device.name] = len(self.devices)
        # add a new device
        self.devices.append(new_device)

        if new_device is Device:
            # suscribe to events
            new_device.logger.askForSimulationTime += self.getSimulationTime
            new_device.askSignalTime += self.getSignalTime
            new_device.consultDevice += self.getDevices
            new_device.consultDeviceMap += self.getDevicesMap
            new_device.askCountDevice += self.getCountDevices
   
    def connect_device(self, ci):
        ''' connect network devices and check that it remains in a non-collision state '''
        ci.device_1, ci.device_2 = self.devices[self.deviceMap[ci.device_1]], self.devices[self.deviceMap[ci.device_2]]

        if ci.device_1.ports[ci.port_1]=='' and ci.device_2.ports[ci.port_2]=='':
            

            wire=Wire('wire'+str(len(self.devices)),ci.name_1,ci.name_2)
            self.deviceMap[wire.name]=len(self.deviceMap)
            self.devices.append(wire)
            ci.device_1.ports[ci.port_1]=wire.name +'_'+str(1)
            ci.device_2.ports[ci.port_2]=wire.name +'_'+str(2)
            ci.device_1.cable_send[ci.port_1]=True
            ci.device_2.cable_send[ci.port_2]=False
        else:
            print('Busy port. Ignored action')
        #     rvd1, rvd2 = ci.device_1.read_value, ci.device_2.read_value
        #     if  rvd1 == None:
        #         ci.device_1.read_value =  rvd2
        #         rvd1 = rvd2
        #         if rvd2 != None:
        #             ci.device_1.receive_port = ci.name_1
        #     elif rvd2 == None:
        #         ci.device_2.read_value =  rvd1
        #         rvd2 = rvd1
        #         if rvd1 != None:
        #             ci.device_2.receive_port = ci.name_2 
        #     elif rvd1 != None and rvd2 != None:
        #         send_roots = [self.find_root(ci.device_1.receive_port) if type(ci.device_1) != Host else ci.device_1, self.find_root(ci.device_2.receive_port) if type(ci.device_2) != Host else ci.device_2]
        #         decision = randint(0,1)
                
        #         devl = [ci.device_1, ci.device_2]
        #         portl = [ci.name_1, ci.name_2]
        #         nonD = abs(decision - 1)
        #         devl[nonD].receive_port = portl[nonD]
        #         self.sending_device.remove(send_roots[nonD])
        #         self.pending.append(Instruction.getInstruction(self.simulation_time, "send", [send_roots[nonD].name, send_roots[nonD].data_to_send]))
        #         self.pending[-1].sendEvent += self.sendMessage
        #         send_roots[nonD].data_to_send = ""
        #         send_roots[nonD].index_sending = 0
        #         send_roots[nonD].time_sending = 0

        #         del decision, nonD, send_roots
        # else:
        #     print('Busy port. Ignored action')
    
    def send_frame_message(self):
        pass
    
    def send_message(self, sendI):
        ''' Send data over the network '''
        send_device = self.devices[self.deviceMap[sendI.host]] 
        if send_device.send(sendI.data):
            self.sending_device.add(send_device)
            return True
        return False        
    
    def set_mac(self, mI):
        self.devices[self.deviceMap[mI.host]].set_MAC(bin(int(mI.mac, 16))[2:])     
        return True
    #endregion Instructions methods

    #region Auxiliar methods
    def find_root(self, port):
        device_name = get_device_port(port)[0]
        device = self.devices[self.deviceMap[device_name]]
        while True:
            if device.receive_port == None:
                return device
            device_name = get_device_port(device.ports[int(get_device_port(device.receive_port)[1])-1])[0]
            device = self.devices[self.deviceMap[device_name]]
    
    def bfs(self, node_device):
        vis = [False for i in range(len(self.devices))]
        
        q = deque([node_device])
        
        while len(q) != 0:
            x = q.pop()
            vis[self.devices[self.deviceMap[x]]] = True

            if x in self.sending_device:
                self.pending.append(InstructionFactory.getInstance(self.simulation_time, "send_frame", [x.name, x.mac_to, x.data_to_send]))
                self.pending[-1].sendFrameEvent += self.send_frame_message
                x.data_to_send = ""
                x.index_sending = 0
                x.time_sending = 0
                x.mac_to = ""
                break

            for item in map(lambda j: get_device_port(j)[0], filter(lambda i: i != "", x.ports)):
                if not vis[self.devices[self.deviceMap[item]]]:
                    q.append(self.devices[self.deviceMap[item]])
    
    def check_hub_condition(self, hub):
        return len(list(filter(lambda x: x != None, hub.read_value))) >= 2
    #endregion Auxiliar methods

    #region Methods about execution simulation
    def clear_network_component(self):
        for d in self.devices:
            d.clean() 

    def update_instructions(self):
        ''' update all the instructions that must be executed at any given 
        time in the network simulation and the pending instructions '''
        self.time_instruction, length_new = self.get_all_instruction_at()
        self.instructions = self.instructions[length_new:] if length_new < len(self.instructions) else []
        self.pending = []
    
    def get_all_instruction_at(self):
        ''' Returns all the instructions that have to be executed at the given moment by time '''

        # instructions to return, not pending instructions, this list only contains instructions of new instructions
        rInstruction = []
        # select all instructions that must execute at this time
        for _instruction in self.instructions:
            if _instruction.time == self.simulation_time:
                rInstruction.append(_instruction)
                if type(_instruction) is Create:
                    _instruction.createEvent += self.add_device
                elif type(_instruction) is Connect:
                    _instruction.connectEvent += self.connect_device
                elif type(_instruction) is Disconnect:
                    _instruction.disconnectEvent += self.disconnect_device
                elif type(_instruction) is Send:
                    _instruction.sendEvent += self.send_message
                elif type(_instruction) is Mac:
                    _instruction.macEvent += self.set_mac
            else: 
                break
        # all the instructions are pending and new
        return [self.pending + rInstruction, len(rInstruction)]
    
    def execute_sending_device(self):
        ''' execute data sends from all devices that are sending '''
        temp_sending = self.sending_device.copy()      
        for send_device in temp_sending:
            if not send_device.keep_sending():
                self.sending_device.remove(send_device)
    
    def execute_time_instructions(self):
        ''' execute all the instructions that must be executed at this time '''
        for _i in self.time_instruction:
            if not _i.execute():
                self.pending.append(_i)
                _i.time += 1

    def advance_simulation(self):
        ''' advance simulation time in 1 ms'''
        self.simulation_time += 1

    def must_stop(self):

        ''' simulation stops if there are no instructions left in 
        the file if there are no pending instructions and no 
        device is currently sending '''
        return sum([len(i) for i in [self.sending_device, self.pending, self.instructions]]) == 0

    def load_instruction(self, _path: str):
        ''' This function receive a path of file with the
        instructions and parse the instruction. Return a list 
        of Instructions '''
        
        if not path.isfile(_path):
            raise NonExistentInstructionFileException()
        # open file
        fd = open(_path)
        # read from file
        _content = fd.readlines()
        # close file
        fd.close()
        # list to return list
        _instructions = []

        # parse all the instructions
        for item in _content:
            # tokenize instruction
            sInstruction = item.split()
            
            # empty instruction then continue for 
            if len(sInstruction) == 0:
                continue
            
            # valid length of instruction
            if len(sInstruction) < 3:
                raise CorruptInstructionException()

            # get values
            time = int(sInstruction[0])
            Itype = sInstruction[1]
            args = sInstruction[2:]

            _instructions.append(Instruction.getInstruction(time, Itype, args))
        return _instructions

    #endregion Methods about execution simulation
    
    #region Methods for event to query prop of simulation
    def getCountDevices(self):
        ''' get the number of devices at any given time on the network '''
        return len(self.devices)

    def getSimulationTime(self):
        ''' get current simulation time '''
        return self.simulation_time

    def getSignalTime(self):
        ''' get signal time of current simulation '''
        return self.signal_time

    def getDevices(self, i):
        ''' given an index get the device on the network '''
        return self.devices[i]
    
    def getDevicesMap(self, name):
        ''' given the name of a device get its index on the network '''
        return self.deviceMap[name]
    #endregion Methods for event to query prop of simulation