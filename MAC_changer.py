import subprocess
import optparse
import time
import re

def getArument():
    parser = optparse.OptionParser()

    parser.add_option('-i','--interface',dest='interface',help='Choose the name of device for change MAC Address')
    parser.add_option('-m','--mac-address',dest='mac_address',help='Choose the  MAC Address for changing to')
    (options,args) = parser.parse_args()

    if not options.interface :
        parser.error('[-] Please Choose Device')
    elif not options.mac_address :
        parser.error('[-] Please Choose New Mac Address')

    return options

def changeMacAddress(interface,mac_address):

    print(f"[+] Changing MAC address of {interface} to {mac_address}")
    #using second form of call (More Secure)
    subprocess.call(['ip','link','set','dev',interface,'down'])
    subprocess.call(['ip','link','set','dev',interface,'address',mac_address])
    subprocess.call(['ip','link','set','dev',interface,'up'])

def validateNewMacAddress(interface,mac_address):
    output = subprocess.check_output(['ip','link','show','dev',interface]).decode()
    match = re.search(r'\w\w:\w\w:\w\w:\w\w:\w\w:\w\w',output)
    if match :
        new_mac_addr = match.group(0)
        if new_mac_addr == mac_address :
            print('[+] Mac Address changed.')
            return new_mac_addr
    else : 
        print("[-] Couldn't find MAC address")
        return None


# using ifconfig

# subprocess.call("sudo ifconfig eth0 down",shell=True)
# time.sleep(1)
# subprocess.call("sudo ifconfig eth0 hw ether 00:44:11:22:33:55",shell=True)
# time.sleep(1)
# subprocess.call("sudo ifconfig eth0 up",shell=True)
# time.sleep(1)
# subprocess.call("ip link show ",shell=True)

#using ip
# subprocess.call(f"ip link set dev {interface} down",shell=True)
# subprocess.call(f"ip link set dev {interface} address {mac_address}",shell=True)
# subprocess.call(f"ip link set dev {interface} up",shell=True)
# time.sleep(1)
# subprocess.call(f"ip link show dev {interface}",shell=True)

options = getArument()
changeMacAddress(options.interface,options.mac_address)
new_mac_address = validateNewMacAddress(options.interface,options.mac_address)
print(f'[+] New Mac Address : {new_mac_address}')