import sys
import math
import struct

_p = lambda x: struct.unpack('f', x)[0]
_u = lambda x: struct.pack('b', (round(x)+0x80)%0x100-0x80)

if len(sys.argv) != 2:
    sys.exit(1)

filename = sys.argv[1]

enc = open(filename + '.enc', 'rb').read()

"""
#bs = open(filename + '.dec', 'wb')

ran = [int(x) for x in sys.argv[2].split('-')]
for rad in range(ran[0],ran[1]):
    key = math.radians(rad)
    tmp=''
    for i in range(0, min(len(enc),0x40), 8):
        _x, _y = _p(enc[i:i+4]), _p(enc[i+4:i+8])
        tmp+=(_u(_x * math.cos(key) + _y * math.sin(key)) + _u(-_x * math.sin(key) + _y * math.cos(key)))
    print str(rad)+':'+tmp
    
key = math.radians(int(raw_input('>>')))
for i in range(0, len(enc), 8):
    _x, _y = _p(enc[i:i+4]), _p(enc[i+4:i+8])
    bs.write(_u(_x * math.cos(key) + _y * math.sin(key)) + _u(-_x * math.sin(key) + _y * math.cos(key)))
"""

for rad in range(360):
    key = math.radians(rad)
    dec = open('dec/'+str(rad)+'_'+filename, 'wb')
    for i in range(0, len(enc), 8):
        _x, _y = _p(enc[i:i+4]), _p(enc[i+4:i+8])
        dec.write(_u(_x * math.cos(key) + _y * math.sin(key)) + _u(-_x * math.sin(key) + _y * math.cos(key)))
    
