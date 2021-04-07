from exception import NoneInstructionFileException, NonExistentInstructionFileException
from instruction import *
from os import path
from random import randint
from collections import deque
from util import bin_hex, hex_bin, mult_x, INIT_FRAME_BIT

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
        device = self.devices[index_1]
        if device.ports[di.port_1]=='':
            print('Unconnected port. Ignored action')
        else:
            name_wire, port_wire = get_device_port(device.ports[di.port_1])
            port_wire = int(port_wire) - 1

            wire = self.devices[self.deviceMap[name_wire]]

            name_2, port_2 = get_device_port(wire.ports[1-port_wire])
            port_2 = int(port_2) - 1

            device.ports[di.port_1] = ""
            self.devices[self.deviceMap[name_2]].ports[port_2] = ""

    def add_device(self, new_device):
        ''' this method adds a new device to the network and subscribes 
        the simulator to all device events ''' 

        # add name to device map
        self.deviceMap[new_device.name] = len(self.devices)
        # add a new device
        self.devices.append(new_device)

        if isinstance(new_device, Device):
            # suscribe to events
            new_device.logger.askForSimulationTime += self.getSimulationTime
            new_device.askSignalTime += self.getSignalTime
            new_device.consultDevice += self.getDevices
            new_device.consultDeviceMap += self.getDevicesMap
            new_device.askCountDevice += self.getCountDevices
            if isinstance(new_device, Host):
                new_device.data_logger.askForSimulationTime += self.getSimulationTime
    
    def connect_device(self, ci):
        ''' connect network devices and check that it remains in a non-collision state '''
        ci.device_1, ci.device_2 = self.devices[self.deviceMap[ci.device_1]], self.devices[self.deviceMap[ci.device_2]]

        if ci.device_1.ports[ci.port_1]=='' and ci.device_2.ports[ci.port_2]=='':
            is_hub_d1, is_hub_d2 = isinstance(ci.device_1, Hub), isinstance(ci.device_2, Hub)
            more_than_2d_sending = lambda x: len(list(filter(lambda y: y != None, x.read_value))) >= 2
            hub_d_sending = lambda x: len(list(filter(lambda y: y != None, x.read_value))) == 1
            # si el dispositivo uno es un hub que tiene mas de un dispositivo enviando entonces uno debe callarse para evitar la colision
            if is_hub_d1 and more_than_2d_sending(ci.device_1):
                self.shut_up_a_host(ci.device_1)
            # si el dispositivo 2 es un hub que tiene mas de un dispositivo enviando enotnces uno debe callarse
            if is_hub_d2 and more_than_2d_sending(ci.device_2):
                self.shut_up_a_host(ci.device_2)
            # si ambos son hub con un dispositivo enviando, uno de ellos debe callarse
            if is_hub_d1 and is_hub_d2 and hub_d_sending(ci.device_1) and hub_d_sending( ci.device_2):
                self.shut_up_a_host(ci.device_1)
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
    
    def send_message(self, sendI):
        ''' Send data over the network '''
        send_device = self.devices[self.deviceMap[sendI.host]] 
        data = ""
        if isinstance(sendI, SendFrame):
            data = str(INIT_FRAME_BIT) + mult_x(hex_bin(sendI.mac_to),16) + mult_x(send_device.MAC,16) + mult_x(bin(len(sendI.dataSend))[2:],8) + "0"*8 + mult_x(hex_bin(sendI.dataSend), 8)
        else:
            data = sendI.data
        if send_device.send(data,isinstance(sendI, SendFrame)):
            self.sending_device.add(send_device)
            return True
        return False        
    
    def set_mac(self, mI):
        self.devices[self.deviceMap[mI.host]].set_MAC(mult_x(hex_bin(mI.mac), 16))
        return True
    #endregion Instructions methods

    #region Auxiliar methods
    def shut_up_a_host(self, hub: Hub):
        index_rv = list(filter(lambda x: x != -1,[i  if hub.read_value[i] != None else -1 for i in range(len(hub.ports))]))
        to_shut_up = self.find_root(hub.ports[randint(0, len(index_rv)-1)])
        if to_shut_up.sending_frame:
            self.pending.append(Instruction.getInstruction(self.simulation_time + 1, "send_frame", [to_shut_up.name, bin_hex(to_shut_up.data_to_send[0:16]), bin_hex(to_shut_up.data_to_send[48:])]))
            self.pending[-1].sendframeEvent += self.send_message
        else:
            self.pending.append(Instruction.getInstruction(self.simulation_time +1, "send", [to_shut_up.name, to_shut_up.data_to_send]))
            self.pending[-1].sendEvent += self.send_message        
        self.sending_device.remove(to_shut_up)
        to_shut_up.clean_sending()

    def find_root(self, port_name):
        device_name,port = get_device_port(port_name)
        port=int(port)-1
        component = self.devices[self.deviceMap[device_name]]
        while True:
            if isinstance(component,Host):
               return component
            elif isinstance(component,Wire):
                port_name=component.ports[1]  if port==0 else component.ports[0]
            else:
                port_name=component.internal_port_connection[port]
            device_name,port=get_device_port(port_name)
            port=int(port)-1
            component = self.devices[self.deviceMap[device_name]]
               
    def bfs(self, node_device):
        vis = [False for i in range(len(self.devices))]
        
        q = deque([node_device])
        
        while len(q) != 0:
            x = q.pop()
            vis[self.devices[self.deviceMap[x]]] = True

            if x in self.sending_device:
                self.pending.append(InstructionFactory.getInstance(self.simulation_time, "send_frame", [x.name, x.mac_to, x.data_to_send]))
                self.pending[-1].sendFrameEvent += self.send_message
                x.data_to_send = ""
                x.index_sending = 0
                x.time_sending = 0
                x.mac_to = ""
                break

            for item in map(lambda j: get_device_port(j)[0], filter(lambda i: i != "", x.ports)):
                if not vis[self.devices[self.deviceMap[item]]]:
                    q.append(self.devices[self.deviceMap[item]])
    
    #endregion Auxiliar methods

    #region Methods about execution simulation
    def clear_network_component(self):
        for d in self.devices:
            d.clean() 

    def send_switch(self):
        for i in self.devices:
            if isinstance(i, Switch):
                if sum([1 if len(j) != 0 else 0 for j in i.port_information]) != 0:
                    i.send()

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
                elif type(_instruction) is SendFrame:
                    _instruction.sendframeEvent += self.send_message
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
        send_port_switch = 0
        for i in self.devices:
            if isinstance(i, Switch):
                send_port_switch += sum([1 if len(j) != 0 else 0 for j in i.port_information])
        return sum([len(i) for i in [self.sending_device, self.pending, self.instructions]]) + send_port_switch == 0

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

    def read_host_wire(self):
        for i in self.devices:
            if isinstance(i, Host):
                i.read(True)
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