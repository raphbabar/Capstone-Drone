import RPi.GPIO as GPIO
import numpy as np
from time import sleep, time
import collections

class UltraSonic(): #UltraSonic Class
    
    def __init__(self):
        
        # Pin settings - change when using drone
        self.TRIG_Z = 5
        self.ECHO_Z = 6
        self.offset_Z = 0.5

        self.TRIG_X = 23
        self.ECHO_X = 24
        self.offset_X = 0.5

        # GPIO pins and setup for TRIGGER and ECHO
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        GPIO.setup(self.TRIG_Z, GPIO.OUT)                  # Set pin as GPIO output
        GPIO.setup(self.ECHO_Z, GPIO.IN)                    # Set pin as GPIO input

        GPIO.setup(self.TRIG_X, GPIO.OUT)                  # Set pin as GPIO output
        GPIO.setup(self.ECHO_X, GPIO.IN)                    # Set pin as GPIO input

        self.distance_Z = 0
        self.distance_X = 0

    def ping(self, TRIG, ECHO, offset):
        
        start_ultrasonic = time()
        # Get distance measurement
        GPIO.output(TRIG, GPIO.LOW)                 # Set TRIG LOW
        sleep(0.1)                                       # Min gap between measurements        
        # Create 10 us pulse on TRIG
        GPIO.output(TRIG, GPIO.HIGH)                # Set TRIG HIGH
        sleep(0.00001)                                   # Delay 10 us
        GPIO.output(TRIG, GPIO.LOW)                 # Set TRIG LOW
        # Declare variables
        pulse_start = 0
        pulse_end = 0
        # Measure return echo pulse duration
        while GPIO.input(ECHO) == GPIO.LOW:         # Wait until ECHO is LOW
            pulse_start = time()                         # Save pulse start time

        while GPIO.input(ECHO) == GPIO.HIGH:        # Wait until ECHO is HIGH
            pulse_end = time()                           # Save pulse end time

        pulse_duration = pulse_end - pulse_start 
        # Distance = 17160.5 * Time (unit cm) at sea level and 20C
        distance = pulse_duration * 17160.5              # Calculate distance
        distance = round(distance, 2)                    # Round to two decimal points

        if distance > 2 and distance < 400:              # Check distance is in sensor range
            distance = distance + offset
            #print("Distance: ", distance," cm")
        else:
            distance = 0
            print("Distance is not in range")            # Nothing detected by sensor
        end_ultrasonic = time()
        #print("Ultrasonic time is ", end_ultrasonic-start_ultrasonic)
        return distance
    
    def measurement(self):
        
        # Enter variables
        expected = 200    # ENTER EXPECTED DISTANCE HERE
        n = 50            # ENTER # OF SAMPLES FOR MOVING AVERAGE FILTER
        
        # Other variables
        i = 0             # counter
        k = 0             # counter
        total = 0         # sum for moving average calc.
        samples = []      # list of samples
        elapsed_time = 0  # total time
        max_time = 300    # time limit for stability test
        
        # Generate list/buffer (size "n"). Store n samples into buffer
        while i < n: 
            samples.append(round(self.ping( self.TRIG_Z, self.ECHO_Z, self.offset_Z ),2))
            i += 1
        
        while True:
            # Start time for ultrasonic measurement
            start = time()
            #print("Start: ", start)
            
            # Circular Buffer - store data where pointer is at
            # eg. [1 2 3 4] -> [5 2 3 4] -> [5 6 3 4] -> ...
            samples[k] = round(self.ping( self.TRIG_Z, self.ECHO_Z, self.offset_Z ),2)
            if k > n-2:
                k = 0
            else:
                k += 1
            
            # Convert sample to numpy array
            np_sample = np.array(samples)
            #print("raw data: ",np_sample)
            
            # Reject outlier from array
            d = np.abs(np_sample - np.median(np_sample))
            mdev = np.median(d)
            s = d / (mdev if mdev else 1.)
            filtered = np_sample[s < n]
            #print("Filtered: ",filtered)
            
            # Calculate the average         
            average = round(sum(filtered) / len(filtered),2)
            #print("Average: ",average)
            
            # End time for ultrasonic measurement
            end = time()
            
            # Calculate speed and accuracy
            accuracy = round(abs(average - expected),2)
            speed = round(end - start,2)
            
            # Print the distance and other test measurements
            print(" Ultrasonic Test Result: Moving Average Filter (n = ", n, ")\n",\
                  "(1) Accuracy: +/- ", accuracy, " cm\n",\
                  "(2) Speed: ", speed, " sec\n",\
                  "(3) DISTANCE: ", average, " cm\n",\
                  "(4) Elapsed Time = ", round(elapsed_time,2), "sec\n\n")
            
            # Stability Test - stop code if error is greater than +/- 5 cm (UNSTABLE)
            #if accuracy > 5:
            #    print("Distance is unstable")
            #    sleep(1000)
            # Stability Test - stop code if error is less than +/- 5 cm for 5 minutes (STABLE)
            #if accuracy < 5 and elapsed_time > max_time:
            #    print("Distance is stable")
            #    sleep(1000)
            
            # Timer for total time elapsed
            elapsed_time += speed
