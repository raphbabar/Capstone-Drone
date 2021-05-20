import serial
import time
import sys
import numpy as np
import struct

ser = serial.Serial (
        port='/dev/ttyS0',
        baudrate = 100000,
        parity=serial.PARITY_EVEN,
        stopbits=serial.STOPBITS_TWO,
        bytesize=serial.EIGHTBITS,
        timeout=1   )
#counter=0

while 1:
        #counter = 170
        #print("This is counter ",counter)
        ser.write(240)
        time.sleep(1)

