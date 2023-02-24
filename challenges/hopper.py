# -*- coding: UTF-8 -*-
import sys
import time
from scapy.all import *
from multiprocessing import Process, Manager
from functools import partial
import secrets

interface="wlan9"

client="dd:dd:dd:dd:dd:dd"
bssid="ee:ee:ee:ee:ee:ee"

def lfsr(taps, deg, seed):
  period = math.pow(2, deg)
  value = seed
  it = 0
  while it < period:
    bit = 0
    for tap in taps:
      if len(tap):
        element = 1
        for k in tap:
          if not ( (value>>k) & 1):
            element = 0
            break
      else:
        element = 0
      bit ^= element
    bit &= 1
    value = (value >> 1) | (bit << (deg-1))
    it += 1
    yield value

def sniffAP(S, p):
  advance = False
  if p.addr2 == client and hasattr(p.payload, 'load'):
    print("STATE",S[0])
    incoming = p.payload.load
    msg = "🌝"*S[0]
    if S[0] == 1:
      if int(incoming) != S[2]: #fail
        msg = "☠️ "
        S[0] = 0
      else:
        S[0] = 2
    elif S[0] % 2 == 1:
        if int(incoming) != S[2]: #fail
            msg = "☠️ "
            S[0] = 0
        else:
            advance = True

    #send acknowledge
    packet = RadioTap() / \
             Dot11(type=2,
                   subtype=0,
                   addr1=client,
                   addr2=bssid,
                   addr3=bssid) / ("|||" + msg)
    sendp(packet, iface=interface)

    if advance:
        S[0] += 1

def recv(S):
 sniff(iface=interface, prn=partial(sniffAP, S))

channels = [1,2,3,4,5,6,7,8,9,10,11,36,40,44,48,52,56,60,100,104,108,112,116,120,124,128,132,136,140,149,153,157,161,165,171,176]

def sm(S):
  PRNG = lfsr(([0],[3]), 32, S[1])
  last_chan = 0
  while True:
    time.sleep(1)
    msg = "👾 %s 👾"% " ".join(str(x) for x in S[3:])
    transmit = True
    if S[0] == 0:
      os.system("iw dev %s set channel %d; echo $? > /tmp/switch" % (interface, 1))
      N=16
      S[1] = secrets.randbelow(1<<N)
      PRNG = lfsr(([0],[3]), N, S[1])
      for i in range(5):
        S[3+i] = next(PRNG)
      S[2] = next(PRNG)
      msg = "👾 %s 👾"% " ".join(str(x) for x in S[3:])
      S[0] = 1
    elif S[0] >= 20:
      msg = "flag{}"
      #S[0] = 0
    else:
      # Begin frequency hopping protocol
      if S[0] % 2 == 0:
        value = next(PRNG)
        chan = channels[value % len(channels)]
        os.system("iw dev %s set channel %d" % (interface, chan))
        last_chan = chan
        msg = "👾  Beep 👾  Boop 👾 "
        S[2] = next(PRNG) #next challenge
        S[0] += 1
      elif S[0] != 1:
        transmit = False

    if transmit:
      packet = RadioTap() / \
             Dot11(type=2,
                   subtype=0,
                   addr1=client,
                   addr2=bssid,
                   addr3=bssid) / ("|||" + msg)
      sendp(packet, iface=interface)

if __name__ == '__main__':
  manager = Manager()
  s = manager.list()
  s.append(0)
  s.append(0)

  s.append(0)

  s.append(0)
  s.append(0)
  s.append(0)
  s.append(0)
  s.append(0)

  p = Process(target=recv, args=(s,))
  p.start()
  sm(s)
  p.join()
