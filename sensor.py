import time
from threading import Thread, Lock
import requests

TO_METRES = 0.01
IP = "35.1.53.166"
class Sensor:

    def __init__(self, TRIG, ECHO):
        self.distance = 0
        self.mutex = Lock()
        self.threshold = 1
        self.TRIG = TRIG
        self.ECHO = ECHO

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
        
        while True:

            #Call the API server running on python
            response = requests.post("http://"+IP+"/fetchSensorData", data={'TRIG':self.TRIG, 'ECHO':self.ECHO})
            print(response.json())
            if response.status_code == 200:

                dist_in_metres = (response.json())["distance"]*TO_METRES

                self.mutex.acquire()
                if dist_in_metres < self.threshold:
                    self.distance = dist_in_metres
                
                self.mutex.release()
    
        
