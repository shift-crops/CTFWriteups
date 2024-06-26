#!/usr/bin/env python3
from mycipher import MyCipher
import hashlib
from itertools import product

def make_token(data1: str, data2: str):
    sha256 = hashlib.sha256()
    sha256.update(data1.encode())
    right = sha256.hexdigest()[:20]
    sha256.update(data2.encode())
    left = sha256.hexdigest()[:12]
    token = left + right
    return token

def main():
    username = 'gureisya'
    ciphertext = '061ff06da6fbf8efcd2ca0c1d3b236aede3f5d4b6e8ea24179'
    ciphertext = bytes.fromhex(ciphertext)

    for m,s,r in product(range(60), range(60), range(11)):
        token = make_token(f'user: {username}, {m}:{s}', f'{username}{r}')

        sha256 = hashlib.sha256()
        sha256.update(token.encode())
        key = sha256.hexdigest()[:32]
        nonce = token[:12]

        cipher = MyCipher(key.encode(), nonce.encode())
        if ciphertext.startswith(cipher.encrypt(b'FLAG{')):
            print(m, s, r, cipher.encrypt(ciphertext)) # decrypt == encrypt
            break

if __name__ == '__main__':
    main()
