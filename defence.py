# detect the attack and block Evil twin attack

# attack victim and monitor all his activities

# sudo python3 attack.py

# detect
"""
1. turn on monitor mode
2. scan
3. display all the WI-FI that has more than one ap with the same ssid
4. let the user choose his ssid
5. display all the mac address attach to this ssid
6. let the user choose wich one to attack (attack the one he doesn't know)
"""
# attack
"""
1. ask the user how much time to attack
2. Disconnect the victim from WI-FI (using deauthentication)
3. Disconnect the WI-FI from victim (using deauthentication)
4. ask if he want to repeat on the scan
"""
# finish
"""
1. turn off monitor mode
"""

from network import Network
from fake import deauthentication_packet


def start_defence():
    # if os.geteuid():
    #     sys.exit('need sudo permission')

    net_obj = Network()
    interface = net_obj.get_interface()
    client_mac = input('\nwhat is your MAC address? ')
    if interface == 'None':
        return -1
    # scanning for networks
    net_mac = net_obj.scanning_networks(False)
    if net_mac == 'None':
        return -1

    # deauthentication
    deauthentication_packet(interface, net_mac, client_mac) # do this with thread

    net_obj.off()


if __name__ == '__main__':
    print('start EVIL TWIN defence...')

    start_defence()
    ans = input('do you want to scan again? [y/n] ')
    while ans == 'y':
        start_defence()
        ans = input('do you want to scan again? [y/n] ')

    print('\nfinish defence')
