import os
import time
from scapy.all import *
from scapy.layers.dot11 import Dot11, Dot11Beacon, RadioTap, Dot11Elt


ssid_list = list() # need to chnge to list
client_list = list()
mac_ssid = ''       # global MAC address

def command_line(command: str):
    return os.system(command)


def choose_client():
    length = len(client_list)
    if length > 0:
        print('found:')
        for i in range(length):
            print('\t' + str(i) + ': ' + client_list[i])
        print('choose client:')
        cli = int(input(''))
        if cli < 0 or cli > length:
            return -1
        else:
            return client_list[cli]
    return -2

def choose_net():
    length = len(ssid_list)
    if length > 0:
        print('found:')
        for i in range(length):
            print('\t' + str(i) + ': ' + ssid_list[i][0])
        print('choose network:')
        cli = int(input(''))
        if cli < 0 or cli > length:
            return -1
        else:
            return ssid_list[cli]
    return -2


def sniff_networks(pkt):
    if pkt.haslayer(Dot11Beacon):
        mac = pkt[Dot11].addr2
        if mac not in [temp[1] for temp in ssid_list[0:]]:
            ssid_name = pkt[Dot11Beacon].info.decode()
            # mac address + number of the channel
            channel = str(ord(pkt[Dot11Elt:3].info))      
            ssid_list.append([ssid_name, mac, channel])


def sniff_clients(pkt):
    if (pkt.addr2 == mac_ssid  or pkt.addr3 == mac_ssid) and pkt.addr1 != 'ff:ff:ff:ff:ff:ff' :
        client_mac = pkt.addr1
        if client_mac not in client_list and client_mac != mac_ssid:
            client_list.append(client_mac)


def change_channels(net_card):
    nums_of_channel = 14      # need to check how channels need to scan
    ch = 1
    time.sleep(1)
    # during couple minutes  
    while ch < nums_of_channel: 
        command_line('iwconfig ' + net_card + ' ch ' + str(ch))
        ch += 1
        time.sleep(1)


def change_monitor(net_card: str, mode: str):
    print('\nchanging mode...')
    command_line('ifconfig ' + net_card + ' down')
    command_line('iwconfig ' + net_card + ' mode ' + mode)
    command_line('ifconfig ' + net_card + ' up')    


class Network:
    def __init__(self):
        self.interface = 'wlxd03745b00a7c' #input('Insert your network card name: ')
        change_monitor(self.interface, 'monitor')
        print('mode monitor')

    def scanning_networks(self):
        print('\nscanning for network...')

        change_channel_thread = Thread(target=change_channels, args=(self.interface,))      # the ',' is must
        change_channel_thread.start()

        my_time = 15        # check the time
        try:
            sniff(prn=sniff_networks, iface=self.interface, timeout=my_time)
        except:
            print('print propper massege and check the type of the exception')
        
        change_channel_thread.join()

        network_to_attack = choose_net()
        if network_to_attack == -1:
            print('not a valid input')
            return 'None'
        elif network_to_attack == -2:
            print('not found any network')
            return 'None'
        ch = network_to_attack[2]
        print('changing channel to ' + ch)
        command_line('iwconfig ' + self.interface + ' ch ' + ch)
        global mac_ssid
        mac_ssid = network_to_attack[1]
        return mac_ssid
        
    def scanning_clients(self):
        print('\nscanning for clients...')
        my_time = 15        # check the time
        try:
            sniff(prn=sniff_clients, iface=self.interface, timeout=my_time)
        except:
            print('print propper massege and check the type of the exception')
        
        client_to_attack = choose_client()
        if client_to_attack == -1:
            print('not a valid input')
            return 'None'
        elif client_to_attack == -2:
            print('not found any clients')
            return 'None'
        print('\nattacking: ' + client_to_attack)
        return client_to_attack

    def get_interface(self):
        return self.interface

    def off(self):
        change_monitor(self.interface, 'managed')
        print('mode managed')
