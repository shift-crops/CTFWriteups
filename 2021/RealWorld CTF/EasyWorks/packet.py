#!/usr/bin/env python3
from scapy.all import *
import random
import re

def packet_callback(packet):
    print(packet.show)
    if packet[TCP].flags == 'S':
        connect(packet)
    elif packet[TCP].flags == 'PA':
        response(packet)
    elif re.match(r'[FR]', str(packet[TCP].flags)) is not None:
        disconnect(packet)

def connect(packet):
    r_ip  = packet[IP]
    r_tcp = packet[TCP]

    sport = r_tcp.dport
    dport = r_tcp.sport
    ack_num = r_tcp.seq+1
    seq_num = random.randint(0,10000000)

    t_ip  = IP(dst=r_ip.src, src=r_ip.dst)
    # t_tcp = TCP(sport=sport, dport=dport, flags="SA", seq=seq_num, ack=ack_num)
    # syn_ack = t_ip/t_tcp
    # sr1(syn_ack)

    t_tcp = TCP(sport=sport, dport=dport, flags="SAFU", seq=seq_num, ack=ack_num)
    psh = t_ip/t_tcp
    send(psh)

    seq_num = random.randint(0,10000000)
    t_tcp = TCP(sport=sport, dport=dport, flags="SA", seq=seq_num, ack=ack_num)
    payload = b'a'*4000
    syn_ack = t_ip/t_tcp/payload
    send(syn_ack)

def response(packet):
    r_ip  = packet[IP]
    r_tcp = packet[TCP]
    r_raw = packet[Raw]

    sport = r_tcp.dport
    dport = r_tcp.sport
    seq_num = r_tcp.ack
    ack_num = r_tcp.seq + len(r_raw.load)

    t_ip  = IP(dst=r_ip.src, src=r_ip.dst)
    t_tcp = TCP(sport=sport , dport=dport ,flags='A', seq=seq_num, ack=ack_num)
    ack = t_ip/t_tcp
    send(ack)

    '''
    t_tcp = TCP(sport=sport, dport=dport, flags='PAU', seq=seq_num, ack=ack_num, urgptr=0)
    payload = b'b'*1000
    psh = t_ip/t_tcp/payload
    send(psh)
    '''

def disconnect(packet):
    r_ip  = packet[IP]
    r_tcp = packet[TCP]

    t_ip  = IP(dst=r_ip.src, src=r_ip.dst)
    t_tcp = TCP(sport=r_tcp.dport , dport=r_tcp.sport ,flags=r_tcp.flags, seq=r_tcp.ack, ack=r_tcp.seq+1)
    send(t_ip/t_tcp)

if __name__=='__main__':
    sniff(prn=packet_callback, filter='tcp and dst port 4660')

