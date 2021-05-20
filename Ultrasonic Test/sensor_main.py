"""Example of getting a direct reading from RPi.GPIO."""

import numpy as np
import RPi.GPIO as GPIO
import time
from sensor_class import sensor

# set gpio pins
trig = 5
echo = 6

# Declare variables
n = 10
total = 0
samples = []
ct = 0

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)  # use GPIO.BOARD for board pin values

def reject_outliers(data, m=10):
    d = np.abs(data - np.median(data))
    mdev = np.median(d)
    s = d / (mdev if mdev else 1.)
    return data[s < m]

def average_list(lst):
    return sum(lst) / len(lst)

print("Test for n = ",n,"\n")

while True:
    # Measurement
    start = time.time()
    x = sensor.Measurement
    # Distance
    i = 0
    samples.clear()
    while i < n:
        samples.append(round(x.basic_distance(trig, echo),1))
        time.sleep(0.01)
        i += 1
    #print(samples)
    np_sample = np.array(samples)
    #print("raw data: ",np_sample)
    filtered = reject_outliers(np_sample,20)
    #print("filtered: ", filtered)
    average = np.average(filtered)
    #print(" average: ", average)
    #distance = round(total / n, 2)
    #total = 0
    end = time.time()
    
    # Check for false readings before print/send of data
    #if distance-round(x.basic_distance(trig, echo),2) > 5:
        #print("Error: False Reading ---> {} cm".format(distance))
    #else:
    print("The distance is {} cm".format(round(average,1)))
    print("The measurement speed is {} sec".format(round(end-start,3)))
    ct = ct + 1
# cleanup gpio pins.
GPIO.cleanup((trig, echo))