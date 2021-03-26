from Ultrasonic_Class_V3 import UltraSonic # import this class
import threading

# Measure the distance for ultrasonic sensor #1 and #2
sensors_Z_X = UltraSonic()       # create a new instance for Z and X sensors
t_sensors_Z_X = threading.Thread(target=sensors_Z_X.measurement, daemon=True)
t_sensors_Z_X.start()

# Distance Range is 8cm to 82cm