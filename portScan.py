#!/usr/bin/env python3
# pip install python-nmap
# to run the tool sudo ./portScan.py

import nmap
import re


# Ask user to input the ip address they want to scan.
ip_address = input("\nenter the target ip address: ")


print("\n[i] enter the port range in format xx-xx")
port_range = input("Enter port range: ")
min, max = port_range.split('-')
int_min = int(min)
int_max = int(max)

print('\n')

# create an object in PortScanner class
nmp = nmap.PortScanner()

# looping over the ports in the specified port range
for port in range(int_min, int_max + 1):
    try:
        result = nmp.scan(ip_address, str(port))
        # result is a huge dictionary
        # nmap -oX - -p 89 -sV 10.0.0.2
        # print(result)
        # get the port status from that dictionary
        port_status = (result['scan'][ip_address]['tcp'][port]['state'])
        print(f"Port {port} is {port_status}")
    except:
        # for the ports that we cannot start.this ensures the program doesn't show errors when we try to scan them.
        print(f"Cannot scan port {port}.")
