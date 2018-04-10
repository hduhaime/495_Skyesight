# import tkinter as tki
import cv2

from Model import Model
from View import viewApp as View
from Util import OnScreenButtons
from Util import DisplaySelection

import threading


class Controller:
    def __init__(self, leftCapture, rightCapture, rearCapture):
        self.model = Model(leftCapture, rightCapture, rearCapture)
        self.notificationsMuted = False
        self.isFullScreen = True
        self.continueRunning = True

        #TODO:
        # initialize tkinter components and View
        # self.root = tki.Tk()
        # set a callback to handle when the window is closed
        # self.root.wm_title("Skyesight")
        # self.root.wm_protocol("WM_DELETE_WINDOW", self.onClose)

        # buttonMap = {OnScreenButtons.FullSplitscreenToggle: tki.Button(self.root, text="Make Splitscreen",
        #                                                     command=self.toggleScreen),
        #              OnScreenButtons.Recalibrate: tki.Button(self.root, text="Recalibrate",
        #                                             command=self.model.recalibrate),
        #              OnScreenButtons.ToggleNotifications: tki.Button(self.root, text="Mute Notifications",
        #                                                     command=self.toggleNotifications),
        #              OnScreenButtons.MainLeftPrevFeed: tki.Button(self.root, text="Prev Feed",
        #                                                 command=lambda: self.pressPrev(DisplaySelection.MainLeft)),
        #              OnScreenButtons.MainLeftNextFeed: tki.Button(self.root, text="Next Feed",
        #                                                 command=lambda: self.pressNext(DisplaySelection.MainLeft)),
        #              OnScreenButtons.RightPrevFeed: tki.Button(self.root, text="Prev Feed",
        #                                             command=lambda: self.pressPrev(DisplaySelection.Right)),
        #              OnScreenButtons.RightNextFeed: tki.Button(self.root, text="Next Feed",
        #                                             command=lambda: self.pressNext(DisplaySelection.Right))}

        buttonMap = {
            "onToggleScreen": self.toggleScreen,
            "onRecalibrate": self.model.recalibrate,
            "onToggleNotifications": self.toggleNotifications,
            "onPrimaryPrev": self.pressPrev(DisplaySelection.MainLeft),
            "onPrimaryNext": lambda: self.pressNext(DisplaySelection.MainLeft),
            "onSecondaryPrev": lambda: self.pressPrev(DisplaySelection.Right),
            "onSecondaryNext": lambda: self.pressNext(DisplaySelection.Right),
            "onChangeMaxDistance": None #TODO:

        }
        self.view = View(buttonMap)
        print("CREATE_VIEW")
        back_thread = threading.Thread(target=self.view.run)
        back_thread.setDaemon(True)
        back_thread.start()
        #self.view.run()
        print("RUN_VIEW")


    def onClose(self):
        self.continueRunning = False

    def run(self):
        print("HERE")
        while self.continueRunning:
            if(self.view.fxns): #TODO: Wait until fxns object is initialized
                frame = self.model.getFeed(DisplaySelection.MainLeft)
                self.view.fxns.updatePanel(DisplaySelection.MainLeft, frame)

                if not self.isFullScreen:
                    rightFrame = self.model.getFeed(DisplaySelection.Right)
                    self.view.fxns.updatePanel(DisplaySelection.Right, rightFrame)

                #self.root.update_idletasks()
                #self.root.update()

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


def main():
    leftCam = cv2.VideoCapture(0)
    rightCam = cv2.VideoCapture(1)
    rearCam = cv2.VideoCapture(2)

    controller = Controller(leftCam, rightCam, rearCam)
    controller.run()

    leftCam.release()
    rightCam.release()
    rearCam.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()