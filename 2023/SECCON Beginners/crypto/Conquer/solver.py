#!/usr/bin/env python3

from Crypto.Util.number import *

def main():
    key = 364765105385226228888267246885507128079813677318333502635464281930855331056070734926401965510936356014326979260977790597194503012948
    cipher = 92499232109251162138344223189844914420326826743556872876639400853892198641955596900058352490329330224967987380962193017044830636379

    length = cipher.bit_length()
    length = ((length//8+1)*8 if length%8 else length) -1

    '''
    def ROL(bits, N):
        for _ in range(N):
            bits = ((bits << 1) & (2**length - 1)) | (bits >> (length - 1))
        return bits
    '''

    def ROR(bits, N):
        for _ in range(N):
            bits = (bits >> 1) | ((bits&1) << (length - 1))
        return bits

    for _ in range(32):
        cipher ^= key
        key = ROR(key, pow(cipher, 3, length))

    flag = cipher ^ key
    print(long_to_bytes(flag).decode())

if __name__ == '__main__':
    main()
