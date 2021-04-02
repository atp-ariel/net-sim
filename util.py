def list_to_str(L: list, separator = " "):
    ''' Receive a list L and separator and return 
    a string with the item of L separated by separator'''
    slist = ""
    for item in L:
        slist += str(item) + str(separator)
    return slist[:-len(separator)]

def get_device_port(name):
    ''' Given a port name return name and index port '''
    return name.split('_')

def report(simulation_time, devices):
    print(f"=== Time {simulation_time} ===")
    for d in devices:
        print(f"{d.name} {d.read_value}")
    print('===============')