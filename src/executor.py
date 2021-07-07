from abc import ABCMeta, abstractmethod
from shut_up import ShutUp
from simulator_singleton import Simulator_Singleton
from storage_device import Storage_Device_Singleton
from util import mult_x, hex_bin, INIT_FRAME_BIT, get_device_port, OFF_SET
from devices import *
from strategy_factory import get_factory
from router_table import RouterTable, Route

class Executor(metaclass=ABCMeta):
    @abstractmethod
    def execute(self, instruction):
        pass

class Connector(Executor):
    def execute(self, instruction):
        ''' connect network devices and check that it remains in a non-collision state '''
        instruction.device_1, instruction.device_2 = Storage_Device_Singleton.instance().get_device_with(instruction.device_1), Storage_Device_Singleton.instance().get_device_with(instruction.device_2)
        if instruction.device_1.ports[instruction.port_1]=='' and instruction.device_2.ports[instruction.port_2]=='':
            is_hub_d1, is_hub_d2 = isinstance(instruction.device_1, Hub), isinstance(instruction.device_2, Hub)
            more_than_2d_sending = lambda x: len(list(filter(lambda y: y != None, x.read_value))) >= 2
            hub_d_sending = lambda x: len(list(filter(lambda y: y != None, x.read_value))) == 1
            
            # si el dispositivo uno es un hub que tiene mas de un dispositivo enviando entonces uno debe callarse
            # para evitar la colision
            if is_hub_d1 and more_than_2d_sending(instruction.device_1):
                ShutUp(Simulator_Singleton.instance()).shut_up_a_host(instruction.device_1)
            # si el dispositivo 2 es un hub que tiene mas de un dispositivo enviando enotnces uno debe callarse
            if is_hub_d2 and more_than_2d_sending(instruction.device_2):
                ShutUp(Simulator_Singleton.instance()).shut_up_a_host(instruction.device_2)
            # si ambos son hub con un dispositivo enviando, uno de ellos debe callarse
            if is_hub_d1 and is_hub_d2 and hub_d_sending(instruction.device_1) and hub_d_sending( instruction.device_2):
                ShutUp(Simulator_Singleton.instance()).shut_up_a_host(instruction.device_1)
            
            wire=Wire('wire'+str(len(Storage_Device_Singleton.instance())),instruction.name_1,instruction.name_2)
            Storage_Device_Singleton.instance().add(wire)
            instruction.device_1.ports[instruction.port_1]=wire.name +'_'+str(1)
            instruction.device_2.ports[instruction.port_2]=wire.name +'_'+str(2)
            instruction.device_1.cable_send[instruction.port_1]=True
            instruction.device_2.cable_send[instruction.port_2]=False
        else:
            print('Busy port. Ignored action')
        return True

class Setter_Mac(Executor):
    def execute(self, instruction):
        Storage_Device_Singleton.instance().get_device_with(instruction.host).set_MAC(mult_x(hex_bin(instruction.mac), 16), instruction.interface)
        return True

class Disconnector(Executor):
    def execute(self, instruction):
        index_1=Storage_Device_Singleton.instance().get_index(instruction.device_1)
        device = Storage_Device_Singleton.instance().get_device_with(instruction.device_1)
        if device.ports[instruction.port_1]=='':
            print('Unconnected port. Ignored action')
        else:
            name_wire, port_wire = get_device_port(device.ports[instruction.port_1])
            port_wire = int(port_wire) - 1

            wire =  Storage_Device_Singleton.instance().get_device_with(name_wire)

            name_2, port_2 = get_device_port(wire.ports[1-port_wire])
            port_2 = int(port_2) - 1

            device.ports[instruction.port_1] = ""
            device_2 = Storage_Device_Singleton.instance().get_device_with(name_2)
            device_2.ports[port_2] = ""

            if isinstance(device, Switch):
                device.clean_port(port_wire)
            if isinstance(device_2, Switch):
                device_2.clean_port(port_2)
        return True

class Sender(Executor):
    def execute(self, instruction):
        ''' Send data over the network '''
        send_device = Storage_Device_Singleton.instance().get_device_with(instruction.host)
        data = instruction.data
        
        if send_device.send(data,False):
            Simulator_Singleton.instance().sending_device.add(send_device)
            return True
        return False        

class SenderFrame(Executor):
    def execute(self, instruction):
        send_device = Storage_Device_Singleton.instance().get_device_with(instruction.host)

        data = INIT_FRAME_BIT 
        data += mult_x(hex_bin(instruction.mac_to), 16)
        data += mult_x(send_device.MAC, 16)
        data += mult_x(bin(len(mult_x(hex_bin(instruction.dataSend),8))//8)[2:],8)
        
        det = send_device.detection.apply(mult_x(hex_bin(instruction.dataSend), 8))
        data += det[0]
        data += mult_x(hex_bin(instruction.dataSend), 8)
        data += det[1]
        
        if send_device.send(data, True):
            Simulator_Singleton.instance().sending_device.add(send_device)
            return True
        return False  

class Creator(Executor):
    def execute(self, instruction):
        new_device = None
        _type = instruction.type.lower()

        if _type == "hub":
            new_device = Hub(instruction.name, instruction.no_ports)
        elif _type == "switch":
            new_device = Switch(instruction.name, instruction.no_ports)
        elif _type == "router":
            new_device = Router(instruction.name, instruction.no_ports)
        elif _type == "host":
            new_device = Host(instruction.name)

        Storage_Device_Singleton.instance().add(new_device)

        if isinstance(new_device, Device):
            # suscribe to events
            new_device.logger.askForSimulationTime += Simulator_Singleton.instance().getSimulationTime
            new_device.askSignalTime += Simulator_Singleton.instance().getSignalTime
            new_device.consultDevice += Simulator_Singleton.instance().getDevices
            new_device.consultDeviceMap += Simulator_Singleton.instance().getDevicesMap
            new_device.askCountDevice += Simulator_Singleton.instance().getCountDevices
            if isinstance(new_device, Host):
                new_device.data_logger.askForSimulationTime += Simulator_Singleton.instance().getSimulationTime   
                new_device.payload_logger.askForSimulationTime += Simulator_Singleton.instance().getSimulationTime  
                new_device.detection = get_factory()[Simulator_Singleton.instance().detection_method].get_instance()
            elif isinstance(new_device, Switch):
                new_device.refresh_time()
            elif isinstance(new_device, Router):
                new_device.detection = get_factory()[Simulator_Singleton.instance().detection_method].get_instance()
                new_device.sendEvent += Simulator_Singleton.instance().add_sending
        return True

class SenderPacket(Executor):
    STATE_INIT = 0
    STATE_ARPQ = 1
    STATE_DOING_ARPQ = 2
    STATE_DONE_ARPQ = 3
    
    def __init__(self):
        self.state = SenderPacket.STATE_INIT
        
        self._device = None
        self._ip = str()
        self._data = str()

    def int_execute(self, name, ip_to, dataSend, icmp):
        if self.state == SenderPacket.STATE_INIT:
            self.init_send_packet(name, ip_to, dataSend)
            self.state += 1
        if self.state == SenderPacket.STATE_ARPQ:
            if ip_to == self._device.bit_ip(self._device.subred_broadcast):
                self._device.ARPQ_mac_to = mult_x(bin(0xFFFF)[2:], 8)
                self.state += 2
            elif self._device.do_ARPQ(self._ip):
                Simulator_Singleton.instance().sending_device.add(self._device)
                self.state += 1
        elif self.state == SenderPacket.STATE_DOING_ARPQ:
            if self._device.done_ARPQ:
                self.state += 1
        elif self.state == SenderPacket.STATE_DONE_ARPQ:
            return self.send_packet(icmp)

    def execute(self, instruction, icmp=False):
        return self.int_execute(instruction.name_from, instruction.IP_to, instruction.dataSend, icmp)
    
    def init_send_packet(self, name, ip, data):
        self._device = Storage_Device_Singleton.instance().get_device_with(name)
        self._ip = self._device.ip_bit(ip)
        self._data = data
    
    def send_packet(self, icmp):
        data = INIT_FRAME_BIT 
        data += mult_x(self._device.ARPQ_mac_to,16)
        data += mult_x(self._device.MAC,16)
        
        TTL = OFF_SET
        Protocolo = OFF_SET if not icmp else "0"*7 + "1"
        real_data = self._ip + self._device._assoc_ip[0] + TTL + Protocolo
        real_data += mult_x(bin(len(mult_x(hex_bin(self._data),8))//8)[2:],8)
        
        real_data += mult_x(hex_bin(self._data), 8)
        
        data += mult_x(bin(len(mult_x(real_data,8))//8)[2:],8)
        det = self._device.detection.apply(mult_x(real_data, 8))
        data += det[0]
        data += real_data
        data += det[1]

        if self._device.send(data, True):
            Simulator_Singleton.instance().sending_device.add(self._device)
            return True
        return False

class Setter_IP(Executor):
    def execute(self, instruction):
        if not Setter_IP.__is_reserved_ip(instruction.ip):
            _device = Storage_Device_Singleton.instance().get_device_with(instruction.host)
            _device.set_ip(instruction.ip, instruction.mask, instruction.interface)
            return True
        raise Exception("You can't assign this IP")

    @staticmethod
    def __is_reserved_ip(ip: str):
        __last_digit = int(ip.split(".")[3])
        return __last_digit in [0, 255]

class RouteReseter(Executor):
    def execute(self, instruction):
        _device = Storage_Device_Singleton.instance().get_device_with(instruction.name_device)
        if isinstance(_device, RouterTable):
            _device.clean()
            return True
        return False

class RouteAdder(Executor):
    def execute(self, instruction):
        _device = Storage_Device_Singleton.instance().get_device_with(instruction.name_device)
        if isinstance(_device, RouterTable):
            _device.add(Route(instruction.destination, instruction.mask, instruction.gateway, instruction.interface))
            return True
        return False

class RouteRemover(Executor):
    def execute(self, instruction):
        _device = Storage_Device_Singleton.instance().get_device_with(instruction.name_device)
        if isinstance(_device, RouterTable):
            _device.delete(Route(instruction.destination, instruction.mask, instruction.gateway, instruction.interface))
            return True
        return False

class PingExecutor(Executor):
    STATE_INIT = 0
    STATE_FIRST_PING = 2
    STATE_SECOND_PING = 4
    STATE_THIRD_PING = 6
    STATE_FORTH_PING = 8

    def __init__(self):
        self.state = PingExecutor.STATE_INIT
        self.sender = SenderPacket()
        self.time = 0

    def execute(self, instruction):
        if self.state == PingExecutor.STATE_INIT:
            self.send_ping(instruction)
            self.state = PingExecutor.STATE_FIRST_PING
        elif self.state == PingExecutor.STATE_FIRST_PING and self.sender._device.donePing == 1:
            if PingExecutor.get_time() - self.time == 100:
                self.send_ping(instruction)
                self.state = PingExecutor.STATE_SECOND_PING
        elif self.state == PingExecutor.STATE_SECOND_PING and self.sender._device.donePing == 2:
            if PingExecutor.get_time() - self.time == 100:
                self.send_ping(instruction)
                self.state = PingExecutor.STATE_THIRD_PING
        elif self.state == PingExecutor.STATE_THIRD_PING and self.sender._device.donePing == 3:
            if PingExecutor.get_time() - self.time == 100:
                self.send_ping(instruction)
                self.state = PingExecutor.STATE_FORTH_PING
        elif self.state == PingExecutor.STATE_FORTH_PING and self.sender._device.donePing == 4:
            self.sender.donePing = 0


    def send_ping(self, instruction):
        self.sender.int_execute(instruction.host, instruction.ip, mult_x(str(bin(8))[2:], 8), True)
        self.time = PingExecutor.get_time()

    @staticmethod
    def get_time():
        return Simulator_Singleton.instance().getSimulationTime()