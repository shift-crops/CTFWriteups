#!/usr/bin/env python3

'''
message: !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~
encrypted message: caeee087ef3f6c2d4e78b6ae51fad3b2fdf2768a3d5058d0427c10665c4821cf49cce24fc8d404e4f72901fcb475ce9b60dd132cd588479581e5c76792f093340d2b636aedcbe82f4c1f5e9d0be7055da857be06e6ec59bdc1dcc4c95a7f9f
'''

def main():
    flag = decode('6ae6e83d63c90bed34a8be8a0bfd3ded34f25034ec508ae8ec0b7f')
    print(flag)

def decode(enc):
    tbl = [None]*0x100
    
    cvt = bytes.fromhex('eee087ef3f6c2d4e78b6ae51fad3b2fdf2768a3d5058d0427c10665c4821cf49cce24fc8d404e4f72901fcb475ce9b60dd132cd588479581e5c76792f093340d2b636aedcbe82f4c1f5e9d0be7055da857be06e6ec59bdc1dcc4c95a7f9f')
    for i in range(len(cvt)):
        tbl[cvt[i]] = 0x21+i

    dec = []
    for c in bytes.fromhex(enc):
        dec += [tbl[c]]
    return bytes(dec)

if __name__ == '__main__':
    main()
