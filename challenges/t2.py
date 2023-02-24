from scapy.all import *
import time,datetime

iface = sys.argv[1] if len(sys.argv) > 1 else "hwsim0"

FLAG=b'FLAG-CENSORED'

def send_res(addr1):
    global FLAG
    addr2=b"22:22:22:22:22:22"
    addr3=b"33:33:33:33:33:33"

    packet = RadioTap()\
        /Dot11(type=0, subtype=8, addr1=addr1, addr2=addr2, addr3=addr3)\
        /Dot11Beacon(cap='ESS') \
        /Dot11Elt(ID='SSID',info=FLAG, len=len(FLAG))

    sendp(packet, iface=iface, verbose=0)

def detect_deauth_attack(pkt):
    if pkt.haslayer(Dot11Deauth):
        time=datetime.datetime.today()
        addr2 = str(pkt.addr2)
        print(f"{time} deauth against mac: {addr2}")

        if addr2 == 'aa:aa:aa:aa:aa:aa':
            send_res(addr2)

sniff(iface=iface,prn=detect_deauth_attack,count=0)