import RPi.GPIO as GPIO
from time import sleep, time

class UltraSonic(): #UltraSonic Class
    
    def __init__(self):
        
        self.beta = 0.7

        # Pin settings
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

    @staticmethod
    def low_pass_filter(value, previous_value, beta):
        # Simple infinite-impulse-response (IIR) single-pole low-pass filter.
        # ß = discrete-time smoothing parameter (determines smoothness). 0 < ß < 1
        # LPF: Y(n) = (1-ß)*Y(n-1) + (ß*X(n))) = Y(n-1) - (ß*(Y(n-1)-X(n)))
        smooth_value = previous_value - (beta * (previous_value - value))
        return smooth_value

    def measurement(self):
        # Start time for ultrasonic measurement
        start_measure = time()
        # Enter the expected Z distance
        expected_Z = 200
        # Flags
        speed_flag = False
        flag_Z = False
        flag_time = 0
        
        while True:
            # Take the distance measurement and apply filter
            self.distance_Z = self.low_pass_filter( self.ping( self.TRIG_Z, self.ECHO_Z, self.offset_Z ), self.distance_Z, float(self.beta) )
            self.distance_X = self.low_pass_filter( self.ping( self.TRIG_X, self.ECHO_X, self.offset_X), self.distance_X, float(self.beta) )
            self.distance_Z = round(self.distance_Z, 2)
            self.distance_X = round(self.distance_X, 2)
            # End time for ultrasonic measurement
            end_measure = time()
            # Print the elapsed time for the ultrasonic measurement
            if speed_flag == False:
                print("1) How often measurement updates: ", round(end_measure-start_measure,4), "sec")
                speed_flag = True
            
            # Print the distance for both Z and X directions
            #print("UltraSonic #1 (Z Direction): ", self.distance_Z, " cm")
            #print("UltraSonic #2 (X Direction): ", self.distance_X, " cm")
            
            # Test the steady state time
            error_Z = abs(expected_Z - self.distance_Z)
            #print("Error is ", round(error_Z,2))
            accuracy = 3.00
            if error_Z < accuracy:
                steady_time_Z = time() - start_measure
                if flag_Z == False:
                    print("Steady State Time (within", round(accuracy,1), "cm): ", round(steady_time_Z,2), "sec")
                    print("Distance at steady state (within", round(accuracy,1), "cm): ", self.distance_Z, "cm")
                flag_Z = True
            flag_time = flag_time + 1 
            if flag_time == 50:
                print("Distance at t = inf : ", self.distance_Z, " cm")
                print("2) Accuracy (expected = 20 cm): ", round(abs(self.distance_Z - expected_Z),4), "cm")