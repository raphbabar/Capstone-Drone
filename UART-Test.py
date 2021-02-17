import numpy as np
import serial
import time
import sys
from time import sleep
import struct
import SBUS

# //////////////////////////////////////////////////
# ///////// BEFORE STARTING, READ THIS: ////////////
# //////////////////////////////////////////////////
# to use UART0 (/dev/ttyAMA0), add this line of code
# in config.txt under "[all]" then reboot
# CODE: dtoverlay=pi3-miniuart-bt

# Serial Port follow the SBUS Protocol based on "https://github.com/bolderflight/SBUS"
# SBUS protocol uses an inverted serial logic with a baud rate of 100000,
#      8 data bits, even parity and 2 stop bits
# SBUS packet is 25 bytes long. Refer to GitHub link to view the channel mapping
ser = serial.Serial (
        port='/dev/ttyAMA0',
        baudrate = 100000,
        parity=serial.PARITY_EVEN,
        stopbits=serial.STOPBITS_TWO,
        bytesize=serial.EIGHTBITS,
        )

try:
    ch0_data  = 1055 ; ch1_data  = 0; ch2_data  = 0; ch3_data  = 0; ch4_data  = 0; \
    ch5_data  = 0; ch6_data  = 0; ch7_data  = 0; ch8_data  = 0; ch9_data  = 0; \
    ch10_data = 0; ch11_data = 0; ch12_data = 0; ch13_data = 0; ch14_data = 0; \
    ch15_data = 1000

    # use to send command
    while True:
        #send byte array
        array = SBUS.frameProcess( ch0_data, ch1_data, ch2_data, ch3_data, ch4_data, \
                              ch5_data, ch6_data, ch7_data, ch8_data, ch9_data, \
                              ch10_data, ch11_data, ch12_data, ch13_data, ch14_data, \
                              ch15_data)
        
        for i in range(len(array)):
            ser.write(struct.pack('>B',array[i]))
            #print(array[i], end = '') 
        #print("\n")    
        time.sleep(0.1) # send command sendArray every 0.1 seconds for test
        
except Exception as e:
    print(e)

finally:
    ser.close()






