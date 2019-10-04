from XORShift import Decrypt

flag=map(ord,'712249146f241d31651a504a1a7372384d173f7f790c2b115f47'.decode('hex'))
dec = Decrypt(1)

i = len(flag)-1
while(i>=0):
    flag[i] = dec.decXORShift_R(int(flag[i]),1)
    flag[i] = dec.decXORShift_R(flag[i],2)
    flag[i] = dec.decXORShift_R(flag[i],3)
    flag[i] = dec.decXORShift_R(flag[i],4)
    if(i>0):
        flag[i] ^= flag[i-1]
    i-=1

print ''.join(map(chr,flag))

raw_input('Press any key to exit...')
