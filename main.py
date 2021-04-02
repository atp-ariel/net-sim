from simulator import *
from initializer import *

if __name__ == "__main__":
    # Give me an instance of the simulator class. This instance will 
    # be in charge of handling the entire simulation. It will also 
    # have the devices connected to the network. It will also handle 
    # the simulation times, the signal time, the pending instructions, 
    # the instructions that have to be executed in a time and it will 
    # also handle the data sending
    
    init = Initializer()
    init.load_config()
    
    simulator = Simulator(init.get("signal_time"), init.get("script_name"))
    del init

    while True:
        # update the instructions that must be executed in the current simulation time
        simulator.update_instructions()
        
        # clear devices 
        simulator.clear_network_component()

        # execute pending data sendings
        simulator.execute_sending_device()
        
        # execute the instructions of this time
        simulator.execute_time_instructions()
        print(simulator.devices[0].MAC)
        
        # check if the simulation stop condition was reached
        if simulator.must_stop():
            break
        
        #uncomment to report simulation details
        #report(simulator.simulation_time, simulator.devices)

        #then advance simulation time 
        simulator.advance_simulation()