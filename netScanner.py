#!/usr/bin/env python3
# to run the tool ./netScanner.py -t

# pip3 install scapy-python3
import scapy.all as scapy
import argparse


# function to use -t switch in the terminal
def get_arguments():
    # parser object
    parser = argparse.ArgumentParser()

    # adding switches to be used in terminal
    parser.add_argument('-t', '--target', dest='target',
                        help='target IP range')

    # storing user input values in options object
    options = parser.parse_args()

    return options


def scan(ip):
    # creating a instance of ARP class
    # scapy.ls(scapy.ARP()) shows different fields that can be added like 'pdst'
    arp_request = scapy.ARP(pdst=ip)
    # arp_request.show()

    # creating an ethernet frame
    broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
    # broadcast.show()

    # Combining the ARP request and Ethernet frame to create the complete packet
    arp_request_broadcast = broadcast/arp_request
    # arp_request_broadcast.show()

    # srp (Send & Recieve Pkts) for pkts with custom ether parts
    # answered_pkts_list is a list of tuples that store pkts & responses
    answered_pkts_list = scapy.srp(arp_request_broadcast,
                                   timeout=1, verbose=False)[0]

    # Creating a list to store the client information
    client_list = []

    # answered_pkts_list = [(packet1, response1),(packet2, response2)]
    for item in answered_pkts_list:
        client_dict = {'ip': item[1].psrc, 'mac': item[1].hwsrc}

        # adding dicts to the list
        client_list.append(client_dict)
    return client_list


# print result to the terminal
def print_results(results_list):
    print('IP\t\t\tMAC address\n-------------------------------------------')
    for item in results_list:
        print(item['ip'] + '\t\t' + item['mac'])


# assign options object to variable options
options = get_arguments()

# do the scan & assign scan results to a variable
scan_result = scan(options.target)

# print scan result
print_results(scan_result)
