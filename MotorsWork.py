import numpy as np
import serial
import sys
from time import sleep
import struct
import cv2
import RPi.GPIO as GPIO

class SBUS():
    
    def __init__(self, q_snd_com): # Initializing
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(26, GPIO.OUT)
        GPIO.output(26, GPIO.HIGH) #SBUS code control flight controller
        #GPIO.output(26, GPIO.LOW) #For manual mode with controller
        
        # //////////////////////////////////////////////////
        # ///////// BEFORE STARTING, READ THIS: ////////////
        # //////////////////////////////////////////////////
        # to use UART0 (/dev/ttyAMA0), add this line of code
        # in config.txt under "[all]" then reboot
        # CODE: dtoverlay=pi3-miniuart-bt

        # Serial Port follow the SBUS Protocol based on https://github.com/bolderflight/SBUS
        # SBUS protocol uses an inverted serial logic with a baud rate of 100000,
        #      8 data bits, even parity and 2 stop bits
        # SBUS packet is 25 bytes long. Refer to GitHub link to view the channel mapping
        self.ser =  serial.Serial (
                    port='/dev/ttyAMA0',
                    baudrate = 100000,
                    parity=serial.PARITY_EVEN,
                    stopbits=serial.STOPBITS_TWO,
                    bytesize=serial.EIGHTBITS,
                )
        
        self.q_snd_com = q_snd_com # queue receives channel data from Drone control
        self.channel_data_list = [] #channel data
        for i in range(18): # data channel index from 0 to 15 for now. Additional digital channel 17, 18
            self.channel_data_list.append(0)
            
        self.channel_data_sent = [] #channel data
        for i in range(18): # data channel index from 0 to 15 for now. Additional digital channel 17, 18
            self.channel_data_sent.append(0)

    # Deleting (Calling destructor) 
    def __del__(self):
        self.ser.close()

    #///////////////////////////
    # convert_input() reads the betaflight input and converts it into the channel data using linear conversion
    # betaflight range is 1000 to 2000 (input)
    # channel data is 192 to 1792 (output)
    def convert_input(self, betaflight_data):
        if betaflight_data < 1000:
            input = 1000
        elif betaflight_data > 2000:
            input = 2000
        else:
            input = betaflight_data
        channel_data = ((1792-192) / (2000-1000) * (input-1000)) + 192
        return int(channel_data)
    #///////////////////////////

    #///////////////////////////
    # https://www.geeksforgeeks.org/extract-k-bits-given-position-number/?ref=rp
    # Python program to extract k bits from a given 
    # position. 

    # Function to extract k bits from p position  
    # and returns the extracted value as integer 
    def bitExtracted(self, number, k, p):    
        return ( ((1 << k) - 1)  &  (number >> (p-1) ) )
    #///////////////////////////

    #///////////////////////////
    # https://www.geeksforgeeks.org/reverse-bits-positive-integer-number-python/
    # Function to reverse bits of positive   
    # integer number  
    def reverseBits(self, num,bitSize):  
        
         # convert number into binary representation  
         # output will be like bin(10) = '0b10101'  
         binary = bin(num)  
        
         # skip first two characters of binary  
         # representation string and reverse  
         # remaining string and then append zeros  
         # after it. binary[-1:1:-1]  --> start  
         # from last character and reverse it until  
         # second last character from left  
         reverse = binary[-1:1:-1]  
         reverse = reverse + (bitSize - len(reverse))*'0'

         # converts reversed binary string into integer  
         return (int(reverse,2))
    #///////////////////////////

    def set_bit(self, value, bit):
        return value | (1<<bit)

    def clear_bit(self, value, bit):
        return value & ~(1<<bit)
    #///////////////////////////

    def send_command(self):

        while True:
            
            # receive channel data
            self.channel_data_list = self.q_snd_com.get()
            
            print("Channel data before conversion: ", end = '')
            print(self.channel_data_list) 

            self.channel_data_sent[0]  = self.convert_input(self.channel_data_list[0]) # Roll
            self.channel_data_sent[1]  = self.convert_input(self.channel_data_list[1]) # Pitch
            self.channel_data_sent[2]  = self.convert_input(self.channel_data_list[2]) # Yaw
            self.channel_data_sent[3]  = self.convert_input(self.channel_data_list[3]) # Throttle
            self.channel_data_sent[4]  = self.convert_input(self.channel_data_list[4])
            self.channel_data_sent[5]  = self.convert_input(self.channel_data_list[5])
            self.channel_data_sent[6]  = self.convert_input(self.channel_data_list[6])
            self.channel_data_sent[7]  = self.convert_input(self.channel_data_list[7])
            self.channel_data_sent[8]  = self.convert_input(self.channel_data_list[8])
            self.channel_data_sent[9]  = self.convert_input(self.channel_data_list[9])
            self.channel_data_sent[10] = self.convert_input(self.channel_data_list[10])
            self.channel_data_sent[11] = self.convert_input(self.channel_data_list[11])
            self.channel_data_sent[12] = self.convert_input(self.channel_data_list[12])
            self.channel_data_sent[13] = self.convert_input(self.channel_data_list[13])
            self.channel_data_sent[14] = self.convert_input(self.channel_data_list[14])
            self.channel_data_sent[15] = self.convert_input(self.channel_data_list[15])
            self.channel_data_sent[16] = self.channel_data_list[16] # [digital channel [17] stop = 1 when stop button is pressed (start = 0)
            self.channel_data_sent[17] = self.channel_data_list[17] # [digital channel [18] start = 1 when start button is pressed (stop = 0)

            print("Channel data after  conversion: ", end = '')
            print(self.channel_data_sent)
            
            array = self.frameProcess( self.channel_data_sent[0],  self.channel_data_sent[1],  self.channel_data_sent[2],  self.channel_data_sent[3], \
                                  self.channel_data_sent[4],  self.channel_data_sent[5],  self.channel_data_sent[6],  self.channel_data_sent[7],  \
                                  self.channel_data_sent[8],  self.channel_data_sent[9],  self.channel_data_sent[10], self.channel_data_sent[11], \
                                  self.channel_data_sent[12], self.channel_data_sent[13], self.channel_data_sent[14], self.channel_data_sent[15], \
                                  self.channel_data_sent[16], self.channel_data_sent[17]
                                    )
            
            print('Sent array: ', end = '')
            for i in range(len(array)):
                self.ser.write(struct.pack('>B',array[i]))
                print(' ', array[i], end = '')
            print("\n")
        
            sleep(0.007) # send command array once every 7 ms
#///////////////////////////

#///////////////////////////
    def send_command_hard_code(self):
        ch0_data  = 1000; ch1_data  = 1050; ch2_data  = 1100; ch3_data  = 1150; ch4_data  = 1200; \
        ch5_data  = 1250; ch6_data  = 1300; ch7_data  = 1350; ch8_data  = 1400; ch9_data  = 1450; \
        ch10_data = 1500; ch11_data = 1550; ch12_data = 1600; ch13_data = 1650; ch14_data = 1700; \
        ch15_data = 1750
        
        ch0_data = int(16/10 * (ch0_data - 1000) + 192)
        ch1_data = int(16/10 * (ch1_data - 1000) + 192)
        ch2_data = int(16/10 * (ch2_data - 1000) + 192)
        ch3_data = int(16/10 * (ch3_data - 1000) + 192)
        ch4_data = int(16/10 * (ch4_data - 1000) + 192)
        ch5_data = int(16/10 * (ch5_data - 1000) + 192)
        ch6_data = int(16/10 * (ch6_data - 1000) + 192)
        ch7_data = int(16/10 * (ch7_data - 1000) + 192)
        ch8_data = int(16/10 * (ch8_data - 1000) + 192)
        ch9_data = int(16/10 * (ch9_data - 1000) + 192)
        ch10_data = int(16/10 * (ch10_data - 1000) + 192)
        ch11_data = int(16/10 * (ch11_data - 1000) + 192)
        ch12_data = int(16/10 * (ch12_data - 1000) + 192)
        ch13_data = int(16/10 * (ch13_data - 1000) + 192)
        ch14_data = int(16/10 * (ch14_data - 1000) + 192)
        ch15_data = int(16/10 * (ch15_data - 1000) + 192)
        
        #ch0_data = 512
        #ch0_data = self.convert_input(ch0_data)
        #ch1_data = self.convert_input(ch1_data)
        #ch2_data = self.convert_input(ch2_data)
        #ch3_data = self.convert_input(ch3_data)
        #ch4_data = self.convert_input(ch4_data)
        #ch5_data = self.convert_input(ch5_data)
        #ch6_data = self.convert_input(ch6_data)
        #ch7_data = self.convert_input(ch7_data)
        #ch8_data = self.convert_input(ch8_data)
        #ch9_data = self.convert_input(ch9_data)
        #ch10_data = self.convert_input(ch10_data)
        #ch11_data = self.convert_input(ch11_data)
        #ch12_data = self.convert_input(ch12_data)
        #ch13_data = self.convert_input(ch13_data)
        #ch14_data = self.convert_input(ch14_data)
        #ch15_data = self.convert_input(ch15_data)

        # use to send command
        count = 0
        while True:
            #send byte array
            array = self.frameProcess(ch0_data, ch1_data, ch2_data, ch3_data, ch4_data, \
                                  ch5_data, ch6_data, ch7_data, ch8_data, ch9_data, \
                                  ch10_data, ch11_data, ch12_data, ch13_data, ch14_data, \
                                  ch15_data, 0, 0)
            
            count = count + 1
            print (count)
            if count > 500:
                ch4_data = 192
            if count > 1000:
                ch2_data = 1000
                
            #print ('to arm, press a')
            #if keyboard.is_pressed('a'):
                #print('You pressed A')
            #if cv2.waitKey(33) == ord('a'):
                #h2_data = int(ch2_data + 1);
            #print (ch0_data, 'chan 0')
            #ch2_data = int(ch2_data + 1);
            #if ch2_data > 992:
                #ch2_data = 192
            
            for i in range(len(array)):
                self.ser.write(struct.pack('>B',array[i]))
                #print(array[i], end = ' ')
            #print("\n")
                
            #ch0_data = ch0_data + 5
            #if ch0_data > 1700:
                #ch0_data = 1000
        
        time.sleep(0.007) # send command array once every 7 ms
#///////////////////////////

#///////////////////////////
    # frameProcess() reads input for 16 channels and outputs channel data within an array of 25 bytes     
    def frameProcess(self, ch0_data  = 1000, ch1_data  = 1050, ch2_data  = 1100, ch3_data  = 1150, ch4_data  = 1200, \
                           ch5_data  = 1250, ch6_data  = 1300, ch7_data  = 1350, ch8_data  = 1400, ch9_data  = 1450, \
                           ch10_data = 1500, ch11_data = 1550, ch12_data = 1600, ch13_data = 1650, ch14_data = 1700, \
                           ch15_data = 1750, d_ch17 = 0, d_ch18 = 0
                    ):
        header =  0b11110000 
        Start_byte = self.reverseBits(header, 8)

        sbyte_0  = 0; sbyte_1  = 0; sbyte_2  = 0; sbyte_3  = 0; sbyte_4  = 0; sbyte_5  = 0; sbyte_6  = 0; sbyte_7  = 0
        sbyte_8  = 0; sbyte_9  = 0; sbyte_10 = 0; sbyte_11 = 0; sbyte_12 = 0; sbyte_13 = 0; sbyte_14 = 0; sbyte_15 = 0
        sbyte_16 = 0; sbyte_17 = 0; sbyte_18 = 0; sbyte_19 = 0; sbyte_20 = 0; sbyte_21 = 0

        # ////////////////ch_0////////////////
        # first 8 bits
        #print('\nch0_data = ', format(ch0_data, '011b'))
        position = 1 # extract from bit 0.0 to 0.7
        numOfBits = 8 # extract 8 bits
        sbyte_0 = self.bitExtracted(ch0_data, numOfBits, position)
        #sbyte_0 = self.reverseBits(sbyte_0, 8) # 8 bits are ready in byte_0
        #print('sbyte_0 = ', format(sbyte_0, '08b'))

        # other 3 bits
        position = 9 # extract from bit 0.8 to 0.10
        numOfBits = 3 # extract 3 bits
        temp1 = np.ubyte( self.bitExtracted(ch0_data, numOfBits, position) )
        #print('temp1 = ', format(temp1, '08b'))
        #temp2 = np.ubyte(self.reverseBits(temp1, 8))
        #print('temp2 = ', format(temp2, '08b'))
        #sbyte_1 = temp2  # 3 high bits are ready in byte_1
        sbyte_1 = temp1
        #print('sbyte_1 = ', format(sbyte_1, '08b'))

        # ////////////////ch_1////////////////
        # first 5 bits
        #print('\nch1_data = ', format(ch1_data, '011b'))
        position = 1 # extract from bit 1.0 to 1.5
        numOfBits = 5 # extract 5 bits
        temp3 = np.ubyte(self.bitExtracted(ch1_data, numOfBits, position))
        #print('temp3_A = ', format(temp3, '08b'))
        #temp3 = self.reverseBits(temp3, 8) # put the lsb bit first
        #print('temp3_B = ', format(temp3, '08b'))
        temp3 = temp3 >> 3 # lsb starts from sbyte_1 bit 5, 3 high bits are zero
        #print('temp3_C = ', format(temp3, '08b'))
        #sbyte_1 = sbyte_1 | temp3 # set the lowest 5 bits ot sbyte_1, 5 low bits are ready in byte_1
        #print('sbyte_1 = ', format(sbyte_1, '08b'))

        # second 6 bits
        position = 6 # extract from bit 1.6 to 1.10
        numOfBits = 6 # extract 5 bits
        temp4 = np.ubyte( self.bitExtracted(ch1_data, numOfBits, position) )
        #print('temp4 = ', format(temp4, '08b'))
        #temp4 = np.ubyte(self.reverseBits(temp4, 8))
        #print('temp4 = ', format(temp4, '08b'))
        sbyte_2 = temp4  # 6 high bits are ready in byte_2
        #print('sbyte_2 = ', format(sbyte_2, '08b'))

        # ////////////////ch_2////////////////
        # first 2 bits
        #print('\nch2_data = ', format(ch2_data, '011b'))
        position = 1 # extract from bit 2.0 to 2.1
        numOfBits = 2 # extract 2 bits
        temp5 = np.ubyte(self.bitExtracted(ch2_data, numOfBits, position))
        #print('temp5_A = ', format(temp5, '08b'))
        #temp5 = self.reverseBits(temp5, 8) # put the lsb bit first
        #print('temp5_B = ', format(temp5, '08b'))
        temp5 = temp5 >> 6
        sbyte_2 = sbyte_2 | temp5 # set the lowest 2 bits ot sbyte_2, 2 low bits are ready in byte_2
        #print('sbyte_2 = ', format(sbyte_2, '08b'))

        # second 8 bits
        position = 3 # extract from bit 2.2 to 2.9
        numOfBits = 8 # extract 5 bits
        temp6 = np.ubyte( self.bitExtracted(ch2_data, numOfBits, position) )
        #print('temp6 = ', format(temp6, '08b'))
        #temp6 = np.ubyte(self.reverseBits(temp6, 8))
        #print('temp6 = ', format(temp6, '08b'))
        sbyte_3 = temp6  # 8 bits are ready in byte_3
        #print('sbyte_3 = ', format(sbyte_3, '08b'))

        # last 1 bit
        position = 11 # extract bit 2.10
        numOfBits = 1 # extract 2 bits
        temp7 = np.ubyte(self.bitExtracted(ch2_data, numOfBits, position))
        #print('temp7_A = ', format(temp7, '08b'))
        #temp7 = self.reverseBits(temp7, 8) # put the lsb bit first
        #print('temp7_B = ', format(temp7, '08b'))
        sbyte_4 = sbyte_4 | temp7 # set the highest bit of sbyte_4, highest bit is ready in byte_4
        #print('sbyte_4 = ', format(sbyte_4, '08b'))

        # ////////////////ch_3////////////////
        # first 7 bits
        #print('\nch3_data = ', format(ch3_data, '011b'))
        position = 1 # extract from bit 3.0 to 3.6
        numOfBits = 7 # extract 7 bits
        temp8 = np.ubyte(self.bitExtracted(ch3_data, numOfBits, position))
        #print('temp8_A = ', format(temp8, '08b'))
        #temp8 = self.reverseBits(temp8, 8) # put the lsb bit first
        #print('temp8_B = ', format(temp8, '08b'))
        temp8 = temp8 << 1
        sbyte_4 = sbyte_4 | temp8 # set the lowest 7 bits of sbyte_4, 7 low bits are ready in byte_4
        #print('sbyte_4 = ', format(sbyte_4, '08b'))

        # second 4 bits
        position = 8 # extract from bit 3.7 to 3.10
        numOfBits = 4 # extract 4 bits
        temp9 = np.ubyte( self.bitExtracted(ch3_data, numOfBits, position) )
        #print('temp9 = ', format(temp9, '08b'))
        #temp9 = np.ubyte(self.reverseBits(temp9, 8))
        #print('temp9 = ', format(temp9, '08b'))
        sbyte_5 = temp9  # 4 high bits are ready in byte_5
        #print('sbyte_5 = ', format(sbyte_5, '08b'))

        # ////////////////ch_4////////////////
        # first 4 bits
        #print('\nch4_data = ', format(ch4_data, '011b'))
        position = 1 # extract from bit 4.0 to 4.3
        numOfBits = 4 # extract 4 bits
        temp10 = np.ubyte(self.bitExtracted(ch4_data, numOfBits, position))
        #print('temp10_A = ', format(temp10, '08b'))
        #temp10 = self.reverseBits(temp10, 8) # put the lsb bit first
        #print('temp10_B = ', format(temp10, '08b'))
        temp10 = temp10 >> 4
        sbyte_5 = sbyte_5 | temp10 # set the lowest 7 bits of sbyte_5, 7 low bits are ready in byte_5
        #print('sbyte_5 = ', format(sbyte_5, '08b'))

        # second 7 bits
        position = 5 # extract from bit 4.4 to 4.10
        numOfBits = 7 # extract 4 bits
        temp11 = np.ubyte( self.bitExtracted(ch4_data, numOfBits, position) )
        #print('temp11 = ', format(temp11, '08b'))
        #temp11 = np.ubyte(self.reverseBits(temp11, 8))
        #print('temp11 = ', format(temp11, '08b'))
        sbyte_6 = temp11  # 7 high bits are ready in byte_6
        #print('sbyte_6 = ', format(sbyte_6, '08b'))

        # ////////////////ch_5////////////////
        # first 1 bit
        #print('\nch5_data = ', format(ch5_data, '011b'))
        position = 1 # extract bit 5.0
        numOfBits =1 # extract 1 bit
        temp12 = np.ubyte(self.bitExtracted(ch5_data, numOfBits, position))
        #print('temp12_A = ', format(temp12, '08b'))
        #temp12 = self.reverseBits(temp12, 8) # put the lsb bit first
        #print('temp12_B = ', format(temp12, '08b'))
        temp12 = temp12 >> 7
        sbyte_6 = sbyte_6 | temp12 # set the lowest  bit of sbyte_6, lowest bit is ready in byte_6
        #print('sbyte_5 = ', format(sbyte_5, '08b'))

        # second 8 bits
        position = 2 # extract from bit 5.1 to 5.8
        numOfBits = 8 # extract 4 bits
        temp13 = np.ubyte( self.bitExtracted(ch5_data, numOfBits, position) )
        #print('temp13 = ', format(temp13, '08b'))
        #temp13 = np.ubyte(self.reverseBits(temp13, 8))
        #print('temp13 = ', format(temp13, '08b'))
        sbyte_7 = temp13  # 8 bits are ready in byte_7
        #print('sbyte_7 = ', format(sbyte_7, '08b'))

        # last 2 bit2
        position = 10 # extract bit 5.9
        numOfBits = 2 # extract 2 bits
        temp14 = np.ubyte(self.bitExtracted(ch5_data, numOfBits, position))
        #print('temp14_A = ', format(temp14, '08b'))
        #temp14 = self.reverseBits(temp14, 8) # put the lsb bit first
        #print('temp14_B = ', format(temp14, '08b'))
        sbyte_8 = sbyte_8 | temp14 # set two highe bits of sbyte_8
        #print('sbyte_8 = ', format(sbyte_8, '08b'))

        # ////////////////ch_6////////////////
        # first 6 bits
        #print('\nch6_data = ', format(ch6_data, '011b'))
        position = 1 # extract from bit 6.0 to 6.5
        numOfBits = 6 # extract 6 bits
        temp15 = np.ubyte(self.bitExtracted(ch6_data, numOfBits, position))
        #print('temp15_A = ', format(temp15, '08b'))
        #temp15 = self.reverseBits(temp15, 8)
        #print('temp15_B = ', format(temp15, '08b'))
        temp15 = temp15 >> 2
        sbyte_8 = sbyte_8 | temp15 # set 6 lowe bits of sbyte_8
        #print('sbyte_8 = ', format(sbyte_8, '08b'))

        # second 5 bits
        position = 7 # extract from bit 6.6 to 6.10
        numOfBits = 5 # extract 5 bits
        temp16 = np.ubyte( self.bitExtracted(ch6_data, numOfBits, position) )
        #print('temp16 = ', format(temp16, '08b'))
        #temp16 = np.ubyte(self.reverseBits(temp16, 8))
        #print('temp16 = ', format(temp16, '08b'))
        sbyte_9 = temp16  # 5 high bits are ready in byte_9
        #print('sbyte_9 = ', format(sbyte_9, '08b'))

        # ////////////////ch_7////////////////
        # first 3 bits
        #print('\nch7_data = ', format(ch7_data, '011b'))
        position = 1 # extract from bit 7.0 to 7.2
        numOfBits = 3 # extract 3 bits
        temp16 = np.ubyte(self.bitExtracted(ch7_data, numOfBits, position))
        #print('temp16_A = ', format(temp16, '08b'))
        #temp16 = self.reverseBits(temp16, 8)
        #print('temp16_B = ', format(temp16, '08b'))
        temp16 = temp16 >> 5
        sbyte_9 = sbyte_9 | temp16 # set 3 low bits of sbyte_9
        #print('sbyte_9 = ', format(sbyte_9, '08b'))

        # second 8 bits
        position = 4 # extract from bit 7.3 to 7.10
        numOfBits = 8 # extract 8 bits
        temp17 = np.ubyte( self.bitExtracted(ch7_data, numOfBits, position) )
        #print('temp17 = ', format(temp17, '08b'))
        #temp17 = np.ubyte(self.reverseBits(temp17, 8))
        #print('temp17 = ', format(temp17, '08b'))
        sbyte_10 = temp17  # 8 bits are ready in byte_10
        #print('sbyte_10 = ', format(sbyte_10, '08b'))

        # ////////////////ch_8////////////////
        # first 8 bits
        #print('\nch8_data = ', format(ch8_data, '011b'))
        position = 1 # extract from bit 8.0 to 8.7
        numOfBits = 8 # extract 8 bits
        temp18 = np.ubyte(self.bitExtracted(ch8_data, numOfBits, position))
        #print('temp18_A = ', format(temp18, '08b'))
        #temp18 = self.reverseBits(temp18, 8)
        #print('temp18_B = ', format(temp18, '08b'))
        sbyte_11 = temp18 # set all bits of sbyte_11
        #print('sbyte_11 = ', format(sbyte_11, '08b'))

        # second 3 bits
        position = 9 # extract from bit 8.8 to 8.10
        numOfBits = 3 # extract 5 bits
        temp19 = np.ubyte( self.bitExtracted(ch8_data, numOfBits, position) )
        #print('temp19 = ', format(temp19, '08b'))
        #temp19 = np.ubyte(self.reverseBits(temp19, 8))
        #print('temp19 = ', format(temp19, '08b'))
        sbyte_12 = temp19  # 3 high bits are ready in byte_12
        #print('sbyte_12 = ', format(sbyte_12, '08b'))

        # ////////////////ch_9////////////////
        # first 5 bits
        #print('\nch9_data = ', format(ch9_data, '011b'))
        position = 1 # extract bit from 9.0 to 9.4
        numOfBits =5 # extract 5 bit
        temp20 = np.ubyte(self.bitExtracted(ch9_data, numOfBits, position))
        #print('temp20_A = ', format(temp20, '08b'))
        #temp20 = self.reverseBits(temp20, 8) # put the lsb bit first
        #print('temp20_B = ', format(temp20, '08b'))
        temp20 = temp20 >> 3
        #print('sbyte_12 = ', format(sbyte_12, '08b'))
        #print('temp20 = ', format(temp20, '08b'))
        sbyte_12 = sbyte_12 | temp20 # set 5 lowe  bits of sbyte_12
        #print('sbyte_12 = ', format(sbyte_12, '08b'))

        # second 6 bits
        position = 6 # extract from bit 9.5 to 9.10
        numOfBits = 6 # extract 4 bits
        temp21 = np.ubyte( self.bitExtracted(ch9_data, numOfBits, position) )
        #print('temp21 = ', format(temp21, '08b'))
        #temp21 = np.ubyte(self.reverseBits(temp21, 8))
        #print('temp21 = ', format(temp21, '08b'))
        sbyte_13 = temp21  # 6 high bits are ready in byte_13
        #print('sbyte_13 = ', format(sbyte_13, '08b'))

        # ////////////////ch_10////////////////
        # first 2 bits
        #print('\nch10_data = ', format(ch10_data, '011b'))
        position = 1 # extract bit 10.0 and 10.1
        numOfBits =2 # extract 2 bit
        temp22 = np.ubyte(self.bitExtracted(ch10_data, numOfBits, position))
        #print('temp22_A = ', format(temp22, '08b'))
        #temp22 = self.reverseBits(temp22, 8) # put the lsb bit first
        #print('temp22_B = ', format(temp22, '08b'))
        temp22 = temp22 >> 6
        #print('sbyte_13 = ', format(sbyte_13, '08b'))
        #print('temp22 = ', format(temp22, '08b'))
        sbyte_13 = sbyte_13 | temp22 # set 2 lowest  bits of sbyte_13
        #print('sbyte_13 = ', format(sbyte_13, '08b'))

        # second 8 bits
        position = 3 # extract from bit 10.2 to 10.9
        numOfBits = 8 # extract8 bits
        temp23 = np.ubyte( self.bitExtracted(ch10_data, numOfBits, position) )
        #print('temp23 = ', format(temp23, '08b'))
        #temp23 = np.ubyte(self.reverseBits(temp23, 8))
        #print('temp23 = ', format(temp23, '08b'))
        sbyte_14 = temp23  # 8 bits are ready in byte_14
        #print('sbyte_14 = ', format(sbyte_14, '08b'))

        # last bit
        position = 11 # extract bit 10.10
        numOfBits = 1 # extract 1 bit
        temp24 = np.ubyte(self.bitExtracted(ch10_data, numOfBits, position))
        #print('temp24_A = ', format(temp24, '08b'))
        #temp24 = self.reverseBits(temp24, 8) # put the lsb bit first
        #print('temp24_B = ', format(temp24, '08b'))
        sbyte_15 = sbyte_15 | temp24 # set the highest of sbyte_15
        #print('sbyte_15 = ', format(sbyte_15, '08b'))

        # ////////////////ch_11////////////////
        # first 7 bits
        #print('\nch11_data = ', format(ch11_data, '011b'))
        position = 1 # extract bit from11.0 to 11.6
        numOfBits =7 # extract 7 bit
        temp25 = np.ubyte(self.bitExtracted(ch11_data, numOfBits, position))
        #print('temp25_A = ', format(temp25, '08b'))
        #temp25 = self.reverseBits(temp25, 8) # put the lsb bit first
        #print('temp25_B = ', format(temp25, '08b'))
        temp25 = temp25 << 1
        sbyte_15 = sbyte_15 | temp25 # set 7 low  bits of sbyte_15
        #print('sbyte_15 = ', format(sbyte_15, '08b'))

        # second 4 bits
        position = 8 # extract from bit 11.7 to 11.10
        numOfBits = 4 # extract 4 bits
        temp26 = np.ubyte( self.bitExtracted(ch11_data, numOfBits, position) )
        #print('temp26 = ', format(temp26, '08b'))
        #temp26 = np.ubyte(self.reverseBits(temp26, 8))
        #print('temp26 = ', format(temp26, '08b'))
        sbyte_16 = temp26  # 4 high bits are ready in byte_16
        #print('sbyte_16 = ', format(sbyte_16, '08b'))

        # ////////////////ch_12////////////////
        # first 4 bits
        #print('\nch12_data = ', format(ch12_data, '011b'))
        position = 1 # extract bit from 12.0 to 12.3
        numOfBits = 4 # extract 4 bit
        temp27 = np.ubyte(self.bitExtracted(ch12_data, numOfBits, position))
        #print('temp27_A = ', format(temp27, '08b'))
        #temp27 = self.reverseBits(temp27, 8) # put the lsb bit first
        #print('temp27_B = ', format(temp27, '08b'))
        temp27 = temp27 >> 4
        sbyte_16 = sbyte_16 | temp27 # set 7 low  bits of sbyte_15
        #print('sbyte_16 = ', format(sbyte_16, '08b'))

        # second 7 bits
        position = 5 # extract from bit 12.4 to 12.10
        numOfBits = 7 # extract 7 bits
        temp28 = np.ubyte( self.bitExtracted(ch12_data, numOfBits, position) )
        #print('temp26 = ', format(temp28, '08b'))
        #temp28 = np.ubyte(self.reverseBits(temp28, 8))
        #print('temp28 = ', format(temp28, '08b'))
        sbyte_17 = temp28  # 7 high bits are ready in byte_17
        #print('sbyte_17 = ', format(sbyte_17, '08b'))

        # ////////////////ch_13////////////////
        # first 1 bit
        #print('\nch13_data = ', format(ch13_data, '011b'))
        position = 1 # extract bit 13.0
        numOfBits =1 # extract 1 bit
        temp29 = np.ubyte(self.bitExtracted(ch13_data, numOfBits, position))
        #print('temp29_A = ', format(temp29, '08b'))
        #temp29 = self.reverseBits(temp29, 8) # put the lsb bit first
        #print('temp29_B = ', format(temp29, '08b'))
        temp29 = temp29 >> 7
        sbyte_17 = sbyte_17 | temp29 # set the lowest  bit of sbyte_17
        #print('sbyte_17 = ', format(sbyte_17, '08b'))

        # second 8 bits
        position = 2 # extract from bit 13.1 to 13.8
        numOfBits = 8 # extract 8 bits
        temp30 = np.ubyte( self.bitExtracted(ch13_data, numOfBits, position) )
        #print('temp30 = ', format(temp30, '08b'))
        #temp30 = np.ubyte(self.reverseBits(temp30, 8))
        #print('temp30 = ', format(temp30, '08b'))
        sbyte_18 = temp30  # 8 bits are ready in byte_18
        #print('sbyte_18 = ', format(sbyte_18, '08b'))

        # last 2 bit2
        position = 10 # extract bits 13.9 and 13.10
        numOfBits = 2 # extract 2 bits
        temp31 = np.ubyte(self.bitExtracted(ch13_data, numOfBits, position))
        #print('temp31_A = ', format(temp31, '08b'))
        #temp31 = self.reverseBits(temp31, 8) # put the lsb bit first
        #print('temp31_B = ', format(temp31, '08b'))
        sbyte_19 = sbyte_19 | temp31# set two highe bits of sbyte_19
        #print('sbyte_19 = ', format(sbyte_19, '08b'))

        # ////////////////ch_14////////////////
        # first 6 bits
        #print('\nch14_data = ', format(ch14_data, '011b'))
        position = 1 # extract from bit 14.0 to 14.5
        numOfBits = 6 # extract 6 bits
        temp32 = np.ubyte(self.bitExtracted(ch14_data, numOfBits, position))
        #print('temp32_A = ', format(temp32, '08b'))
        #temp32 = self.reverseBits(temp32, 8)
        #print('temp32_B = ', format(temp32, '08b'))
        temp32 = temp32 >> 2
        sbyte_19 = sbyte_19 | temp32 # set 6 lowe bits of sbyte_19
        #print('sbyte_19 = ', format(sbyte_19, '08b'))

        # second 5 bits
        position = 7 # extract from bit 14.6 to 14.10
        numOfBits = 5 # extract 5 bits
        temp33 = np.ubyte( self.bitExtracted(ch14_data, numOfBits, position) )
        #print('temp33 = ', format(temp33, '08b'))
        #temp33 = np.ubyte(self.reverseBits(temp33, 8))
        #print('temp33 = ', format(temp33, '08b'))
        sbyte_20 = temp33 # 5 high bits are ready in byte_20
        #print('sbyte_20 = ', format(sbyte_20, '08b'))

        # ////////////////ch_15////////////////
        # first 3 bits
        #print('\nch15_data = ', format(ch15_data, '011b'))
        position = 1 # extract from bit 15.0 to 15.2
        numOfBits = 3 # extract 3 bits
        temp34 = np.ubyte(self.bitExtracted(ch15_data, numOfBits, position))
        #print('temp34_A = ', format(temp34, '08b'))
        #temp34 = self.reverseBits(temp34, 8)
        #print('temp34_B = ', format(temp34, '08b'))
        temp34 = temp34 >> 5
        sbyte_20 = sbyte_20 | temp34 # set 3 low bits of sbyte_20
        #print('sbyte_20 = ', format(sbyte_20, '08b'))

        # second 8 bits
        position = 4 # extract from bit 15.3 to 15.10
        numOfBits = 8 # extract 8 bits
        temp35 = np.ubyte( self.bitExtracted(ch15_data, numOfBits, position) )
        #print('temp35 = ', format(temp35, '08b'))
        #temp35 = np.ubyte(self.reverseBits(temp35, 8))
        #print('temp35 = ', format(temp35, '08b'))
        sbyte_21 = temp35  # 8 bits are ready in byte_21
        #print('sbyte_21 = ', format(sbyte_21, '08b'))
        
        byte_23 = 0

        # byte_23 = 0b0000  failsafe  frame_lost  digi_ch18  digi_ch17
        # failsafe   = 0b0;    frame_lost = 0b0
        if d_ch17 == 1:
            byte_23 = self.set_bit(byte_23, 0) # stop button pressed
            byte_23 = self.clear_bit(byte_23, 1)

        elif d_ch18 == 1:
            byte_23 = self.set_bit(byte_23, 1) # start button pressed
            byte_23 = self.clear_bit(byte_23, 0)
            
        else:
            byte_23 = self.clear_bit(byte_23, 0)
            byte_23 = self.clear_bit(byte_23, 1)

        byte_24 = 0x00

        flag_byte  = byte_23
        End_byte   = byte_24

        sendArray = bytearray([ Start_byte,  \
                                sbyte_0, sbyte_1,  sbyte_2,  sbyte_3,  sbyte_4,  sbyte_5,  sbyte_6,  sbyte_7, \
                                sbyte_8,  sbyte_9,  sbyte_10, sbyte_11, sbyte_12, sbyte_13, sbyte_14, sbyte_15, \
                                sbyte_16, sbyte_17, sbyte_18, sbyte_19, sbyte_20, sbyte_21, \
                                flag_byte, End_byte \
                             ])

        return sendArray;