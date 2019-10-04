enc = 'fmcj\x7f\x38gz\x81hm]mpY|C\x8e'

flag = ''
for i in range(len(enc)):
    flag += chr(ord(enc[i])-i)

print flag
