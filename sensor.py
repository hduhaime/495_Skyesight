cimport time
from threading import Thread, Lock

TO_METRES = 0.01
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
        
        while True:

            #Call the API server running on python
            response = requests.get("http://api.open-notify.org/iss-now.json")

            if response.status_code == 200:

                dist_in_metres = response["distance"]*TO_METRES

                self.mutex.acquire()
                if dist_in_metres < self.threshold:
                    self.distance = dist_in_metres
                
                self.mutex.release()
    
        
