# import tkinter as tki
import cv2

from Model import Model
from View import viewApp as View
from Model import GPIO
from Util import *
import threading

#TODO
from random import *

class Controller:
    def __init__(self, view, leftCapture, rightCapture, rearCapture, sensorVals):
        self.model = Model(leftCapture, rightCapture, rearCapture, sensorVals)
        self.notificationsMuted = False
        self.isFullScreen = True
        self.continueRunning = True
        self.sensorToIsValidMap = {CamList.Left: True, CamList.Right: True, CamList.Rear: True}
        self.distanceThreshold = 1.5 #TODO: change this to a global default value
        self.view = view

        self.sensorMapLock = threading.Lock()

        buttonMap = {
            "onToggleScreen": self.toggleScreen,
            "onRecalibrate": self.model.recalibrate,
            "onToggleNotifications": self.toggleNotifications,
            "onPrimaryPrev": lambda: self.pressPrev(DisplaySelection.MainLeft),
            "onPrimaryNext": lambda: self.pressNext(DisplaySelection.MainLeft),
            "onSecondaryPrev": lambda: self.pressPrev(DisplaySelection.Right),
            "onSecondaryNext": lambda: self.pressNext(DisplaySelection.Right)
        }

        buttonMapArgs = {
            "onDismissNotification": self.acknowledgeDistNotification,
            "onGotoNotification" : self.changeFeed,
            "onChangeDistanceRange" : self.changeDistanceThreshold
        }

        view.initialize(buttonMap, buttonMapArgs)

    def onClose(self):
        self.continueRunning = False

    def run(self):
        while self.continueRunning:
            if self.view.fxns:

                frame, text = self.model.getFeed(DisplaySelection.MainLeft)

                if self.isFullScreen:
                    self.view.fxns.updatePanel(VideoSelection.Main, frame, text)

                if not self.isFullScreen:
                    self.view.fxns.updatePanel(VideoSelection.Left, frame, text)

                    rightFrame, altText = self.model.getFeed(DisplaySelection.Right)
                    self.view.fxns.updatePanel(VideoSelection.Right, rightFrame, altText)



                sensorToReadingMap = {
                    CamList.Left: 1.3,
                    CamList.Rear: 4.2,
                    CamList.Right: 0.4

                } #TODO: self.model.getReading()
                for key, value in sensorToReadingMap.items():

                    self.sensorMapLock.acquire()

                    # make sensor valid again if we go out of threshold
                    if value > self.distanceThreshold and not self.sensorToIsValidMap[key]:
                        self.sensorToIsValidMap[key] = True

                    # send distance notification to view if sensor is valid and in threshold
                    if self.sensorToIsValidMap[key] and self.distanceThreshold >= value:
                        self.view.fxns.sendDistanceNotification(key, value, camToNameMap[key])
                        #TODO: do we want a queue with the closest distance at the highest priority?

                    self.sensorMapLock.release()

    def pressNext(self, displaySelection):
        self.model.nextFeed(displaySelection)

    def pressPrev(self, displaySelection):
        self.model.prevFeed(displaySelection)

    def changeFeed(self, desiredCamSelection):
        self.acknowledgeDistNotification(desiredCamSelection)
        self.model.changeFeed(DisplaySelection.MainLeft, desiredCamSelection)

    def changeDistanceThreshold(self, distance):
        self.distanceThreshold = distance

    def toggleNotifications(self):
        self.model.toggleNotifications(self.notificationsMuted)
        self.view.fxns.toggleNotifications(self.notificationsMuted)

    def acknowledgeDistNotification(self, camSelection):
        self.sensorMapLock.acquire()
        self.sensorToIsValidMap[camSelection] = False
        self.sensorMapLock.release()

    def toggleScreen(self):
        if self.isFullScreen:
            self.isFullScreen = False
            self.view.fxns.makeSplitScreen()
        else:
            self.isFullScreen = True
            self.view.fxns.makeFullScreen()



controller = None #TODO: ensure this doesn't cause controller_thread to go out of scope
def main():

    view = View()

    #For Henry's laptop: 0, 1, 2

    leftCam = cv2.VideoCapture(0)
    rightCam = cv2.VideoCapture(3)
    rearCam = cv2.VideoCapture(2)

    sensorVals = {
        CamList.Left : {
                        GPIO.TRIG: 4,
                        GPIO.ECHO: 18
                    }
    }
    controller = Controller(view, leftCam, rightCam, rearCam, sensorVals)
    controller_thread = threading.Thread(target=lambda: controller.run())
    controller_thread.start()

    view.run()

    # wait for controller run thread to end
    controller.onClose()
    controller_thread.join()

    leftCam.release()
    rightCam.release()
    rearCam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()