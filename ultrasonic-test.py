from ultrasonic import ultrasonic

# GPIO pins and setup for TRIGGER and ECHO
TRIG1 = 5                                                #PIN 29
ECHO1 = 6                                                #PIN 31
TRIG2 = 23                                               #PIN 
ECHO2 = 24                                               #PIN 

# Declare variables
distance1 = 0
distance2 = 0

# Measure distance for z direction
#distance1 = ultrasonic.measure(TRIG1, ECHO1)
# Measure distance for x direction
#distance2 = ultrasonic.measure(TRIG2, ECHO2)

# Print results
#print("Ultrasonic #1 Distance (Z Direction) is ", distance1)
#print("Ultrasonic #2 Distance (X Direction) is ", distance2)

ultrasonic.measure(TRIG1, ECHO1)