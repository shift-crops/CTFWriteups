from PIL import Image
from itertools import product
from sqrd import Decode

side_len = 29

img = Image.open('qrgarden.png','r')
img = img.convert("RGB")
size = img.size

for j,i in product(range(size[1]/(29*3)),range(size[0]/(29*3))):
    code=""
    for y in range(29):
         for x in range(29):
            code += "X" if img.getpixel((i*(29*3)+x*3,j*(29*3)+y*3))==(0,0,0) else " "
            if(x==28):
                code += '\n'

    msg=Decode(code)
    open('result.txt','a').write('(%3d,%3d): %s\n' % (i,j,msg))

    if 'ADCTF' in msg:
        print '(%3d,%3d): %s' % (i,j,msg)
