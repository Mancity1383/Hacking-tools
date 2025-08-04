import scapy.all as scapy
import optparse
import re

def scan(ip):

    #using arping for get the MAC of the IP
    # scapy.arping(ip)


    arp_request = scapy.ARP(pdst = ip)
    broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
    arp_broadcast = broadcast/arp_request

    answer , unanswered = scapy.srp(arp_broadcast,timeout=1)
    MAC_Address_and_IP = dict()

    for answer_item in answer:
        extract_ip = answer_item[1].psrc
        extract_mac = answer_item[1].hwsrc
        # extract_mac = re.findall(r'\w\w:\w\w:\w\w:\w\w:\w\w:\w\w',str(answer_item))[2]
        # extract_ip = re.findall(r'\d+.\d+.\d+.\d+',str(answer_item))[0]
        if extract_ip not in MAC_Address_and_IP.keys():
            MAC_Address_and_IP[extract_ip] = extract_mac

    for num,data in enumerate(MAC_Address_and_IP.keys()):
        print(f'{num+1}. IP: {data}, MAC : {MAC_Address_and_IP[data]}')

    #get information about ARP class
    # scapy.ls(scapy.ARP())

    #get full data about the varaiable
    # arp_broadcast.show()


parser = optparse.OptionParser()
parser.add_option('-t','--target',dest='ip',help='Choose the Target for scan')
(options,args) = parser.parse_args()

ip = options.ip

scan(ip)