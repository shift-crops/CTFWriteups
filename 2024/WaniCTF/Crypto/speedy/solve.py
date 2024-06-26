#!/usr/bin/env python3
from sc_expwn import *
from cipher import MyCipher
from Cryptodome.Util.Padding import *

def split_km(c):
    c = list(map(lambda x: split_n(x, 8), split_n(c, 16)))

    k = list(map(lambda x: x[0], c))
    m = b''.join(list(map(lambda x: x[1], c)))
    return k,m

def main():
    ct = b'"G:F\xfe\x8f\xb0<O\xc0\x91\xc8\xa6\x96\xc5\xf7N\xc7n\xaf8\x1c,\xcb\xebY<z\xd7\xd8\xc0-\x08\x8d\xe9\x9e\xd8\xa51\xa8\xfbp\x8f\xd4\x13\xf5m\x8f\x02\xa3\xa9\x9e\xb7\xbb\xaf\xbd\xb9\xdf&Y3\xf3\x80\xb8'
    # ct = b'\x0f\x99\x84\xaa\xbd\xca\xd0"\xe7\x05\xdd\x9e,\xf8\x0c\x19O\xae\xa5\xcc-I0\xd9\xe7{\xc8\x85[\xfb\t9\xce\x9fh\x89f\xb2\xbe\x88\x97\xa1\x0e(\x11D\x8b\xe2\xd0\xc3"E\x06\xb0\xec\xd5\x89\x94Y\x9d\xec\x9e6\x8e'
    k,m = split_km(ct)

    x0 = int.from_bytes(k[0])
    x1 = int.from_bytes(k[1])
    y0 = XORShift.decLeft(x1 ^ rol(x0, 24, 64), 16) ^ x0

    cipher = MyCipher(x0, y0)
    _, pt = split_km(cipher.encrypt(m))
    secret = unpad(pt, 8)
    print(secret)

if __name__ == '__main__':
    main()
