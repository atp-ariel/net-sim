class CorruptInstructionException(Exception):
    ''' Represent an Exception about corrupted state of instructions
    by default the message is Instruction is corrupted! '''
    def __init__(self, msg = "Instruction is corrupted!"):
        super().__init__(msg)
    
class NoneInstructionFileException(Exception):
    ''' Represent an exception about not file instruction '''
    def __init__(self, msg="None Instruction File to execute"):
        super().__init__(msg)

class NonExistentInstructionFileException(Exception):
    ''' Represent an exception about non existent file '''
    def __init__(self, msg="Not instruction file at this path"):
        super().__init__(msg)

class MissConfigFileException(Exception):
    ''' Represent an exception about missing config file '''
    def __init__(self, msg="Missing config file"):
        super().__init__(msg)

class UnknowKeyOfConfigException(Exception):
    def __init__(self, key):
        super().__init__(f"Unknown key {key} on config dict")

class ClassNotSupportedException(Exception):
    def __init__(self, clss):
        super().__init__(f"Class '{clss}' not supported")