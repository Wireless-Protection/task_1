#!/bin/sh

service NetworkManager start
service NetworkManager start
service hostapd stop
service apache2 stop
service dnsmasq stop
service rpcbind stop
killall dnsmasq
killall hostapd
# rm -f build/hostapd.conf
# rm -f build/dnsmasq.conf
systemctl enable systemd-resolved.service
systemctl start systemd-resolved
# rm -rf build/
ifconfig ${INTERFACE} down
iwconfig ${INTERFACE} mode managed
ifconfig ${INTERFACE} up
ifconfig ${SECOND_INTERFACE} down
iwconfig ${SECOND_INTERFACE} mode managed
ifconfig ${SECOND_INTERFACE} up
service network-manager restart