from devices import *
from util import get_device_port
from storage_device import Storage_Device_Singleton
from random import randint

class ShutUp:
    def __init__(self, simulator_instance):
        self.simulator_instance = simulator_instance

    def shut_up_a_host(self, hub: Hub):
        from instruction_factory_method import getInstruction

        index_rv = list(filter(lambda x: x != -1,[i  if hub.read_value[i] != None else -1 for i in range(len(hub.ports))]))
        to_shut_up = self.find_root(hub.ports[randint(0, len(index_rv)-1)])
        if to_shut_up.sending_frame:
            self.simulator_instance.pending.append(getInstruction(self.simulator_instance.simulation_time + 1, "send_frame", [to_shut_up.name, bin_hex(to_shut_up.data_to_send[1:17]), bin_hex(to_shut_up.data_to_send[49:])]))
        else:
            self.simulator_instance.pending.append(getInstruction(self.simulator_instance.simulation_time +1, "send", [to_shut_up.name, to_shut_up.data_to_send]))
        self.simulator_instance.sending_device.remove(to_shut_up)
        to_shut_up.clean_sending()

    def find_root(self, port_name):
        device_name,port = get_device_port(port_name)
        port=int(port)-1
        component = Storage_Device_Singleton.instance().get_device_with(device_name)
        while True:
            if isinstance(component,Host):
               return component
            elif isinstance(component,Wire):
                port_name=component.ports[1]  if port==0 else component.ports[0]
            else:
                port_name=component.internal_port_connection[port]
            device_name,port=get_device_port(port_name)
            port=int(port)-1
            component = Storage_Device_Singleton.instance().get_device_with(device_name)

               