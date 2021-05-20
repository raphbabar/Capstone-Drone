import RPi.GPIO as GPIO
import time, sys
import statistics 
GPIO.setmode(GPIO.BCM)


log=__import__("logger")

TRIG = 23
ECHO = 24

log.log("Settng up Distance module...","distance.py")

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
history=[]

total=0
count=0
distance=0
avg=0
dist=[]
distlist=[]
scan=False

GPIO.setmode(GPIO.BCM)
TRIG = 23
ECHO = 24
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

def status():
    history=[]

    starttime=time.time()
    for i in range(10):
        GPIO.output(TRIG, False)
        time.sleep(0.1)
        #print("Waiting for sensor to settle...")
        #print("Please wait...")

        # ==========
        # GPIO Setup
        # ==========
        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)

        #print("Sending...")
        start=time.time()
        pulse_start=start
        while GPIO.input(ECHO)==0 and pulse_start-start<=0.0005:
            pulse_start=time.time()
        if round(pulse_start-start,3)>=0.300:
            print(timeout)
        else:
            #print("Receiving...")
            pulse_end=0
            pulse_duration=0
            while GPIO.input(ECHO)==1 and pulse_duration<2:
                pulse_end=time.time()
                pulse_duration=pulse_end-pulse_start
                #print("Measuring...")

        pulse_duration=pulse_end-pulse_start

        # ====================
        # Calculating Distance
        # ====================
        distance=pulse_duration*17150
        distance=round(distance,2)
        history.append(distance)
    validcount=0
    total=0
    print(history)
    for i in history:
        if i<150:
            validcount+=1
            total+=i
    if validcount>1:
        avg_dist=round(total/validcount,2)
        print("Average distance:",avg_dist)
        if avg_dist<=50:
            return([avg_dist,True,avg_dist,avg_dist])
        else:
            return([avg_dist,False,avg_dist,avg_dist])
    else:
        print("Timeout")
        return([999,False,999,999])
    
while True: print(status()); time.sleep(1)