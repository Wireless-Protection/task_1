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
from client import Client


def start_attack():
    print('start EVIL TWIN attack...')
    # if os.geteuid():
    #     sys.exit('need sudo permission')

    net_obj = Network()
    net_attack = net_obj.scanning_network()
    clinet_obj = Client()

    net_obj.off()
    print('done')


if __name__ == '__main__':
    start_attack()


# def start_attack():
#     print('start EVIL TWIN attack...')
#     if os.geteuid():
#         sys.exit('need sudo permission')
    
#     net_card_name = input('insert your network card name: ')
#     # need to check if the net_card is exist
#     os.popen('iwconfig').read()         # check how to use it 
    
#     # realy start the attack
#     change_monitor(net_card_name, 'monitor')
    
#     # using thread and wait for the thread join
#     # network_list = scanning_network(net_card_name)
#     # network = choose_network_to_attack(network_list)      # need to do

#     # using thread and wait for the thread join
#     # client = scanning_clients(network)      # need to do
#     # attack_client(client)       # need to do
    
#     # end the attack
#     change_monitor(net_card_name, 'managed')