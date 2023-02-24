# -*- coding: UTF-8 -*-
import sys
import time
from scapy.all import *
from multiprocessing import Process, Manager
from functools import partial

interface="wlan7"

empty="   "

client="dd:dd:dd:dd:dd:dd"
bssid="ee:ee:ee:ee:ee:ee"

def check_game(T, S):
  win = empty

  for i in range(3):
    if T[0][i] == T[1][i] == T[2][i]:
      win = T[0][i]
    if T[i][0] == T[i][1] == T[i][2]:
      win = T[i][0]
    if T[0][0] == T[1][1] == T[2][2]:
      win = T[1][1]
    if T[2][0] == T[1][1] == T[0][2]:
      win = T[1][1]

    selection = possibilities(T)

    if win == empty and (len(selection) > 0):
      return

    msg = "!"

    if win == "👽 " or (len(selection) == 0):
      msg = "Game Over " + win
      T[0] = [empty, empty, empty]
      T[1] = [empty, empty, empty]
      T[2] = [empty, empty, empty]
      S[0] = 0

    if win == "🛸 ":
      msg = "flag{}"
      S[0] = 0

    packet = RadioTap() / \
             Dot11(type=2,
                   subtype=0,
                   addr1=client,
                   addr2=bssid,
                   addr3=bssid) / ("|||" + msg)
    sendp(packet, iface=interface)
  

def sniffAP(T, S, p):
  if p.addr2 == client:
    move = p.payload.load
    msg = "OK"
    print(chr(move[0]))
    if len(move) != 2:
      msg = "NO-"
    else:
      if chr(move[0]) not in 'ABC':
        msg = "NO+"
      if chr(move[1]) not in '0123':
        msg = "NO!"
      if msg == "OK":
        c = move[0]-ord('A')
        r = move[1]-ord('0')
        if (S[0] == 1) and (T[r][c] == empty):
          print("SET T",r, c)
          row = T[r]
          row[c] = "🛸 "
          T[r] = row
          S[0] = 0
          check_game(T, S)
        else:
          msg = "NO@-"+repr(S[0])

    packet = RadioTap() / \
             Dot11(type=2,
                   subtype=0,
                   addr1=client,
                   addr2=bssid,
                   addr3=bssid) / ("|||" + msg)
    sendp(packet, iface=interface)

def recv(T, S):
 sniff(iface=interface, prn=partial(sniffAP, T, S))

def tstate(T):
  o = ""
  o += "   ||  A   |  B  |  C  \n"
  o += "------------------------\n"
  count = 0
  for row in T:
    o += " %d || " % count + " " + row[0] + " | " + row[1] + " | " + row[2]+"\n"
    o += "------------------------\n"
    count += 1
  return o

def possibilities(T):
    l = []
    for i in range(len(T)):
        for j in range(len(T)):
            if T[i][j] == empty:
                l.append((i, j))
    return l

def play_random(T):
  selection = possibilities(T)
  s = random.choice(selection)
  row = T[s[0]]
  row[s[1]] = "👽 "
  T[s[0]] = row
  return T

def sm(T, S):
  while True:
    time.sleep(3)
    if S[0] == 0:
      T = play_random(T)
      S[0] = 1
      check_game(T, S)

    if 1:
      print("state")
      packet = RadioTap() / \
             Dot11(type=2,
                   subtype=0,
                   addr1=client,
                   addr2=bssid,
                   addr3=bssid) / ("|||" + tstate(T))
      sendp(packet, iface=interface)

if __name__ == '__main__':
  manager = Manager()
  d = manager.list()
  s = manager.list()
  s.append(0)
  d.append([empty, empty, empty])
  d.append([empty, empty, empty])
  d.append([empty, empty, empty])
  p = Process(target=recv, args=(d,s))
  p.start()
  sm(d, s)
  p.join()
