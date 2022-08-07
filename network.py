import os
import time
from scapy.all import *
from scapy.layers.dot11 import Dot11, Dot11Beacon, Dot11Elt


ssid_list = list() 
client_list = list()
mac_ssid = ''       # global MAC address


def command_line(command: str):
    return os.system(command)


def choose_duplicate():
    duplicate_ssid = list()
    for i in range(len(ssid_list)):
        j = i + 1
        while j < len(ssid_list):
            temp_ssid = ssid_list[i][0]
            if temp_ssid == ssid_list[j][0]: 
                if temp_ssid not in duplicate_ssid:
                    duplicate_ssid.append(temp_ssid)
            j += 1

    length = len(duplicate_ssid)
    if length > 0:
        print('there are more than one AP with those ssid each one and cause a problem: ')
        for i in range(length):
            print('\t' + str(i) + ': ' + duplicate_ssid[i])
        print('wich one you want to check their mac address? ')
        cli = int(input(''))
        if cli < 0 or cli > length:
            return -1
        else:
            return duplicate_ssid[cli]
    return -2


def choose_target(target_ssid):
    sus_mac = list()
    for i in range(len(ssid_list)):
        if ssid_list[i][0] == target_ssid:
            sus_mac.append(ssid_list[i][1])
    
    length = len(sus_mac)
    if length > 0:
        print('\ncheck if you know all the mac address: ')
        for i in range(length):
            print('\t' + str(i) + ': ' + sus_mac[i])
        ans = input('do you know all? [y/n] ')
        if ans == 'y':
            return -2
        cli = int(input('wich one do you want to attack? '))
        if cli < 0 or cli > length:
            return -1
        else:
            return sus_mac[cli]
    return -2


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
        # addr1 = who hear the pkt, 2 = who send the pkt, 
        # 3 = who the source, 4 = destination
        if mac not in [temp[1] for temp in ssid_list[0:]]:
            ssid_name = pkt[Dot11Beacon].info.decode()
            # mac address + number of the channel
            channel = str(ord(pkt[Dot11Elt:3].info))      
            ssid_list.append([ssid_name, mac, channel])


def sniff_clients(pkt):
    # boadcast? ff:ff:ff:ff:ff:ff
    if (pkt.addr2 == mac_ssid  or pkt.addr3 == mac_ssid) and pkt.addr1 != 'ff:ff:ff:ff:ff:ff':
        client_mac = pkt.addr1
        if client_mac not in client_list and client_mac != mac_ssid:
            client_list.append(client_mac)


def change_channels(net_card):
    nums_of_channel = 14      # need to check how channels need to scan 
    for(ch = 1; ch < nums_of_channel; ch += 1) 
        command_line('iwconfig ' + net_card + ' ch ' + str(ch))
        time.sleep(4)


def change_monitor(net_card: str, mode: str):
    print('\nchanging mode...')
    command_line('ifconfig ' + net_card + ' down')
    command_line('iwconfig ' + net_card + ' mode ' + mode)
    command_line('ifconfig ' + net_card + ' up')
    print('mode: ' + mode)


class Network:
    def __init__(self):
        self.interface = input('Insert your network card name: ')
        change_monitor(self.interface, 'monitor')

    def scanning_networks(self, isAttck):     # need to add the posibility to scan again
        print('\nscanning for network...')

        change_channel_thread = Thread(target=change_channels, args=(self.interface,))      # the ',' is must
        change_channel_thread.start()

        my_time = 60        # check the time
        try:
            sniff(prn=sniff_networks, iface=self.interface, timeout=my_time)
        except:
            print('sniff network problem')
        
        change_channel_thread.join()
        if isAttck:
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
            
            return network_to_attack

        target_ssid = choose_duplicate()
        if target_ssid == -1:
                print('not a valid input')
                return 'None'
        elif target_ssid == -2:
            print('all good! no evil twin attack')
            return 'None'
        evil_mac = choose_target(target_ssid)
        if evil_mac == -1:
            print('not a valid input')
            return 'None'
        elif evil_mac == -2:
            print('not found any network')
            return 'None'
        return evil_mac
        
    def scanning_clients(self):
        print('\nscanning for clients...')
        my_time = 60       # check the time
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