# import tkinter as tki
import cv2

from Model import Model
from View import viewApp as View
from Util import *
import threading


class Controller:
    def __init__(self, view, leftCapture, rightCapture, rearCapture, sensorVals):
        self.model = Model(leftCapture, rightCapture, rearCapture, sensorVals)
        self.notificationsMuted = True
        self.isFullScreen = True
        self.color = True
        self.continueRunning = True
        self.sensorToIsValidMap = {CamList.Left: True, CamList.Right: True, CamList.Rear: True}
        self.distanceThreshold = 1.5
        self.view = view
        self.color_lock = threading.Lock()
        self.distance_lock = threading.Lock()

        self.sensorMapLock = threading.Lock()

        buttonMap = {
            "onToggleScreen": self.toggleScreen,
            "onRecalibrate": self.model.recalibrate,
            "onToggleNotifications": self.toggleNotifications,
            "onPrimaryPrev": lambda: self.pressPrev(DisplaySelection.MainLeft),
            "onPrimaryNext": lambda: self.pressNext(DisplaySelection.MainLeft),
            "onSecondaryPrev": lambda: self.pressPrev(DisplaySelection.Right),
            "onSecondaryNext": lambda: self.pressNext(DisplaySelection.Right),
            "onPressSKey": self.toggleColorMode
        }

        buttonMapArgs = {
            "onDismissNotification": self.acknowledgeDistNotification,
            "onGotoNotification" : self.changeFeed,
            "onChangeDistanceRange" : self.changeDistanceThreshold
        }

        view.initialize(buttonMap, buttonMapArgs)

    def stop(self):
        self.continueRunning = False
        self.model.stop()

    def run(self):
        while self.continueRunning:
            #keyVal = cv2.waitKey(1)
            #if keyVal & 0xFF == ord('b'):
            #    self.color = not self.color
            if self.view.fxns:

                self.color_lock.acquire()

                frame, text = self.model.getFeed(DisplaySelection.MainLeft, self.color)
                if len(frame.shape) > 2 and not self.color:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2GRAY)

                if self.isFullScreen:
                    self.view.fxns.updatePanel(VideoSelection.Main, frame, self.color, text)

                if not self.isFullScreen:
                    self.view.fxns.updatePanel(VideoSelection.Left, frame, self.color, text)

                    rightFrame, altText = self.model.getFeed(DisplaySelection.Right, self.color)
                    if len(rightFrame.shape) > 2 and not self.color:
                        rightFrame = cv2.cvtColor(rightFrame, cv2.COLOR_BGRA2GRAY)
                    self.view.fxns.updatePanel(VideoSelection.Right, rightFrame, self.color, altText)

                self.color_lock.release()

                self.sensorMapLock.acquire()
                sensorToReadingMap = self.model.getReading()
                for key, value in sensorToReadingMap.items():
                    if value is None:
                        continue



                    # make sensor valid again if we go out of threshold
                    if value > self.distanceThreshold and not self.sensorToIsValidMap[key]:
                        self.sensorToIsValidMap[key] = True

                    # send distance notification to view if sensor is valid and in threshold
                    if self.sensorToIsValidMap[key] and self.distanceThreshold >= value:
                        self.view.fxns.sendDistanceNotification(key, value, camToNameMap[key])

                self.sensorMapLock.release()

    def pressNext(self, displaySelection):
        self.model.nextFeed(displaySelection)

    def pressPrev(self, displaySelection):
        self.model.prevFeed(displaySelection)

    def changeFeed(self, desiredCamSelection):
        self.acknowledgeDistNotification(desiredCamSelection)
        self.model.changeFeed(DisplaySelection.MainLeft, desiredCamSelection)

    def changeDistanceThreshold(self, distance):
        self.sensorMapLock.acquire()
        self.distanceThreshold = distance
        self.sensorMapLock.release()

    def toggleNotifications(self):
        self.notificationsMuted = not self.notificationsMuted
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


    def toggleColorMode(self):
        self.color_lock.acquire()
        self.color = not self.color
        self.color_lock.release()


def main():

    view = View()

    #For Henry's laptop: 0, 1, 2

    leftCam = cv2.VideoCapture(2)
    rightCam = cv2.VideoCapture(3)
    rearCam = cv2.VideoCapture(0)

    sensorVals = {
        CamList.Left : {
                        GPIO.TRIG: 21,
                        GPIO.ECHO: 26
                    },

        CamList.Rear: {
                        GPIO.TRIG: 20,
                        GPIO.ECHO: 19
                    },

        CamList.Right: {
                        GPIO.TRIG: 16,
                        GPIO.ECHO: 13
                    }
    }
    controller = Controller(view, leftCam, rightCam, rearCam, sensorVals)
    controller_thread = threading.Thread(target=lambda: controller.run())
    controller_thread.start()

    view.run()

    # wait for controller run thread to end
    controller.stop()
    controller_thread.join()

    leftCam.release()
    rightCam.release()
    rearCam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
