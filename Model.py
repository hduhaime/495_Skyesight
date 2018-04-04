from enum import Enum
import cv2
from PIL import Image
from PIL import ImageTk
from Util import DisplaySelection
import image_stitiching.stitcher.impl.__main__ as stitch_impl


class FeedSelections(Enum):
    Overhead = 0
    Left = 1
    Rear = 2
    Right = 3


class CamList(Enum):
    Left = 0
    Right = 1
    Rear = 2


feedToCamMap = {
                FeedSelections.Overhead: [CamList.Left, CamList.Right, CamList.Rear],
                FeedSelections.Left: CamList.Left,
                FeedSelections.Right: CamList.Right,
                FeedSelections.Rear: CamList.Rear
                }

feedListVals = [feedList.value for feedList in FeedSelections]

class Model:
    def __init__(self, leftCapture, rightCapture, rearCapture):
        self.displayToFeedMap = {
                                DisplaySelection.MainLeft: FeedSelections.Right,
                                DisplaySelection.Right: FeedSelections.Right
                                }

        self.stitcher = stitch_impl.Stitcher()
        self.notificationsMuted = False
        self.leftCapture = leftCapture
        self.rightCapture = rightCapture
        self.rearCapture = rearCapture

        self.nextFeed(DisplaySelection.MainLeft)
        self.nextFeed(DisplaySelection.Right)


    def nextFeed(self, displaySelection):
        self.updateToNextValidFeed(displaySelection, lambda curSelection: (curSelection.value + 1) % len(feedListVals))

    def prevFeed(self, displaySelection):
        self.updateToNextValidFeed(displaySelection,
                lambda curSelection: len(feedListVals) - 1 if curSelection.value == 0 else curSelection.value - 1)

    def updateToNextValidFeed(self, displaySelection, getNextSelection):
        curSelection = self.displayToFeedMap[displaySelection]
        potentialFeed = curSelection

        while True:
            potentialFeed = FeedSelections(feedListVals[getNextSelection(potentialFeed)])
            if self.feedIsValid(potentialFeed):
                break

        self.displayToFeedMap[displaySelection] = potentialFeed


    def feedIsValid(self, feed):
        if feed == FeedSelections.Overhead:
            leftRet, frame = self.leftCapture.read()
            rightRet, frame = self.rightCapture.read()
            rearRet, frame = self.rearCapture.read()

            return leftRet and rightRet and rearRet

        elif feed == FeedSelections.Left:
            ret, frame = self.leftCapture.read()
            return ret
        elif feed == FeedSelections.Right:
            ret, frame = self.rightCapture.read()
            return ret
        elif feed == FeedSelections.Rear:
            ret, frame = self.rearCapture.read()
            return ret

    def toggleNotifications(self, notificationsMuted):
        self.notificationsMuted = notificationsMuted

    def getFeed(self, displaySelection):
        # Get the needed feeds for the relevant display selection
        feedSelection = self.displayToFeedMap[displaySelection]

        if feedSelection == FeedSelections.Overhead:
            # Pull from all feeds and stitch them together
            leftFeed = self.getWebcamFrame(self.leftCapture)
            rightFeed = self.getWebcamFrame(self.rightCapture)
            rearFeed = self.getWebcamFrame(self.rearCapture)
            stitchedArray = self.stitcher.stitch([leftFeed, rightFeed, rearFeed])
            stitchedImage = ImageTk.PhotoImage(Image.fromarray(stitchedArray))
            return stitchedImage
        elif feedSelection == FeedSelections.Left:
            leftFeed = self.getWebcamFrame(self.leftCapture)
            return ImageTk.PhotoImage(Image.fromarray(leftFeed))
        elif feedSelection == FeedSelections.Right:
            rightFeed = self.getWebcamFrame(self.rightCapture)
            return ImageTk.PhotoImage(Image.fromarray(rightFeed))
        elif feedSelection == FeedSelections.Rear:
            rearFeed = self.getWebcamFrame(self.rearCapture)
            return ImageTk.PhotoImage(Image.fromarray(rearFeed))


    def recalibrate(self):
        self.stitcher.calibrate()


    def getWebcamFrame(self, capture):
        ret, frame = capture.read()
        frame_to_display = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        if frame_to_display.shape[0] != 480:
            frame_to_display = cv2.resize(frame_to_display, None, fx=0.444444, fy=0.444444)[:, 106:746, :]

        return cv2.flip(frame_to_display, 1)