#!/usr/bin/env python3

def main():
    dump = open('flag.dump', 'rb').read()
    dump = [dump[:0x60], dump[0x60:0x60+0x40], dump[0xa0:]]

    flag = ''
    for i in range(0x30+1):
        flag += chr(dump[i%3][i//3*4])

    print(flag)

if __name__ == '__main__':
    main()
