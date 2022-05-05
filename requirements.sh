#!/bin/sh

echo start installation evil attack dependency packets...
sudo apt update                 # ????????
sudo apt-get update             # all
sudo apt install net-tools      # ifconfig
# sudo pip install scapy
sudo apt install python3-scapy  # also can be use without python3
# iwconfig ???

sudo apt-get install hostapd
sudo apt-get install dnsmasq
echo please check there are all packets install succefully