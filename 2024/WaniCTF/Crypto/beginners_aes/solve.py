#!/usr/bin/env python3
from Cryptodome.Util.Padding import unpad
from Cryptodome.Cipher import AES
import hashlib
from itertools import product

def main():
    enc = b'\x16\x97,\xa7\xfb_\xf3\x15.\x87jKRaF&"\xb6\xc4x\xf4.K\xd77j\xe5MLI_y\xd96\xf1$\xc5\xa3\x03\x990Q^\xc0\x17M2\x18'
    flag_hash = '6a96111d69e015a07e96dcd141d31e7fc81c4420dbbef75aef5201809093210e'

    for k,i in product(range(0x100), repeat=2):
        key = b'the_enc_key_is_'+ k.to_bytes()
        iv = b'my_great_iv_is_'+ i.to_bytes()

        try:
            cipher = AES.new(key, AES.MODE_CBC, iv)
            flag = unpad(cipher.decrypt(enc), 16)
        except:
            pass
        else:
            if hashlib.sha256(flag).hexdigest() == flag_hash:
                print(k, i, flag)
                break

if __name__ == '__main__':
    main()

