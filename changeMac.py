#!/usr/bin/env python3
# to run the tool sudo ./changeMac.py
import subprocess


def change_mac(interface, new_mac):
    print(f"\n[+] changing MAC address to {new_mac}...")

    # Disable the network interface
    subprocess.run(["ifconfig", interface, "down"])

    # Change the MAC address
    subprocess.run(["ifconfig", interface, "hw", "ether", new_mac])

    # Enable the network interface
    subprocess.run(["ifconfig", interface, "up"])

    print(f"[i] MAC address was changed")
    print(f"[i] press ctrl+c to reset the MAC address ")


def reset_mac(interface, original_mac):
    print(f"[+] resetting MAC address to {original_mac}...")

    # Disable the network interface
    subprocess.run(["ifconfig", interface, "down"])

    # Change the MAC address back to the original MAC
    subprocess.run(["ifconfig", interface, "hw", "ether", original_mac])

    # Enable the network interface
    subprocess.run(["ifconfig", interface, "up"])
    print(f"[i] MAC address was reset")


# Ask for user input
interface = input("Enter the interface name: ")

# Store the original MAC address
result = subprocess.check_output(["ifconfig", interface], text=True)
original_mac = result.split("ether ")[1].split()[0]


# Print the original MAC address
print(f"[i] original MAC address: {original_mac}\n")

# Change the MAC address
new_mac = input("Enter the new MAC address: ")
change_mac(interface, new_mac)

try:
    while True:
        pass
except KeyboardInterrupt:
    print("\n[+] ctrl+c detected...")
    reset_mac(interface, original_mac)
