import socket

rhp     = ("adctf2014.katsudon.org",43010)

code93 = {'101011110':'ST'}
code93.update({'100010100':'0','101001000':'1','101000100':'2','101000010':'3','100101000':'4','100100100':'5','100100010':'6','101010000':'7','100010010':'8','100001010':'9'})
code93.update({'110101000':'A','110100100':'B','110100010':'C','110010100':'D','110010010':'E','110001010':'F','101101000':'G','101100100':'H','101100010':'I','100110100':'J','100011010':'K','101011000':'L','101001100':'M','101000110':'N','100101100':'O','100010110':'P','110110100':'Q','110110010':'R','110101100':'S','110100110':'T','110010110':'U','110011010':'V','101101100':'W','101100110':'X','100110110':'Y','100111010':'Z'})
code93.update({'100101110':'-','111010100':'.','111010010':' ','111001010':'$','101101110':'/','101110110':'+','110101110':'%','100100110':'_$','111011010':'_%','111010110':'_/','100110010':'/+'})

nc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
nc.settimeout(5.0)
nc.connect(rhp)

for i in range(10):
    code = (nc.recv(0x3)+nc.recv(0xc0)).replace('\x20','0').replace('\xe2\x96\x90','01').replace('\xe2\x96\x8c','10').replace('\xe2\x96\x88','11')
    if(code93[code[0:9]]=='ST'): 
        msg=''
        for i in range(9,len(code),9):
            c = code93[code[i:i+9]]
            if(c=='ST'):
                break
            else:
                print code[i:i+9]+' : '+c
                msg+=c[0]

    print 'Data: '+msg[:-2]+'\n'
    nc.sendall(msg[:-2]+'\n')

print nc.recv(0x30)
nc.close()