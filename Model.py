from enum import Enum
import cv2
from PIL import Image
#TODO from PIL import ImageTk
from Util import *
from image_stitching import Stitcher
from sensor import Sensor
from threading import Thread


class FeedSelections(Enum):
    Overhead = 0
    Left = 1
    Rear = 2
    Right = 3

feedToCamMap = {
                FeedSelections.Overhead: [CamList.Left, CamList.Right, CamList.Rear],
                FeedSelections.Left: CamList.Left,
                FeedSelections.Right: CamList.Right,
                FeedSelections.Rear: CamList.Rear
                }

feedListVals = [feedList for feedList in FeedSelections]

#TODO:
# feedToDefaultMap = {
#                     FeedSelections.Overhead: Image.open('defaultImages/overheadDefault.png').resize((400, 300)),
#                     FeedSelections.Left: Image.open('defaultImages/leftDefault.png').resize((400, 300)),
#                     FeedSelections.Right: Image.open('defaultImages/rightDefault.png').resize((400, 300)),
#                     FeedSelections.Rear: Image.open('defaultImages/rearDefault.png').resize((400, 300))
#                     }

feedToDefaultMap = {
                    FeedSelections.Overhead: cv2.imread('defaultImages/overheadDefault.png').resize((400, 300)),
                    FeedSelections.Left: cv2.imread('defaultImages/leftDefault.png').resize((400, 300)),
                    FeedSelections.Right: cv2.imread('defaultImages/rightDefault.png').resize((400, 300)),
                    FeedSelections.Rear: cv2.imread('defaultImages/rearDefault.png').resize((400, 300))
                    }

class Model:
    def __init__(self, leftCapture, rightCapture, rearCapture, sensorVals):
        self.displayToFeedMap = {
                                DisplaySelection.MainLeft: FeedSelections.Overhead,
                                DisplaySelection.Right: FeedSelections.Overhead
                                }

        self.stitcher = Stitcher()

        #Create the left sensor
        self.leftSensor = Sensor(sensorVals[CamList.Left][GPIO.TRIG], sensorVals[CamList.Left][GPIO.ECHO])

        #Run a thread to start the readings
        t = Thread(target = self.leftSensor.startSensors)
        t.start()

        self.notificationsMuted = False
        self.leftCapture = leftCapture
        self.rightCapture = rightCapture
        self.rearCapture = rearCapture

    def changeFeed(self, displaySelection, desiredFeedSelection):
        self.displayToFeedMap[displaySelection] = desiredFeedSelection

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
<<<<<<< HEAD
            leftFeed = self.getWebcamFrame(self.leftCapture)
            rightFeed = self.getWebcamFrame(self.rightCapture)
            rearFeed = self.getWebcamFrame(self.rearCapture)

            if leftFeed is None or rightFeed is None or rearFeed is None:
                return feedToDefaultMap[feedSelection] #TODO: ImageTk.PhotoImage(feedToDefaultMap[feedSelection])

            stitchedArray = self.stitcher.stitch([leftFeed, rightFeed, rearFeed])
            stitchedImage = stitchedArray #TODO: ImageTk.PhotoImage(Image.fromarray(stitchedArray))
            return stitchedImage
=======
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
>>>>>>> 9679d3013fdbbc840e71d10f8b4860d12d9c0aff
        elif feedSelection == FeedSelections.Left:
            leftFeed = self.getWebcamFrame(self.leftCapture)
            if leftFeed is None:
                return feedToDefaultMap[feedSelection] #TODO: ImageTk.PhotoImage(feedToDefaultMap[feedSelection])

            return leftFeed #TODO: ImageTk.PhotoImage(Image.fromarray(leftFeed))
        elif feedSelection == FeedSelections.Right:
            rightFeed = self.getWebcamFrame(self.rightCapture)
            if rightFeed is None:
                return feedToDefaultMap[feedSelection] #TODO: ImageTk.PhotoImage(feedToDefaultMap[feedSelection])

            return rightFeed #TODO: ImageTk.PhotoImage(Image.fromarray(rightFeed))
        elif feedSelection == FeedSelections.Rear:
            rearFeed = self.getWebcamFrame(self.rearCapture)
            if rearFeed is None:
                return feedToDefaultMap[feedSelection] #TODO: ImageTk.PhotoImage(feedToDefaultMap[feedSelection])

            return rearFeed #TODO: ImageTk.PhotoImage(Image.fromarray(rearFeed))


    def recalibrate(self):
        self.stitcher.calibrate()


    def getReading(self):

        readings = {
            CamList.Left: self.leftSensor.getReading()
        }

        '''
        readings = {
            CamList.Left: self.leftSensor.getReading(),
            CamList.Right: self.rightSensor.getReading(),
            CamList.Rear: self.rearSensor.getReading(),

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
