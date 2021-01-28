import serial
import time

# Function to reverse bits of positive  
# integer number

chan = 0
data = 1600
phase = 1

# may need to use latin-1 string encoding

# look into using bytearray

ser = serial.Serial(
"/dev/ttyS0",
parity=serial.PARITY_EVEN,
stopbits=serial.STOPBITS_TWO,
bytesize=serial.EIGHTBITS 
)
ser.baudrate = 100000

#Highest bit is sent first
HEADER = 0x0F #Byte[0]: SBUS Header, 0x0F #RB
#SERVO  = 0x00 #Byte[1-22]: 16 servo channels, 11 bits per servo channel #RB
AUX    = 0x00 #Byte[23]: Choose -> Bit 0 to 7 (https://github.com/bolderflight/SBUS) #RB
END    = 0x00 #Byte[24]: SBUS End Byte, 0x00

#From Original Code
#UPPER = 0xFF00
#LOWER = 0x00FF

# Test UART
# ---------
# ~$ nano serial_read.py

def makeWord(chan, data):
    CHANNEL = 15
    
    word = (chan << CHANNEL) | (data)
    return word
    
def reverseBits(num,bitSize): 
  
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
     #print int(reverse,2)
     return int(reverse,2)
    

try:
    #Channel (Servo) data
    data = 150; #RB

    while(1):        
        # Generate first 16-Byte packet:
        # Ch0 is throttle
        # Ch1 is aileron (roll)
        # Ch2 is elevator (pitch)
        # Ch3 is rudder (yaw)
        # Ch4 is aux1
        # Ch5 is aux2
        # Ch6 is aux3
                
        dataString = ""
        header = chr(HEADER)
        servo = makeWord(0,100)
        aux = chr(AUX)
        end = chr(END)
        dataString = end + aux + servo + header
            
        # Send 16 bytes over serial bus to flight controller
        ser.write(dataString)
        time.sleep(0.008)
                
        # Incr
        data = data + 1
        if(data > 255):
            data = 0
    
except Exception as e:
    print(e)
    
finally:
    ser.close()