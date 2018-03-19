# import the necessary packages
from __future__ import print_function
from enum import Enum
import sys
from PIL import Image
from PIL import ImageTk
import tkinter as tki
import threading
import numpy as np
import cv2
from UltrasonicSensor import UltrasonicSensor

import image_stitiching.stitcher.impl.__main__ as stitch_impl


class LayoutSettings(Enum):
    Fullscreen = 1
    Splitscreen = 2


class FeedList(Enum):
    Overhead = 0
    SingleLeft = 1
    SingleRear = 2
    SingleRight = 3
    DualLR = 4  # Dual Left/Rear
    DualRR = 5  # Dual Right/Rear


class FeedModificationButtons(Enum):
    MainPrev = 0
    MainNext = 1
    LeftPrev = 2
    LeftNext = 3
    RightPrev = 4
    RightNext = 5


class ScreenSelections(Enum):
    Main = 0
    SplitLeft = 1
    SplitRight = 2


class Cameras(Enum):
    Rear = 0
    Left = 1
    Right = 2


stitch = stitch_impl.Stitcher()

class Graphics:
    def __init__(self, cam_list):
        self.thread = None
        self.stopEvent = None
        #self.sensor = UltrasonicSensor()
        #print(self.sensor.getReading())
        self.camList = cam_list
        self.camFeeds = {}
        for camera in Cameras:
            self.camFeeds[camera] = None

        self.feedList = {}
        for feed in FeedList:
            self.feedList[feed] = None

        # Set layout, feed, and notification options
        self.layoutSelection = LayoutSettings.Fullscreen
        self.feedSelections = []  # selection of feed to be shown in fullscreen and splitscreen modes
        for i in ScreenSelections:
            self.feedSelections.append(FeedList.SingleRear)

        self.notificationsMuted = False

        # make panels for images
        self.fullScreenPanel = None
        # splitscreen panels
        self.splitLeftPanel = None
        self.splitRightPanel = None

        # initialize the root window
        self.root = tki.Tk()
        self.root.geometry('800x600')
        for i in range(12):
            self.root.grid_columnconfigure(i, weight=1)

        self.root.grid_rowconfigure(0, weight=2)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)

        # Format buttons on bottom of screen
        self.selectLayoutBtn = tki.Button(self.root, text="Make Splitscreen",
                                          command=self.switch_to_splitscreen)
        self.selectLayoutBtn.grid(row=2, column=0, columnspan=6, sticky='nesw')

        self.muteNotificationsBtn = tki.Button(self.root, text="Mute Notifications",
                                               command=self.mute_unmute_notifications)
        self.muteNotificationsBtn.grid(row=2, column=6, columnspan=6, sticky='nesw')


        # Put feed toggle buttons under main feed
        self.toggleFeedBtns = []
        self.toggleFeedBtns.append(tki.Button(self.root, text="Prev Feed",
                                              command=lambda: self.prev_feed(ScreenSelections.Main)))
        self.toggleFeedBtns[FeedModificationButtons.MainPrev.value].grid(row=1, column=4, columnspan=2, sticky='nesw')

        self.toggleFeedBtns.append(tki.Button(self.root, text="Next Feed",
                                              command=lambda: self.next_feed(ScreenSelections.Main)))
        self.toggleFeedBtns[FeedModificationButtons.MainNext.value].grid(row=1, column=6, columnspan=2, sticky='nesw')


        # Buttons for splitscreen mode
        self.toggleFeedBtns.append(tki.Button(self.root, text="Prev Feed",
                                              command=lambda: self.prev_feed(ScreenSelections.SplitLeft)))
        self.toggleFeedBtns.append(tki.Button(self.root, text="Next Feed",
                                              command=lambda: self.next_feed(ScreenSelections.SplitLeft)))

        self.toggleFeedBtns.append(tki.Button(self.root, text="Prev Feed",
                                              command=lambda: self.prev_feed(ScreenSelections.SplitRight)))
        self.toggleFeedBtns.append(tki.Button(self.root, text="Next Feed",
                                              command=lambda: self.next_feed(ScreenSelections.SplitRight)))


        # start a thread that constantly pools the video sensor for
        # the most recently read frame
        self.stopEvent = threading.Event()
        self.thread = threading.Thread(target=self.video_loop, args=())
        self.thread.start()

        # set a callback to handle when the window is closed
        self.root.wm_title("Skyesight")
        
        self.root.wm_protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        # set the stop event, cleanup the camera, and allow the rest of
        # the quit process to continue
        print("[INFO] closing...")
        self.stopEvent.set()
        self.root.quit()

    def video_loop(self):
        while not self.stopEvent.is_set():

            # Capture Input
            keyVal = cv2.waitKey(1)
            if keyVal & 0xFF == ord('q'):
                break
            if keyVal & 0xFF == ord('a'):
                stitch.calibrate()

            for camera in Cameras:
                if len(self.camList) > camera.value:
                    # Get frame from video feeds
                    self.camFeeds[camera] = self.get_webcam_frame(self.camList[camera.value])

                    # update the actual feeds with displayable image data
                    self.update_feed(camera)

            if len(self.camList) == 2:
                # update feeds where 2 images are stitched together
                # TODO: need to do this
                print("do this pls")

            #if len(self.camList) == 3:
            #    # update feeds where 3 images are stitched together
            #    feedsToStitch = [self.camFeeds[Cameras.Left],
            #                self.camFeeds[Cameras.Rear],
            #                self.camFeeds[Cameras.Right]]
            #    self.feedList[FeedList.Overhead] = stitch.stitch(feedsToStitch)

            # update shown panels
            self.update_panels()

    def update_feed(self, camera):
        try:
            # Convert array from BGR to RGB and then to tkinter image
            img_array = cv2.cvtColor(self.camFeeds[camera], cv2.COLOR_BGR2RGB)
            image = Image.fromarray(img_array)
            image = ImageTk.PhotoImage(image)

            if camera.value == Cameras.Rear.value:
                self.feedList[FeedList.SingleRear] = image
            elif camera.value == Cameras.Left.value:
                self.feedList[FeedList.SingleLeft] = image
            elif camera.value == Cameras.Right.value:
                self.feedList[FeedList.SingleRight] = image

        except RuntimeError as e:
            print("[INFO] caught a RuntimeError")


    def update_panels(self):
        fullScreenFeedSelection = self.feedSelections[ScreenSelections.Main.value]
        fullScreenFeed = self.feedList[fullScreenFeedSelection]

        splitLeftFeedSelection = self.feedSelections[ScreenSelections.SplitLeft.value]
        splitLeftFeed = self.feedList[splitLeftFeedSelection]

        splitRightFeedSelection = self.feedSelections[ScreenSelections.SplitRight.value]
        splitRightFeed = self.feedList[splitRightFeedSelection]

        # initialize panel if it has not been yet
        if self.fullScreenPanel is None:
            self.fullScreenPanel = tki.Label(image=fullScreenFeed, width=300, height=300)
            self.fullScreenPanel.grid(row=0, column=2, columnspan=8)
            self.fullScreenPanel.image = fullScreenFeed

            self.splitLeftPanel = tki.Label(image=splitLeftFeed, width=300, height=300)
            self.splitLeftPanel.image = splitLeftFeed

            self.splitRightPanel = tki.Label(image=splitRightFeed, width=300, height=300)
            self.splitRightPanel.image = splitRightFeed

        # otherwise, update the panel
        else:
            if self.layoutSelection.value == LayoutSettings.Fullscreen.value:
                self.fullScreenPanel.configure(image=fullScreenFeed)
                self.fullScreenPanel.image = fullScreenFeed
            else:
                # splitscreen so update the two panels
                self.splitLeftPanel.configure(image=splitLeftFeed)
                self.splitLeftPanel.image = splitLeftFeed

                self.splitRightPanel.configure(image=splitRightFeed)
                self.splitRightPanel.image = splitRightFeed


    def get_webcam_frame(self, capture):
        ret, frame = capture.read()
        frame_to_display = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
        if frame_to_display.shape[0] != 480:
            frame_to_display = cv2.resize(frame_to_display, None, fx=0.444444, fy=0.444444)[:, 106:746, :]

        return cv2.flip(frame_to_display, 1)

    def switch_to_fullscreen(self):
        self.layoutSelection = LayoutSettings.Fullscreen
        self.selectLayoutBtn.config(text="Make Splitscreen", command=self.switch_to_splitscreen)

        # remove splitscreen things from the window
        self.splitLeftPanel.grid_forget()
        self.splitRightPanel.grid_forget()
        self.toggleFeedBtns[FeedModificationButtons.LeftPrev.value].grid_forget()
        self.toggleFeedBtns[FeedModificationButtons.LeftNext.value].grid_forget()
        self.toggleFeedBtns[FeedModificationButtons.RightPrev.value].grid_forget()
        self.toggleFeedBtns[FeedModificationButtons.RightNext.value].grid_forget()

        # put fullscreeen things into window
        self.toggleFeedBtns[FeedModificationButtons.MainPrev.value].grid(row=1, column=4, columnspan=2, sticky='nesw')
        self.toggleFeedBtns[FeedModificationButtons.MainNext.value].grid(row=1, column=6, columnspan=2, sticky='nesw')
        self.fullScreenPanel.grid(row=0, column=2, columnspan=8)
        self.fullScreenPanel.configure(height=300, width=300)

    def switch_to_splitscreen(self):
        self.layoutSelection = LayoutSettings.Splitscreen
        self.selectLayoutBtn.config(text="Make Fullscreen", command=self.switch_to_fullscreen)
        self.fullScreenPanel.grid_forget()
        self.toggleFeedBtns[FeedModificationButtons.MainPrev.value].grid_forget()
        self.toggleFeedBtns[FeedModificationButtons.MainNext.value].grid_forget()
        self.splitLeftPanel.grid(row=0, columnspan=6)
        self.splitRightPanel.grid(row=0, column=6, columnspan=6)
        self.splitLeftPanel.configure(width=300, height=300)
        self.splitRightPanel.configure(width=300, height=300)
        self.toggleFeedBtns[FeedModificationButtons.LeftPrev.value].grid(row=1, column=1, columnspan=2, sticky="nesw")
        self.toggleFeedBtns[FeedModificationButtons.LeftNext.value].grid(row=1, column=3, columnspan=2, sticky="nesw")
        self.toggleFeedBtns[FeedModificationButtons.RightPrev.value].grid(row=1, column=7, columnspan=2, sticky="nesw")
        self.toggleFeedBtns[FeedModificationButtons.RightNext.value].grid(row=1, column=9, columnspan=2, sticky="nesw")

    def prev_feed(self, feedSelection):
        current = self.feedSelections[feedSelection.value]
        feedListVals = [feedList.value for feedList in FeedList]
        self.feedSelections[feedSelection.value] = FeedList(feedListVals[current.value - 1])

    def next_feed(self, feedSelection):
        current = self.feedSelections[feedSelection.value]
        feedListVals = [feedList.value for feedList in FeedList]
        self.feedSelections[feedSelection.value] = FeedList((feedListVals[current.value] + 1) % len(feedListVals))

    def mute_unmute_notifications(self):
        if self.notificationsMuted:
            self.notificationsMuted = False
            self.muteNotificationsBtn.config(text="Mute Notifications")
        else:
            self.notificationsMuted = True
            self.muteNotificationsBtn.config(text="Unmute Notifications")


def main():
    num_cams = int(sys.argv[1])

    # Get camera feeds
    cam_list= []
    for x in range(0, num_cams):
        cam_list.append(cv2.VideoCapture(x))

    g = Graphics(cam_list)
    g.root.mainloop()
    g.root.destroy()

    # When everything done, release the capture
    for cam in cam_list:
        cam.release()

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
