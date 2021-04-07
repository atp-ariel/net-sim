from simulator_singleton import Simulator_Singleton

if __name__ == "__main__":
    # Give me an instance of the simulator class. This instance will 
    # be in charge of handling the entire simulation. It will also 
    # have the devices connected to the network. It will also handle 
    # the simulation times, the signal time, the pending instructions, 
    # the instructions that have to be executed in a time and it will 
    # also handle the data sending

    while True:
        # update the instructions that must be executed in the current simulation time
        Simulator_Singleton.instance().update_instructions()
        
        # clear devices 
        Simulator_Singleton.instance().clear_network_component()

        # execute pending data sendings
        Simulator_Singleton.instance().execute_sending_device()
        Simulator_Singleton.instance().send_switch()

        # execute the instructions of this time
        Simulator_Singleton.instance().execute_time_instructions()
        Simulator_Singleton.instance().read_host_wire()

        # check if the simulation stop condition was reached
        if Simulator_Singleton.instance().must_stop():
            break
        
        #then advance simulation time 
        Simulator_Singleton.instance().advance_simulation()