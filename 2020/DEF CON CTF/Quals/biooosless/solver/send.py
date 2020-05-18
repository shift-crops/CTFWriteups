#!/usr/bin/env python3
# (./send.py; cat) | nc biooosless.challenges.ooo 6543

import base64
import os

fname = './patch.bin'

print(hex(os.path.getsize(fname)))

data = open(fname, 'rb').read()
print(base64.b64encode(data).decode('utf8'))

# OOO{dont_make_fun_of_noobs_that_cant_read_from_floppies_it_aint_that_easy}
