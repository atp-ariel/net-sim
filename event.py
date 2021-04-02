class EventHook(object):
    ''' Represent an event hook '''
    def __init__(self):
        self.__handlers = []

    def __iadd__(self, handler):
        ''' Redefine the operator += of event, 
        
        e.g: >> a = EventHook()
             >> a += funct
             
             >> def funct():
             >>     print("Hello World!")
             >> a.fire()
             Hello World!'''
        self.__handlers.append(handler)
        return self

    def __isub__(self, handler):
        ''' Redefine the operator -= of event '''
        self.__handlers.remove(handler)
        return self

    def fire(self, *args, **keywargs):
        ''' Raise the event, and execute all handlers, return the last result of handlers

        e.g: >> a = EventHook()
             >> a += funct1
             >> a += funct2

             >> def funct1():
             >>     return "Hello World!
             >> def funct2():
             >>     return "Hola Mundo"
             >> print(a.fire())
             Hola Mundo'''
        response = None
        for handler in self.__handlers:
            response = handler(*args, **keywargs)
        return response