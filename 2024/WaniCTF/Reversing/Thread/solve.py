#!/usr/bin/env python3

split_n = lambda text,n: [text[x:x+n] for x in range(0, len(text), n)]

def main():
    enc_flag = open('enc_flag', 'rb').read()
    enc_flag = map(lambda x: int.from_bytes(x, 'little'), split_n(enc_flag, 4))

    calc = [lambda x: x//3, lambda x: x-5, lambda x: x^0x7f]
    flag = ''
    for i, e in enumerate(enc_flag):
        for j in range(2, -1, -1):
            e = calc[(i+j) % 3](e)
        flag += chr(e)
    print(flag)

if __name__ == '__main__':
    main()
