# attack victim and monitor all his activities

# sudo python3 attack.py

# detect the WLAN
"""
1. turn on monitor mode
2. scan
3. display all the WI-FI
4. let the user choose one WI-FI
5. display choosen WI-FI users
"""
# attack
"""
1. let the user choose wich one he wants to attack
2. Disconnect the victim from WI-FI (using deauthentication)
...
*. display victim's activities 
"""
# finish
"""
1. turn off monitor mode
"""

# use thread to scanning and detect access point and end point (user)

import os
from socket import timeout       # check the function inside
import time
from scapy.all import *


def command_line(command: str):       # -> None
    return os.system(command)


def change_monitor(net_card: str, mode: str):     # -> None:
    print('change mode')
    command_line('ifconfig ' + net_card + ' down')
    command_line('iwconfig ' + net_card + ' mode ' + mode)
    command_line('ifconfig ' + net_card + ' up')


def change_channel(net_card: str):
    # sudo iwconfig $1 channel $2
    print('change channel')
    nums_of_channel = 2      # need to check how channel need to scan
    ch = 1
    # during couple minutes  
    while ch < nums_of_channel: 
        command_line('iwconfig' + net_card + 'channel' + ch)
        ch += 1
        time.sleep(1)


def sniff_network():
    print('sniff network')


def scanning(net_card: str):
    print('scanning')

    change_channel_thread = Thread(target=change_channel, args=(net_card))
    change_channel_thread.start()

    my_time = 10        # check the time
    try:
        sniff(prn=sniff_network, iface=net_card, timeout=my_time)     # saved function (scapy) -> check how to use it
    except:
        print('print propper massege and check the type of the exception')
    
    change_channel_thread.join()


def choose_network_to_attack():
    print('choose_network_to_attack')


def start_attack():
    print('start EVIL TWIN attack...')
    if os.geteuid():
        sys.exit('need sudo permission')
    
    net_card_name = input('insert your network card name: ')
    # need to check if the net_card is exist
    os.popen('iwconfig').read()         # check how to use it 
    
    # realy start the attack
    change_monitor(net_card_name, 'monitor')
    
    # using thread and wait for the thread join
    scanning(net_card_name)

    choose_network_to_attack()      # need to do
    
    # end the attack
    change_monitor(net_card_name, 'managed')


if __name__ == '__main__':
    start_attack()
