from enum import Enum
import cv2
from PIL import Image
from PIL import ImageTk
from Util import DisplaySelection
from image_stitching import Stitcher
from sensor import Sensor
from threading import Thread, Lock


class FeedSelections(Enum):
    Overhead = 0
    Left = 1
    Rear = 2
    Right = 3


class CamList(Enum):
    Left = 0
    Right = 1
    Rear = 2

class SensorList(Enum):
    Left = 0
    Right = 1
    Rear = 2

class GPIO(Enum):
    TRIG = 0
    ECHO = 1

feedToCamMap = {
                FeedSelections.Overhead: [CamList.Left, CamList.Right, CamList.Rear],
                FeedSelections.Left: CamList.Left,
                FeedSelections.Right: CamList.Right,
                FeedSelections.Rear: CamList.Rear
                }

feedListVals = [feedList for feedList in FeedSelections]

feedToDefaultMap = {
                    FeedSelections.Overhead: Image.open('defaultImages/overheadDefault.png').resize((400, 300)),
                    FeedSelections.Left: Image.open('defaultImages/leftDefault.png').resize((400, 300)),
                    FeedSelections.Right: Image.open('defaultImages/rightDefault.png').resize((400, 300)),
                    FeedSelections.Rear: Image.open('defaultImages/rearDefault.png').resize((400, 300))
                    }

class Model:
    def __init__(self, leftCapture, rightCapture, rearCapture, sensorVals):
        self.displayToFeedMap = {
                                DisplaySelection.MainLeft: FeedSelections.Overhead,
                                DisplaySelection.Right: FeedSelections.Overhead
                                }

        self.stitcher = Stitcher()

        #Create the left sensor
        self.leftSensor = Sensor(sensorVals[SensorList.Left][GPIO.TRIG], sensorVals[SensorList.Left][GPIO.ECHO])

        #Run a thread to start the readings
        t = Thread(target = self.leftSensor.startSensors())
        t.start()

        self.notificationsMuted = False
        self.leftCapture = leftCapture
        self.rightCapture = rightCapture
        self.rearCapture = rearCapture


    def nextFeed(self, displaySelection):
        curSelection = self.displayToFeedMap[displaySelection]
        self.displayToFeedMap[displaySelection] = \
            feedListVals[(curSelection.value + 1) % len(feedListVals)]

    def prevFeed(self, displaySelection):
        curSelection = self.displayToFeedMap[displaySelection]
        self.displayToFeedMap[displaySelection] = \
            feedListVals[len(feedListVals) - 1 if curSelection.value == 0 else curSelection.value - 1]

    def toggleNotifications(self, notificationsMuted):
        self.notificationsMuted = notificationsMuted

    def getFeed(self, displaySelection):
        # Get the needed feeds for the relevant display selection
        feedSelection = self.displayToFeedMap[displaySelection]

        if feedSelection == FeedSelections.Overhead:
            # Pull from all feeds and stitch them together
            try:
                leftFeed = self.getWebcamFrame(self.leftCapture)
                rightFeed = self.getWebcamFrame(self.rightCapture)
                rearFeed = self.getWebcamFrame(self.rearCapture)

                if leftFeed is None or rightFeed is None or rearFeed is None:
                    return ImageTk.PhotoImage(feedToDefaultMap[feedSelection])

                stitchedArray = self.stitcher.stitch([leftFeed, rightFeed, rearFeed])
                stitchedImage = ImageTk.PhotoImage(Image.fromarray(stitchedArray))
                return stitchedImage
            except RuntimeError:
                return ImageTk.PhotoImage(feedToDefaultMap[feedSelection])
        elif feedSelection == FeedSelections.Left:
            leftFeed = self.getWebcamFrame(self.leftCapture)
            if leftFeed is None:
                return ImageTk.PhotoImage(feedToDefaultMap[feedSelection])

            return ImageTk.PhotoImage(Image.fromarray(leftFeed))
        elif feedSelection == FeedSelections.Right:
            rightFeed = self.getWebcamFrame(self.rightCapture)
            if rightFeed is None:
                return ImageTk.PhotoImage(feedToDefaultMap[feedSelection])

            return ImageTk.PhotoImage(Image.fromarray(rightFeed))
        elif feedSelection == FeedSelections.Rear:
            rearFeed = self.getWebcamFrame(self.rearCapture)
            if rearFeed is None:
                return ImageTk.PhotoImage(feedToDefaultMap[feedSelection])

            return ImageTk.PhotoImage(Image.fromarray(rearFeed))


    def recalibrate(self):
        self.stitcher.calibrate()


    def getReading(self):

        readings = {
            SensorList.Left: self.leftSensor.getReading()
        }

        '''
        readings = {
            SensorList.Left: self.leftSensor.getReading(),
            SensorList.Right: self.rightSensor.getReading(),
            SensorList.Rear: self.rearSensor.getReading(),

        }
        '''

        return readings

    def setThreshold(self, threshold):
        leftSensor.setThreshold(threshold)

        #rightSensor.setThreshold(threshold)
        #rearSensor.setThreshold(threshold)



    @staticmethod
    def getWebcamFrame(capture):
        ret, frame = capture.read()

        if not ret:
            return None

        frame_to_display = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        if frame_to_display.shape[0] != 480:
            frame_to_display = cv2.resize(frame_to_display, None, fx=0.444444, fy=0.444444)[:, 106:746, :]

        return cv2.flip(frame_to_display, 1)