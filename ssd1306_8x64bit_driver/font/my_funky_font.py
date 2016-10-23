'''
This script generates a myhdl-rom with my funky characters (0..9..A..F).

format of the chars: 8x8 pixels

input-file: my_funky_fonts.bmp with the graphics for the hex letters.
output_file: funky_font_rom.py with the myHDL-model for our ROM with our font.

'''

from PIL import Image
import numpy as np


# 'my_funky_font.bmp' contains the graphics for the hex letters.
im = Image.open('my_funky_font.bmp')

p = np.array(im)_

font = p[:,:,0]

# we want to use the horizontal mode of the display and prepare
# the graphics accordingly.
for char in range(16):
    print char
content_list = []
# we take the bmp data and generate a list of the ROM-content
for x in range(len(font[0])):
    slice_buffer = font[:,x]
    slice_value = 0
    for y in range(len(slice_buffer)):
        if slice_buffer[y] == 255:
            slice_value += pow(2,y)
    content_list.append(slice_value)
    
# 
f = open('funky_font_rom.py', 'w')

f.write('from myhdl import *\n')

f.write('def rom(dout, addr, CONTENT):\n')

f.write('    @always_comb\n')
f.write('    def read():\n')
f.write('        dout.next = CONTENT[int(addr)]\n')
f.write('    return read\n')

f.write('CONTENT = (')
for i in range(len(content_list)):
    f.write(str(content_list[i]^255))
    if i < len(content_list) -1:
        f.write(',')
    if i % 10 == 0:
        f.write('\n')
f.write(')\n')
f.write('\n')

f.write('dout = Signal(intbv(0)[8:])\n')

f.write('addr = Signal(intbv(0)[7:])\n')
f.write('toVerilog(rom, dout, addr, CONTENT)\n')
