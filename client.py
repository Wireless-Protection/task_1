from  scapy.all import *


clients_dict = dict()


def sniff_network(pkt):
    print('sniff clients')

 
class Client:
    def __init__(self):
        self.net = 'client'
