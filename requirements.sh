#!/bin/sh

echo start installation evil attack dependency packets...
apt update
apt-get update             # all
apt install net-tools      # ifconfig

apt install python3-pip
apt install python3-scapy  # also can be use without python3

# apt-get install hostapd
# apt-get install dnsmasq
apt-get install hostapd dnsmasq apache2 -y

echo please check there are all packets install succefully