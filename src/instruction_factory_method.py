from instruction import InstructionFactory

def getAllFactory():
    ''' this function returns a dictionary where the key 
    is the name of the class inheriting from Instruction 
    and an instance of the factory of that class ''' 

    factories = {}
    # get dinamically subclasses of instruction factory
    for factory in InstructionFactory.__subclasses__():
        temp = factory()
        factories[temp.name] = temp
    return factories

def getInstruction(time, IType, args):
    ''' Receive time, type of instructions and args of 
    instructions, and return an object of this instruction '''

    factory = getAllFactory()
    return factory[IType].getInstance(time, args)