#!/usr/bin/env python
"""
This script generates the big ass case statement used in
ssd1306_8x64bit_driver.py for addressing the chars on the display.
"""

f  = open('bigass_case_statement.txt', 'w')

    
index = 64
for char_counter in range(128):
    if char_counter == 0:
        f.write('if')
    else:
        f.write('elif')
    f.write(' char_counter == ' + str(char_counter) + ':\n')
    f.write('    char_buffer.next = val' + str(char_counter/16)+'_buffer[' + str(index) +':'+str(index-4) + ']\n')
    if index == 4:
        index = 64
    else:
        index = index - 4
   
    
f.close()
