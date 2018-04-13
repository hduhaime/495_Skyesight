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

        self.view = view

        buttonMap = {
            "onToggleScreen": self.toggleScreen,
            "onRecalibrate": self.model.recalibrate,
            "onToggleNotifications": self.toggleNotifications,
            "onPrimaryPrev": lambda: self.pressPrev(DisplaySelection.MainLeft),
            "onPrimaryNext": lambda: self.pressNext(DisplaySelection.MainLeft),
            "onSecondaryPrev": lambda: self.pressPrev(DisplaySelection.Right),
            "onSecondaryNext": lambda: self.pressNext(DisplaySelection.Right),
            "onChangeMaxDistance": None #TODO:

        }

        view.initialize(buttonMap)

    def onClose(self):
        self.continueRunning = False

    def run(self):
        while self.continueRunning:
            if(self.view.fxns):

                frame, text = self.model.getFeed(DisplaySelection.MainLeft)

                if self.isFullScreen:

                    self.view.fxns.updatePanel(VideoSelection.Main, frame, text)

                if not self.isFullScreen:
                    self.view.fxns.updatePanel(VideoSelection.Left, frame, text)

                    rightFrame, altText = self.model.getFeed(DisplaySelection.Right)
                    self.view.fxns.updatePanel(VideoSelection.Right, rightFrame, altText)

                #self.root.update_idletasks()
                #self.root.update()

                #TODO: re-integrate sensors
                # sensorToReadingMap = self.model.getReading()
                # closestValue = None
                # closestCamera = None
                # for key, value in sensorToReadingMap:
                #     if closestValue is None:
                #         closestValue = value
                #     elif value is not None:
                #         if closestValue > value:
                #             closestValue = value

                #TODO: to send distance notifications, use view.fxns.sendDistanceNotification(viewType, distance, feedName)
                #   If you call this when a notification is open, it'll update the values instead of reopening
                self.view.fxns.sendDistanceNotification(CamList.Left, 0.52 + random(), "left")

        #self.root.quit()

    def pressNext(self, displaySelection):
        self.model.nextFeed(displaySelection)

    def pressPrev(self, displaySelection):
        self.model.prevFeed(displaySelection)

    def toggleNotifications(self):
        self.notificationsMuted = not self.notificationsMuted
        self.model.toggleNotifications(self.notificationsMuted)
        self.view.fxns.toggleNotifications(self.notificationsMuted)

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

    #TODO: coordinate camera releases (still leftover thread)
    leftCam.release()
    rightCam.release()
    rearCam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()