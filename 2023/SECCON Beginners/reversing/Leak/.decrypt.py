#!/usr/bin/env python3

import sys

def main():
    in_data_flag = open('flag.enc', 'rb').read()
    flag = enc_dec(in_data_flag, b'KEY{th1s_1s_n0t_f1ag_y0u_need_t0_f1nd_rea1_f1ag}')
    sys.stdout.buffer.write(flag)

def enc_dec(in_data, key):
    tbl = [0]*0x100
    for i in range(0x100):
        tbl[i] = (i+0x35) & 0xff

    swp = 0
    for i in range(0x100):
        swp = (swp + key[i % len(key)] + tbl[i]) & 0xff
        tbl[i], tbl[swp] = tbl[swp], tbl[i]

    swp = [0,0]
    out_data = []
    for c in in_data:
        swp[1] += tbl[swp[0]+1]
        swp[0] += 1
        swp[0] &= 0xff
        swp[1] &= 0xff
        tbl[swp[0]], tbl[swp[1]] = tbl[swp[1]], tbl[swp[0]]
        out_data += [c ^ tbl[(tbl[swp[0]] + tbl[swp[1]]) & 0xff]]

    return bytes(out_data)

if __name__ == '__main__':
    main()
