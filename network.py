import os
from pstats import Stats
import time
from scapy.all import *
from scapy.layers.dot11 import Dot11, Dot11Beacon, RadioTap, Dot11Elt


ssid_dict = dict()


def command_line(command: str):
    return os.system(command)


def choose_net():
    print('found: ')
    for i in ssid_dict:
        print('\tname: ' + i)
    # attack_net = input('\nchoose the WIFI you want to attack one of his client: ')
    attack_net = 'None'
    print('\nInsert the WIFI *name* you want to attack one of his client: ')
    return attack_net


def sniff_network(pkt):
    if pkt.haslayer(Dot11Beacon):
        mac = pkt[Dot11].addr2
        if mac not in ssid_dict:
            ssid_name = pkt[Dot11Beacon].info.decode()
            # mac address + number of the channel
            to_save = mac + ' '  + str(ord(pkt[Dot11Elt:3].info))
            ssid_dict[ssid_name] = to_save


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
        self.interface = input('Insert your network card name: ')
        change_monitor(self.interface, 'monitor')
        print('mode monitor')

    def scanning_network(self):
        print('\nscanning...')

        change_channel_thread = Thread(target=change_channels, args=(self.interface,))      # the ',' is must
        change_channel_thread.start()

        my_time = 15        # check the time
        try:
            sniff(prn=sniff_network, iface=self.interface, timeout=my_time)
        except:
            print('print propper massege and check the type of the exception')
        
        change_channel_thread.join()

        net_attack = choose_net()

        if net_attack != 'None':
            temp = ssid_dict[net_attack].split()
            channel = temp[1] 
            command_line('iwconfig ' + self.interface + ' ch ' + channel)
            print('channel now: ' + channel)
        return net_attack


    def off(self):
        change_monitor(self.interface, 'managed')
        print('mode managed')
