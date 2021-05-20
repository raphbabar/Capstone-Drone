import RPi.GPIO as GPIO
import time
import os, signal

from time import sleep, time

# GPIO settings
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

class ultrasonic(): #ultrasonic Class
    
    def __init__(self, TRIG, ECHO, offset = 0.5):
        # Create a new sensor instance
        self.TRIG = TRIG
        self.ECHO = ECHO
        self.offset = offset                             # Sensor calibration factor
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.TRIG, GPIO.OUT)                  # Set pin as GPIO output
        GPIO.setup(self.ECHO, GPIO.IN)                   # Set pin as GPIO input

    def ping(self):
        # Get distance measurement
        GPIO.output(self.TRIG, GPIO.LOW)                 # Set TRIG LOW
        sleep(0.1)                                       # Min gap between measurements        
        # Create 10 us pulse on TRIG
        GPIO.output(self.TRIG, GPIO.HIGH)                # Set TRIG HIGH
        sleep(0.00001)                                   # Delay 10 us
        GPIO.output(self.TRIG, GPIO.LOW)                 # Set TRIG LOW
        # Declare variables
        pulse_start = 0
        pulse_end = 0
        # Measure return echo pulse duration
        while GPIO.input(self.ECHO) == GPIO.LOW:         # Wait until ECHO is LOW
            pulse_start = time()                         # Save pulse start time

        while GPIO.input(self.ECHO) == GPIO.HIGH:        # Wait until ECHO is HIGH
            pulse_end = time()                           # Save pulse end time

        pulse_duration = pulse_end - pulse_start 
        # Distance = 17160.5 * Time (unit cm) at sea level and 20C
        distance = pulse_duration * 17160.5              # Calculate distance
        distance = round(distance, 2)                    # Round to two decimal points

        if distance > 2 and distance < 400:              # Check distance is in sensor range
            distance = distance + self.offset
            #print("Distance: ", distance," cm")
        else:
            distance = 0
            print("Distance is not in range")            # Nothing detected by sensor
        return distance
            
    @staticmethod
    def low_pass_filter(value, previous_value, beta):
        # Simple infinite-impulse-response (IIR) single-pole low-pass filter.
        # ß = discrete-time smoothing parameter (determines smoothness). 0 < ß < 1
        # LPF: Y(n) = (1-ß)*Y(n-1) + (ß*X(n))) = Y(n-1) - (ß*(Y(n-1)-X(n)))
        smooth_value = previous_value - (beta * (previous_value - value))
        return smooth_value
        

    def measure(TRIG, ECHO):
        # Measure the distance for ultrasonic sensor #1 and #2
        sensor = ultrasonic(TRIG, ECHO)       # create a new sensor instance on GPIO pins

        def endProcess(signum = None, frame = None):
            # Called on process termination. 
            if signum is not None:
                SIGNAL_NAMES_DICT = dict((getattr(signal, n), n) for n in dir(signal) if n.startswith('SIG') and '_' not in n )
                print("signal {} received by process with PID {}".format(SIGNAL_NAMES_DICT[signum], os.getpid()))
            print("\n-- Terminating program --")
            print("Cleaning up GPIO...")
            GPIO.cleanup()
            print("Done.")
            exit(0)

        # Assign handler for process exit
        signal.signal(signal.SIGTERM, endProcess)
        signal.signal(signal.SIGINT, endProcess)
        signal.signal(signal.SIGHUP, endProcess)
        signal.signal(signal.SIGQUIT, endProcess)
        
        beta = 0.1
        distance = 0
        
        while True:
            distance = sensor.low_pass_filter(sensor.ping(), distance, float(beta))
            distance = round(distance, 2)
            print("Ultrasonic #1 Distance (Z Direction) is ", distance)
            return distance
