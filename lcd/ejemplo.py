#!/usr/bin/env python
import lcddriver
from time import *

textos = ['control de lcd i2c','por Luis Borbolla','fecha 2016-02-05','qwerty','asdfg','qwertyuiopasdfgh',]
lcd = lcddriver.lcd()

try:
    for i in range(4):
        for texto in textos:
            lcd.lcd_display_string(texto, i+1)
            sleep(1)
            lcd.lcd_clear()
except KeyboardInterrupt:
    lcd.lcd_clear()
lcd.lcd_display_string('Pantalla en stand-by', 1)
lcd.lcd_display_string('Introduce comando', 2)
lcd.lcd_display_string('desde computadora', 3)
lcd.lcd_display_string('realizada borbolla', 4)
