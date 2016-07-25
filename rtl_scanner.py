#!/usr/bin/python
import socket
import subprocess
import sys
from datetime import datetime

# Tuner types, enums in python are a pain...
tuners = {0: 'Unknown', 1: 'E4000', 2: 'FC0012', 3: 'FC0013', 
	      4: 'FC2580', 5: 'R820T', 6: 'R828D'}


# Disect the dongle struct
def check_data_for_dongle(data):
    if len(data) != 12:
        return None
    magic = data[:4]
    tuner_type = int(data[4:8].encode('hex'), 16)
    tuner_gain_count = int(data[8:12].encode('hex'), 16)
    # This keeps the function from spewing gibberish if the data
    # is the right length but no a dongle.
    if magic != "RTL0":
            return None
    return (magic, tuner_type, tuner_gain_count)

# Connect to address
def check_host_for_dongle(address, port=1234):
    
    # Create and connect the socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((address, port))
    
    #Check for successful connection
    if result == 0:
        data = sock.recv(12)
        device = check_data_for_dongle(data)
        # Yes, it is checked in the function. However, here the
        # same check is prudent to prove it is a dongle and not
        # None. Same check, different purpose.
        if device is not None:
            sock.close()
            return (address, device[0], device[1], device[2])
        sock.close()
    return None


def scan_network_for_dongles(address, mask, port=1234):
    
    # Variables
    dongles_found = []
    network_range = []
    
    # Bail if the port doesn't make sense.
    if port <=0 or port >= 2 ** 16:
        return None
    
    # Split the address and mask
    expanded_address = address.split(".")
    expanded_mask = mask.split(".")
    
    
    # Now check if the address and mask jave the right number of octets
    if len(expanded_address) != 4 or len(expanded_mask) !=4:
        return 0
    
    # Cast octets to "int"s and check that they are the right size.
    for index, octet in enumerate(expanded_address):
        expanded_address[index] = int(octet)
        if expanded_address[index] > 255 or expanded_address[index] < 0:
            return None
        
    for index, octet in enumerate(expanded_mask):
        expanded_mask[index] = int(octet)
        if expanded_mask[index] > 255 or expanded_mask[index] < 0:
            return None
        
    # Calculate network "range"
    for octet in range(0, 4):
        # Will make the ranges work correctly
        if expanded_mask[octet] == 255:
            network_range.append((expanded_address[octet], 
								 expanded_address[octet] + 1))
        else: # XORing the mask to 0xFF gives us the wildcard mask which is essentially how "far" to go.
            network_range.append((expanded_address[octet] + 1,
                                  expanded_address[octet] + 
                                  expanded_mask[octet] ^ 0xFF))
		
    # Big loops
    for first in range(network_range[0][0], network_range[0][1]):
        for second in range(network_range[1][0], network_range[1][1]):
            for third in range(network_range[2][0], network_range[2][1]):
                for fourth in range(network_range[3][0], network_range[3][1]):
                    result = check_host_for_dongle(str(first) + "." + str(second) + "." + str(third) + "." + str(fourth),
                                                   port)
                    if result is not None:
                        dongles_found.append(result)                   

    return dongles_found

if __name__ == "__main__":
    
    #scan for the dongles
    dongles = scan_network_for_dongles("127.0.0.0", "255.255.255.0")
    
    #Create some space before spewing the tuners found
    print("\n\n\n\n\n")
    
    #print the dongles found
    if len(dongles) > 0:
        print("The Following dongles were found")
        print("Address\t\tType\tGain")
        for host in dongles:
            print(host[0] + "\t" 
                  + tuners[host[2]] + "\t" + str(host[3]))
    else:
        print("No dongles found. :(")
