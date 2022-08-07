ip link set ${INTERFACE} down

ifconfig ${INTERFACE} up 192.168.0.1 netmask 255.255.255.0
route add - net 192.168.0.0 netmask 255.255.255.0 gw 192.168.0.1
ip link set ${INTERFACE} up

systemctl stop systemd-resolved
# ss -lp "sport = :domain"

iptables --table nat --append POSTROUTING --out-interface ${SECOND_INTERFACE} -j MASQUERADE
iptables --append FORWARD --in-interface ${INTERFACE}  -j ACCEPT

echo 1 > /proc/sys/net/ipv4/ip_forward
#  or
# sysctl net.ipv4.ip_forward=1
# for checking ->
sysctl net.ipv4.ip_forward

dnsmasq -C build/dnsmasq.conf
hostapd build/hostapd.conf -B