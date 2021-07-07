from exception import *
from os import path
from storage_device import Storage_Device_Singleton
from devices import *


class Simulator:
    ''' the simulator class represents the structure in charge of simulating the network '''

    def __init__(self, signal_time=10, instruction_file="./script.txt", detection="hash-sum"):
        # load signal time
        self.signal_time = signal_time

        if instruction_file is None:
            raise NoneInstructionFileException()
        # load instructions from file
        self.instructions = self.load_instruction(instruction_file)
        # simulation time in ms
        self.simulation_time = 0
        # pending instruction to execute
        self.pending = []
        # sending device
        self.sending_device = set()
        # instructions to execution at current time
        self.time_instruction = []

        Storage_Device_Singleton.instance()

        self.detection_method = detection
        self.pending_ARPR = []

    # region Methods about execution simulation
    def clear_network_component(self):
        for d in Storage_Device_Singleton.instance().devices:
            d.clean()

    def send_switch(self):
        for i in Storage_Device_Singleton.instance().devices:
            if isinstance(i, Switch):
                if sum([1 if len(j) != 0 else 0 for j in i.port_information]) != 0:
                    i.send()

    def update_instructions(self):
        """ update all the instructions that must be executed at any given
        time in the network simulation and the pending instructions """
        self.time_instruction, length_new = self.get_all_instruction_at()
        self.instructions = self.instructions[length_new:] if length_new < len(self.instructions) else []
        self.pending = []

    def get_all_instruction_at(self):
        """ Returns all the instructions that have to be executed at the given moment by time """

        # instructions to return, not pending instructions, this list only contains instructions of new instructions
        rInstruction = []
        # select all instructions that must execute at this time
        for _instruction in self.instructions:
            if _instruction.time == self.simulation_time:
                rInstruction.append(_instruction)
            else:
                break
        # all the instructions are pending and new
        return [self.pending + rInstruction, len(rInstruction)]

    def execute_sending_device(self):
        """ execute data sends from all devices that are sending """
        temp_sending = self.sending_device.copy()
        for send_device in temp_sending:
            if not send_device.keep_sending():
                self.sending_device.remove(send_device)

    def execute_time_instructions(self):
        """ execute all the instructions that must be executed at this time """
        for _i in self.time_instruction:
            if not _i.execute():
                self.pending.append(_i)
                _i.time += 1

    def execute_pending_ARPR(self):
        for net_comp in Storage_Device_Singleton.instance().devices:
            if isinstance(net_comp, Host) and net_comp.pending_ARPR:
                self.pending_ARPR.append(net_comp)
            if isinstance(net_comp, Host) and net_comp.doing_ARPR:
                self.sending_device.add(net_comp)
                net_comp.doing_ARPR = False

        temp = []
        for i in self.pending_ARPR:
            if i.send(i.ARPR, True):
                self.sending_device.add(i)
                i.doing_ARPR = True
                i.pending_ARPR = False
                i.ARPR = str()
                temp.append(i)

        for t in temp:
            self.pending_ARPR.remove(t)

    def advance_simulation(self):
        """ advance simulation time in 1 ms"""
        self.simulation_time += 1

    def must_stop(self):
        """ simulation stops if there are no instructions left in
        the file if there are no pending instructions and no
        device is currently sending """
        send_port_switch = 0
        for i in Storage_Device_Singleton.instance().devices:
            if isinstance(i, Switch):
                send_port_switch += sum([1 if len(j) != 0 else 0 for j in i.port_information])
        return sum([len(i) for i in [self.sending_device, self.pending, self.instructions]]) + send_port_switch == 0

    def load_instruction(self, _path: str):
        """ This function receive a path of file with the
        instructions and parse the instruction. Return a list
        of Instructions """
        from instruction_factory_method import getInstruction

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

            _instructions.append(getInstruction(time, Itype, args))
        return _instructions

    def read_host_wire(self):
        for i in Storage_Device_Singleton.instance().devices:
            if isinstance(i, Host):
                i.read(True)

    # endregion Methods about execution simulation

    # region Methods for event to query prop of simulation
    def getCountDevices(self):
        """ get the number of devices at any given time on the network """
        return len(Storage_Device_Singleton.instance())

    def getSimulationTime(self):
        """ get current simulation time """
        return self.simulation_time

    def getSignalTime(self):
        """ get signal time of current simulation """
        return self.signal_time

    def getDevices(self, i):
        """ given an index get the device on the network """
        return Storage_Device_Singleton.instance().get_device(i)

    def getDevicesMap(self, name):
        ''' given the name of a device get its index on the network '''
        return Storage_Device_Singleton.instance().get_index(name)

    def add_sending(self, device):
        self.sending_device.add(device)
    # endregion Methods for event to query prop of simulation
