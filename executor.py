from abc import ABCMeta, abstractmethod

class Executor(metaclass = ABCMeta):
    @abstractmethod
    def execute(self, instruction):
        pass

class Connector(Executor):
    def execute(self, instruction):
         ''' connect network devices and check that it remains in a non-collision state '''
        instruction.device_1, instruction.device_2 = self.devices[self.deviceMap[instruction.device_1]], self.devices[self.deviceMap[instruction.device_2]]

        if instruction.device_1.ports[instruction.port_1]=='' and instruction.device_2.ports[instruction.port_2]=='':
            is_hub_d1, is_hub_d2 = isinstance(instruction.device_1, Hub), isinstance(instruction.device_2, Hub)
            more_than_2d_sending = lambda x: len(list(filter(lambda y: y != None, x.read_value))) >= 2
            hub_d_sending = lambda x: len(list(filter(lambda y: y != None, x.read_value))) == 1
            
            # si el dispositivo uno es un hub que tiene mas de un dispositivo enviando entonces uno debe callarse para evitar la colision
            if is_hub_d1 and more_than_2d_sending(instruction.device_1):
                self.shut_up_a_host(instruction.device_1)
            # si el dispositivo 2 es un hub que tiene mas de un dispositivo enviando enotnces uno debe callarse
            if is_hub_d2 and more_than_2d_sending(instruction.device_2):
                self.shut_up_a_host(instruction.device_2)
            # si ambos son hub con un dispositivo enviando, uno de ellos debe callarse
            if is_hub_d1 and is_hub_d2 and hub_d_sending(instruction.device_1) and hub_d_sending( instruction.device_2):
                self.shut_up_a_host(instruction.device_1)
            
            wire=Wire('wire'+str(len(self.devices)),instruction.name_1,instruction.name_2)
            self.deviceMap[wire.name]=len(self.deviceMap)
            self.devices.append(wire)
            instruction.device_1.ports[instruction.port_1]=wire.name +'_'+str(1)
            instruction.device_2.ports[instruction.port_2]=wire.name +'_'+str(2)
            instruction.device_1.cable_send[instruction.port_1]=True
            instruction.device_2.cable_send[instruction.port_2]=False
        else:
            print('Busy port. Ignored action')