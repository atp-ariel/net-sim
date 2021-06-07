from util import OUTPUT_DIR
from event import EventHook

class Logger:
    ''' Represent an object that write on the log file '''
    def __init__(self, name_file):
        # log file
        self.path_file = OUTPUT_DIR + "/" + name_file
        # event that ask for simulation time to print
        self.askForSimulationTime = EventHook()

        log = open(self.path_file, "a")
        log.close()


    def write(self, message):
        ''' Write on log file '''
        log = open(self.path_file, "a")
        log.write(str(self.askForSimulationTime.fire()) + " " + message + "\n")
        log.close()