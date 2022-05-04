from  scapy.all import *


class Fake:
    def __init__(self, interface, net_mac, cli_mac):
        self.interface = interface
        self.net_mac = net_mac
        self.cli_net = cli_mac
        print('\ncreating fake ap')
    
    def deauthentication(self):
        print('deauthentication')