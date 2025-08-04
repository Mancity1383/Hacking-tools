import scapy.all as scapy
from scapy.layers import http
def sniff(interface):
    print('[+] Program started. ')
    scapy.sniff(iface=interface,store=False,prn=proccess_sniff_packet)

def proccess_sniff_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        if 'microsoft' not in packet[http.HTTPRequest].Host.decode() :
            host = packet[http.HTTPRequest].Host.decode()
            path = packet[http.HTTPRequest].Path.decode()
            print(f'[+] HTTP request : {host}{path}')

sniff('eth0')