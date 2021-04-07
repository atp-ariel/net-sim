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

def bin_hex(binary):
    return hex(int(binary,2))[2:].upper()

def hex_bin(hexadecimal):
    return bin(int(hexadecimal,16))[2:]

def mult_x(s,x):
    if len(s) % x != 0:
        off = "0" * (x - (len(s)%x))
        s = off + s
    return s

INIT_FRAME_BIT = 2
OUTPUT_DIR = "./output"