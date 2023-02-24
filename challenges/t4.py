from scapy.all import *
import codecs
import sys
import datetime
import re
import os

iface = sys.argv[1] if len(sys.argv) > 1 else "wlan2"
verbose = False

# flag is psk for the ap
def get_flag():
	try:
		d = open(os.path.dirname(__file__)+'/w.conf', 'r').read()
		m = re.findall(r'psk="([^"]+)"', d)
		return 'flag{%s}' % (m[0])
	except:
		return 'flag{test}'

DST_MAC = "44:44:44:44:44:44" # only send response if dst is this mac
FLAG = get_flag()

def send_response(p, info, channel=1):
	addr1=b'23:23:23:23:23:23' #dst_mac = p[Dot11].addr1
	addr2=b'11:11:11:11:11:11' #src_mac = p[Dot11].addr2
	addr3=b'22:22:22:22:22:22' #ap_mac  = p[Dot11].addr3
	AP_RATES = b"\x0c\x12\x18\x24\x30\x48\x60\x6c"
	frame = RadioTap() \
		/Dot11(addr1=addr1, addr2=addr2, addr3=addr3) \
		/Dot11ProbeResp() \
		/Dot11Elt(ID='SSID', info=b"balloon") \
		/Dot11Elt(ID='Rates', info=AP_RATES) \
		/Dot11EltDSSSet(channel=int(channel)) \
		/Dot11EltVendorSpecific(info=info)
		#/Dot11Elt(ID='DSset', info=chr(channel))
		
	if verbose:
		print('SENDING')
		frame.show()

	sendp(frame, iface=iface, verbose=0)
	return

def probes_scanner(p):
	if not (p.haslayer(Dot11ProbeReq) or p.haslayer(Dot11ProbeReq) or p.haslayer(Dot11Beacon)):
	    return

	rssi = p[RadioTap].dBm_AntSignal or 0
	dst_mac = p[Dot11].addr1
	src_mac = p[Dot11].addr2
	ap_mac  = p[Dot11].addr3

	info = f"{rssi:2}dBm, dst={dst_mac}, src={src_mac}, ap_mac={ap_mac}"
	if verbose: print(f"# {info}")
	
	if p.haslayer(Dot11ProbeReq) and dst_mac == DST_MAC:
		info = f"{rssi:2}dBm, dst={dst_mac}, src={src_mac}, ap_mac={ap_mac}"
		ssid = codecs.decode(p.info, 'utf-8')
		index = struct.unpack('<b', p[Dot11Elt:0].info)[0]
		index = int(abs(index) % len(FLAG))

		print(f"ProbeReq: ssid=\"{ssid}\", index={index}")
		info = FLAG[index]
		try:
			send_response(p, str(info), channel=index)
		except:
			print("CC")
			pass

		return

sniff(prn=probes_scanner,iface=iface, count=0)
