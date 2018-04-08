import tkinter as tki
import cv2

from Model import Model
from View import View
from Util import OnScreenButtons
from Util import DisplaySelection


class Controller:
    def __init__(self, leftCapture, rightCapture, rearCapture, sensorVals):
        self.model = Model(leftCapture, rightCapture, rearCapture, sensorVals)
        self.notificationsMuted = False
        self.isFullScreen = True
        self.continueRunning = True

        # initialize tkinter components and View
        self.root = tki.Tk()
        # set a callback to handle when the window is closed
        self.root.wm_title("Skyesight")
        self.root.wm_protocol("WM_DELETE_WINDOW", self.onClose)

        buttonMap = {OnScreenButtons.FullSplitscreenToggle: tki.Button(self.root, text="Make Splitscreen",
                                                            command=self.toggleScreen),
                     OnScreenButtons.Recalibrate: tki.Button(self.root, text="Recalibrate",
                                                    command=self.model.recalibrate),
                     OnScreenButtons.ToggleNotifications: tki.Button(self.root, text="Mute Notifications",
                                                            command=self.toggleNotifications),
                     OnScreenButtons.MainLeftPrevFeed: tki.Button(self.root, text="Prev Feed",
                                                        command=lambda: self.pressPrev(DisplaySelection.MainLeft)),
                     OnScreenButtons.MainLeftNextFeed: tki.Button(self.root, text="Next Feed",
                                                        command=lambda: self.pressNext(DisplaySelection.MainLeft)),
                     OnScreenButtons.RightPrevFeed: tki.Button(self.root, text="Prev Feed",
                                                    command=lambda: self.pressPrev(DisplaySelection.Right)),
                     OnScreenButtons.RightNextFeed: tki.Button(self.root, text="Next Feed",
                                                    command=lambda: self.pressNext(DisplaySelection.Right))}
        self.view = View(self.root, buttonMap)

    def onClose(self):
        self.continueRunning = False

    def run(self):
        while self.continueRunning:
            frame = self.model.getFeed(DisplaySelection.MainLeft)
            self.view.updatePanel(DisplaySelection.MainLeft, frame)

            if not self.isFullScreen:
                rightFrame = self.model.getFeed(DisplaySelection.Right)
                self.view.updatePanel(DisplaySelection.Right, rightFrame)

            self.root.update_idletasks()
            self.root.update()

        self.root.quit()

    def pressNext(self, displaySelection):
        self.model.nextFeed(displaySelection)

    def pressPrev(self, displaySelection):
        self.model.prevFeed(displaySelection)

    def toggleNotifications(self):
        self.notificationsMuted = not self.notificationsMuted
        self.model.toggleNotifications(self.notificationsMuted)
        self.view.toggleNotifications(self.notificationsMuted)

    def toggleScreen(self):
        if self.isFullScreen:
            self.isFullScreen = False
            self.view.makeSplitScreen()
        else:
            self.isFullScreen = True
            self.view.makeFullScreen()


def main():
    leftCam = cv2.VideoCapture(0)
    rightCam = cv2.VideoCapture(1)
    rearCam = cv2.VideoCapture(2)

    sensorVals = {
        SensorList.Left : {
                        GPIO.TRIG: 4,
                        GPIO.ECHO: 18
                    }
    }
    controller = Controller(leftCam, rightCam, rearCam, sensorVals)
    controller.run()

    leftCam.release()
    rightCam.release()
    rearCam.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()