import abc
from collections import deque
from logger import *

class Network_Component(metaclass=abc.ABCMeta):
    def __init__(self,name,no_ports):
        # name of device
        self.name=name
        # list of ports, if ports[i] = '' then this ports is not connected, else this ports is connected to ports[i]
        self.ports=['' for x in range(no_ports)]

class Wire(Network_Component):
    def __init__(self,name,port_1,port_2):
        super.__init__(name,2)
        # port 1 that a wire connect
        self.ports[0]=port_1
        # port 2 
        self.ports[1]=port_2

        # bit of the wire
        self.red=None
        # bit of the wire
        self.blue=None

class Device(Network_Component,metaclass=abc.ABCMeta):
    ''' Abstract class that represent a device on the network'''
    def __init__(self,name,no_ports):
        super().__init__(name,no_ports)
        # values that read
        self.read_value = [None for i in range(no_ports)]
        # cable to send True=red False=blue
        self.cable_send=[False for i in range(no_ports)]
        # device's log file
        self.logger = Logger(open("./output/" + self.name + ".txt", "w"))
        # event to ask for the signal time of the simulation.
        self.askSignalTime = EventHook()
         # event to query a specific device from the device list
        self.consultDevice = EventHook()
        # event to consult the index of a device given its name
        self.consultDeviceMap = EventHook()
        # event to know the number of devices at a given time on the network
        self.askCountDevice = EventHook()

    def report_receive_ok(self, bit, port):
        ''' Report by a log message that it received a bit successfully '''
        # If the bit is None then it does not report because there was no current in the communication channel 
        if bit == None:
            return
        # the logger write the log message
        self.logger.write(f"{port} receive {bit}")

    def clean(self):
        self.read_value = None
        self.receive_port = None
        
    def xor(self, a, b):
        ''' XOR operator to apply to the channel and review if another device is sending data '''
        if a==None:
            return b
        elif b==None:
            return a
        return a^b

class Host(Device):
    ''' This class represent a Host device '''
    def __init__(self,name):
        super().__init__(name,1)
        self.data_logger = Logger(open("./output/" + self.name + "_data.txt", "w"))
    
    def report_collision(self, data):
        ''' Report collision on log file '''
        self.logger.write(f"{self.name} send {data} collision")
    
    def report_send_ok(self, data):
        ''' Report success send of log file '''
        if data == None:
            return
        self.logger.write(f"{self.name}_1 send {data} ok")

    def propagate(self, bit):
        ''' Propagates a bit through the using the BFS algorithm '''
        # visited device on network
        visited=[False for x in range(self.askCountDevice.fire())]
        # queue of BFS
        queue=deque()
        # append the root to the queue
        queue.append(self.name)

        # while the queue is not empty
        while len(queue)!=0:
            # device on the top of the queue
            actual_device = self.consultDevice.fire(self.consultDeviceMap.fire(queue.pop()))
            # mark as visited
            visited[self.consultDeviceMap.fire(actual_device.name)]=True

            actual_device.report_receive_ok(bit)
            if type(actual_device) is Hub:
                actual_device.report_resend(bit)

            # for each port of the device's port
            for port_name in actual_device.ports:
                if port_name=='':
                    continue
                # if port is connected get device connected
                device=get_device_port(port_name)[0]
                # if this device is not visited the put on the queue and save info about who send data
                if not visited[self.consultDeviceMap.fire(device)]:
                    self.consultDevice.fire(self.consultDeviceMap.fire(device)).receive_port=port_name
                    queue.append(device)
                
    def send(self, data):
        ''' Function to send data to the network '''
        # data to send
        self.data_to_send = data
        # index of the bit in data to send
        self.index_sending = 0
        # time sending data[index]
        self.time_sending = 0

        return self._send(self.data_to_send[self.index_sending])

    def _send(self, bit):
        wire = self.consultDevice.fire(self.consultDeviceMap.fire(get_device_port(self.ports[0])[0])) 
        
        if self.cable_send[0]:
            wire.red = bit
        else:
            wire.blue = bit

        wd = self.consultDevice.fire(self.consultDeviceMap.fire(get_device_port(wire.ports[1])[0] if wire.ports[0]==self.name+str(1) else get_device_port(wire.ports[0])[0]))
        if type(wd) is IResender:
            wdp = wire.ports[1] if wire.ports[0]==self.name+str(1) else wire.ports[0]
            if wd.resend(bit, wdp) is "COLLISION":
                self.report_collision(bit)
                return False
            else:
                wd.resend(bit, wdp, True)
        elif type(wd) is Host:
            wd.read(True)
        self.report_send_ok(bit)
        return True

    def read(self, report):
        wire = self.consultDevice.fire(self.consultDeviceMap.fire(get_device_port(self.ports[0])[0])) 
        rd = wire.red if self.cable_send[0] else wire.blue
        if report:
            self.report_receive_ok(rd, f"{self.name}_1")

    def keep_sending(self):
        ''' Keep sending a data throught network '''
        signal_time = self.askSignalTime.fire()
 
        # if this device is sending and the sending time is less that signal time then continue spreading data
        if self.time_sending < signal_time - 1:
            self._send(self.data_to_send[self.index_sending])
            self.time_sending += 1
            return True
        # if signal time is accomplished then
        else:
            # if send all data then spread "empty channel" status
            if self.index_sending >= len(self.data_to_send) - 1:
                self._send(None)
                self.time_sending = 0
                self.index_sending = 0
                self.data_to_send = None
                return False
            # else spread the next bit 
            else:
                self.index_sending += 1
                self._send(self.data_to_send[self.index_sending])
                self.time_sending = 0
                return True

    def set_MAC(self,mac):
        self.MAC=mac

class IResender:
    def resend(self,bit, port_name, write=False):
        pass
        
class Hub(Device, IResender):
    ''' This class represent a Hub device '''
    def __init__(self,name,no_ports):
        super().__init__(name,no_ports)
    
    def report_resend(self, bit, port):
        ''' This function reports in the log messages the forwarding of data through all ports '''
        if bit == None:
            return
        name_ports = [self.name + "_" + str(i + 1) for i in range(len(self.ports))]
        name_ports.remove(port)
        for i in name_ports:
            self.logger.write(f"{i} send {bit}")
    
    def report_collision(self):
        pass

    def resend(self, bit, port_name, write=False):
        list_port = []
        for i in range(len(self.ports)):
            port = self.ports[i]
            if port[i] == "":
                continue
            wire = self.consultDevice.fire(self.consultDeviceMap.fire(get_device_port(port)[0]))
            if self.cable_send[i]:
                if not wire.red is None:
                    self.report_collision()
                    return "COLLISION"
                wire.red = bit
            else:
                if not wire.blue is None:
                    self.report_collision()
                    return "COLLISION"
                wire.blue = bit
            list_port.append(i)
            
            wd = get_device_port(wire.ports[1])[0] if wire.ports[0]==self.name+str(i) else get_device_port(wire.ports[0])[0]
            if type(wd) is IResender:
                wdp =wire.ports[1] if wire.ports[0]==self.name+str(i) else wire.ports[0]
                if wd.resend(bit, wdp, write) is "COLLISION":
                    self.report_collision()
                    return "COLLISION"
            elif type(wd) is Host:
                wd.read(write)
        if write:
            self.report_resend(bit, port_name)
        return list_port

class Switch(Device, IResender):
    def __init__(self,name,no_ports):
        super().__init__(name,no_ports)
        self.macs=[set() for i in range(no_ports)]
    
    def resend(self, bit, port_name):
        pass

