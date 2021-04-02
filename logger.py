from util import *
from event import EventHook

class Logger:
    ''' Represent an object that write on the log file '''
    def __init__(self, fd):
        # log file
        self.log = fd
        # event that ask for simulation time to print
        self.askForSimulationTime = EventHook()

    def write(self, message):
        ''' Write on log file '''
        self.log.write(str(self.askForSimulationTime.fire()) + " " + message + "\n")