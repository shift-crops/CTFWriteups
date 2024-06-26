#!/usr/bin/env python3
import hashlib
import string

def make_revdict():
    d = dict()
    for c in string.printable:
        x = hashlib.md5(str(ord(c)).encode()).hexdigest()
        d[int(x, 16)] = c
    return d

def main():
    rd = make_revdict()
    enc = list(map(int, open('my_diary_11_8_Wednesday.txt', 'r').read()[1:-1].split(', ')))

    secret = '' 
    for e in enc:
        secret += rd[e]
    print(secret)

if __name__ == '__main__':
    main()

