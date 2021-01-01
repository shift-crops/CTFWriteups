#!/bin/sh

qemu-system-i386 -curses -m 64 -L . -fda BBS.IMG -boot a -serial tcp::5000,server -monitor tcp::4296,server,nowait -s
