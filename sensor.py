import RPi.GPIO as GPIO
import time
from threading import Thread, Lock

class Sensor:

    def __init__(self):
        self.distance = 0
        self.mutex = Lock()
        self.threshold = 1

    def setThreshold(self, threshold):

        self.mutex.acquire()

        try:
            self.threshold = threshold
        finally:
            self.mutex.release()

    def getReading(self):
        self.mutex.acquire()
        
        try:
            if self.distance < self.threshold:
                return self.distance
            else:
                return None
        finally:
            self.mutex.release()


    def startSensors(self):

        GPIO.setmode(GPIO.BCM)
        TRIG= 4
        ECHO = 18
        
        # while True:

        #     GPIO.setup(TRIG, GPIO.OUT)
        #     GPIO.setup(ECHO, GPIO.IN)

        #     GPIO.output(TRIG, False)
        #     print('waiting for sensor')
        #     time.sleep(2)

        #     GPIO.output(TRIG, True)
        #     time.sleep(0.00001)
        #     GPIO.output(TRIG, False)

        #     while GPIO.input(ECHO) == 0:
        #         pulse_start = time.time()

        #     while(GPIO.input(ECHO) == 1):
        #         pulse_end = time.time()

        #     pulse_duration = pulse_end - pulse_start
        #     distance = pulse_duration*17150
        #     distance = round(distance,2)

        #     print('Distance:',distance,'cm')

        #     GPIO.cleanup()
        
        #     dist_in_metres = distance/100

        #     self.mutex.acquire()
        #     if dist_in_metres < self.threshold:
        #         self.distance = dist_in_metres
            
        #     self.mutex.release()
    
        
