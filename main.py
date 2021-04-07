from simulator import Simulator
from initializer import Initializer

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
        simulator.send_switch()

        # execute the instructions of this time
        simulator.execute_time_instructions()
        simulator.read_host_wire()

        # check if the simulation stop condition was reached
        if simulator.must_stop():
            break
        
        #then advance simulation time 
        simulator.advance_simulation()