from ultrasonic_class import UltraSonic #ultrasonic_class
import threading

# Measure the distance for ultrasonic sensor #1 and #2
sensors_Z_X = UltraSonic()       # create a new instance for Z and X sensors
t_sensors_Z_X = threading.Thread(target=sensors_Z_X.measurement, daemon=True)
t_sensors_Z_X.start()

