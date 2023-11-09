# to run the tool python3 wifips.py
# pip3 install subprocess
import subprocess
import re

# running windows command to get wifi connection names (get the result in binary so decode it)
cmd_command = subprocess.run(
    ["netsh", "wlan", "show", "profiles"], capture_output=True).stdout.decode()

# extracting connection names from above windows command
wifi_connections_names = (re.findall(
    "All User Profile     : (.*)\r", cmd_command))

# list will have dictionaries of wifi connection names and passwords
wifi_connections_list = []

# if wifi connection names found
if len(wifi_connections_names) > 0:
    for name in wifi_connections_names:

        # create a dict for every wifi connection
        wifi_connection_info = {}

        # running windows command to get information of each wifi connection
        wifi_info_command = subprocess.run(
            ["netsh", "wlan", "show", "profile", name], capture_output=True).stdout.decode()

        # using re module to find if the passwd is there or not
        if re.search("Security key           : Absent", wifi_info_command):
            continue

        # if the passwd found run this else block
        else:
            # adding connection name to the wifi_connection_info dictionary.
            wifi_connection_info["ssid"] = name

            # getting the passwd of the connection
            wifi_passwd_command = subprocess.run(
                ["netsh", "wlan", "show", "profile", name, "key=clear"], capture_output=True).stdout.decode()

            # capturing the password
            password = re.search(
                "Key Content            : (.*)\r", wifi_passwd_command)

            # adding the passwd to wifi_connection_info dict
            if password == None:
                wifi_connection_info["password"] = None
            else:
                # adding the grouping (from re search) of where the password sits
                wifi_connection_info["password"] = password[1]

            wifi_connections_list.append(wifi_connection_info)

for item in wifi_connections_list:
    print(item)
