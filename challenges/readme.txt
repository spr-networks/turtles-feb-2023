~~~ the truth is out there ~~~

Welcome to Turtles WiFi Challenges - february 2023
now with UFOs πΈ, balloons π, & more turtles π’!

Challenges can be solved individually, no pivot this time.
Extra points for solving the challenges with one .py / scapy one-liners!
These are network-challenges - No need to try to gain root
or pivot into other namespaces ~~ Good luck & happy scapy!

# challenge 1

a wifi client is sending out wifi beacons with an ssid of
`feb-turtle-intro` - can you read the packet info?

iface: wlan4 or wlan5, channel: 5

# challenge 2

πΈπΈπΈ tic-tac-foe? iface: wlan8

# challenge 3

t2.py is running on another machine,
see if you can decrypt the packets

iface: wlan4 or wlan5, channel: 5

# challenge 4

πΈπΈπΈ kenneth, what's the frequency? iface: wlan10

# challenge 5

t3.py is sending some weird data, what is this?...

iface: wlan4 or wlan5, channel: 5

# challenge 6

t4.py see if you can talk to it on channel 10 & make it send 
you the flag. use this as psk to connect to the network

iface: wlan4 or wlan5, channel: 10

NOTE docker version is running on channel 5

# tips
πΈ Be patient, scapy load time can be slow
πΈ files are under /mnt
πΈ tcpdump can be run on hwsim0  or an interface
πΈ see about monitor mode below
πΈ use snapshots, example start scapy interactive & save state

#### list interfaces:
iw dev

hwsim0 will sniff everything, use the other interaces
in monitor mode to inject packets.

#### to enable monitor mode on an interface:

ip link set dev wlan3 down
iw dev wlan3 set type monitor
ip link set dev wlan3 up
iw dev wlan3 set channel $CHANNEL
