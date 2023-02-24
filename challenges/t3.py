from scapy.all import *
from threading import Thread, Event
from time import sleep
import codecs
import sys
import datetime
import struct

iface = sys.argv[1] if len(sys.argv) > 1 else "hwsim0"

result = ''
print("# iface=", iface)

def xor(key, data):
    res = ''
    for i in range(len(data)):
        res += chr(ord(data[i])^ord(key[i%len(key)]))
    return res

key="KEY-CENSORED"
text="FLAG-CENSORED"

n=4

while True:
    for i in range(0, n):
        dot11 = Dot11(type=0, subtype=8, addr1='22:22:22:22:22:22',
        addr2='23:23:23:23:23:23', addr3='33:33:33:33:33:33')
        beacon = Dot11Beacon(cap='ESS+privacy')
        d = int(len(text) / n)
        start = i*d
        data=xor(key, text[start:start+d])
        essid = Dot11Elt(ID='SSID',info=key, len=len(key))
        rsn = Dot11Elt(ID='RSNinfo', info=(data))
        print(">>", repr(key), repr(data))

        frame = RadioTap()/dot11/beacon/essid/rsn

        sendp(frame, iface=iface, verbose=0)

        sleep(0.25)
