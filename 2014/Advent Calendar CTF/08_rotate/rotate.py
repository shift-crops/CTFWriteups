import sys
import math
import struct

def encode():
    p = lambda x: struct.pack('f', x)
    u = lambda x: struct.unpack('b', x)[0]
    
    bs = open(filename, 'rb').read()
    enc = open(filename + '.enc', 'wb')

    for i in range(0, len(bs), 2):
        x, y = u(bs[i]), u(bs[i+1])
        enc.write(p(x * math.cos(key) - y * math.sin(key)) + p(x * math.sin(key) + y * math.cos(key)))

def decode():
    p = lambda x: struct.pack('b', (round(x)+0x80)%0x100-0x80)
    u = lambda x: struct.unpack('f', x)[0]

    enc = open(filename + '.enc', 'rb').read()
    bs = open(filename, 'wb')

    for i in range(0, len(enc), 8):
        _x, _y = u(enc[i:i+4]), u(enc[i+4:i+8])
        bs.write(p(_x * math.cos(key) + _y * math.sin(key)) + p(-_x * math.sin(key) + _y * math.cos(key)))


if __name__=='__main__':
    if len(sys.argv) < 4:
        sys.exit(1)

    filename = sys.argv[2]
    key = math.radians(int(sys.argv[3]))

    encode() if sys.argv[1]=='encode' else decode() if sys.argv[1] == 'decode' else 0
