~~~ the truth is out there ~~~

Welcome to Turtles WiFi Challenges - february 2023
now with UFOs 🛸, balloons 🎈, & more turtles 🐢!

Challenges can be solved individually, no pivot this time.
Extra points for solving the challenges with one .py / scapy one-liners!
These are network-challenges - No need to try to gain root
or pivot into other namespaces ~~ Good luck & happy scapy!

# challenge 1

a wifi client is sending out wifi beacons with an ssid of
`feb-turtle-intro` - can you read the packet info?

# challenge 2

🛸🛸🛸 tic-tac-foe? (see wlan8)

# challenge 3

t2.py is running on another machine,
see if you can decrypt the packets

# challenge 4

🛸🛸🛸 kenneth, what's the frequency? (see wlan10)

# challenge 5

t3.py is sending some weird data, what is this?...

# challenge 6

t4.py see if you can talk to it & make it send you the flag.
use this as psk to connect to the network & continue the challs

# tips
🛸 Be patient, scapy load time can be slow
🛸 files are under /mnt
🛸 tcpdump can be run on hwsim0  or an interface
🛸 see about monitor mode below
🛸 use snapshots, example start scapy interactive & save state

#### list interfaces:
iw dev

hwsim0 will sniff everything, use the other interaces
in monitor mode to inject packets.

#### to enable monitor mode on an interface:

ip link set dev wlan3 down
iw dev wlan3 set type monitor
ip link set dev wlan3 up
iw dev wlan3 set channel $CHANNEL
