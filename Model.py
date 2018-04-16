from enum import Enum
import numpy as np
import cv2
from Util import *
from image_stitching import Stitcher
from sensor import Sensor
from threading import Thread

import os

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

feedToTitleMap = {
                FeedSelections.Overhead: "Panorama",
                FeedSelections.Left: "Left Camera",
                FeedSelections.Right: "Right Camera",
                FeedSelections.Rear: "Rear Camera"
}

feedListVals = [feedList for feedList in FeedSelections]

class Model:
    def __init__(self, leftCapture, rightCapture, rearCapture, sensorVals):
        self.displayToFeedMap = {
                                DisplaySelection.MainLeft: FeedSelections.Overhead,
                                DisplaySelection.Right: FeedSelections.Overhead
                                }

        prefix = os.path.join(os.getcwd(), 'defaultImages')

        over = cv2.imread(os.path.join(prefix, 'overheadDefault.png'))
        left = cv2.imread(os.path.join(prefix, 'leftDefault.png'))
        right = cv2.imread(os.path.join(prefix, 'rightDefault.png'))
        rear = cv2.imread(os.path.join(prefix, 'rearDefault.png'))

        self.feedToDefaultMap = {
            FeedSelections.Overhead: over,
            FeedSelections.Left: left,
            FeedSelections.Right: right,
            FeedSelections.Rear: rear
        }

        #.resize(400,300) #TODO: Resize


        self.stitcher = Stitcher()

        #TODO: Re-enable sensor code
        #Create the left sensor
        # self.leftSensor = Sensor(sensorVals[CamList.Left][GPIO.TRIG], sensorVals[CamList.Left][GPIO.ECHO])
        #
        # #Run a thread to start the readings
        # t = Thread(target = self.leftSensor.startSensors)
        # t.start()

        self.notificationsMuted = False
        self.leftCapture = leftCapture
        self.rightCapture = rightCapture
        self.rearCapture = rearCapture

    def changeFeed(self, displaySelection, desiredCamSelection):

        if desiredCamSelection == CamList.Left:
            feedSelection = FeedSelections.Left
        elif desiredCamSelection == CamList.Rear:
            feedSelection = FeedSelections.Rear
        else:
            feedSelection = FeedSelections.Right

        self.displayToFeedMap[displaySelection] = feedSelection

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
                rearFeed = self.getWebcamFrame(self.rearCapture, False)

                if leftFeed is None or rightFeed is None or rearFeed is None:
                    return self.feedToDefaultMap[feedSelection], feedToTitleMap[feedSelection]

                stitchedArray = self.stitcher.stitch([leftFeed, rearFeed, rightFeed])
                stitchedImage = stitchedArray
                return stitchedImage, feedToTitleMap[feedSelection]
            except RuntimeError:
                return self.feedToDefaultMap[feedSelection], feedToTitleMap[feedSelection]

        elif feedSelection == FeedSelections.Left:
            leftFeed = self.getWebcamFrame(self.leftCapture)
            if leftFeed is None:
                return self.feedToDefaultMap[feedSelection], feedToTitleMap[feedSelection]

            return leftFeed, feedToTitleMap[feedSelection]
        elif feedSelection == FeedSelections.Right:
            rightFeed = self.getWebcamFrame(self.rightCapture)
            if rightFeed is None:
                return self.feedToDefaultMap[feedSelection], feedToTitleMap[feedSelection]

            return rightFeed, feedToTitleMap[feedSelection]
        elif feedSelection == FeedSelections.Rear:
            rearFeed = self.getWebcamFrame(self.rearCapture, False)
            if rearFeed is None:
                return self.feedToDefaultMap[feedSelection], feedToTitleMap[feedSelection]

            return rearFeed, feedToTitleMap[feedSelection]


    def recalibrate(self):
        try:
            self.stitcher.calibrate()
        except RuntimeError:
            return


    def getReading(self):

        if self.notificationsMuted:
            return {}

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
    def getWebcamFrame(capture, fix_distortion = True):
        ret, frame = capture.read()

        if not ret:
            return None

        if frame.shape[0] != 480:
            frame = cv2.resize(frame, None, fx=0.444444, fy=0.444444)[:, 106:746, :]

        frame_to_display = undistort(frame) if fix_distortion else frame

        return cv2.flip(frame_to_display, 1)




DIM=(640, 480)
K=np.array([[269.6616655760057, 0.0, 322.2636869266894], [0.0, 270.57327145833693, 211.76621398914702], [0.0, 0.0, 1.0]])
D=np.array([[-0.04175871736401356], [-0.0031884652828571736], [0.0006001904789516924], [-0.0009174281553332885]])
def undistort(img):
    h,w = img.shape[:2]
    map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, DIM, cv2.CV_16SC2)
    undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
    return undistorted_img

