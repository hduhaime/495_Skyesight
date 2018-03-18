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

import image_stitiching.stitcher.impl.__main__ as stitch_impl
import menuSelections


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


class FeedScreens(Enum):
    Main = 0
    SplitLeft = 1
    SplitRight = 2

stitch = stitch_impl.Stitcher()
SCREEN_IDX = 1


class Graphics:
    def __init__(self, cam_list):
        self.cam_list = cam_list
        self.thread = None
        self.stopEvent = None

        # Set layout, feed, and notification options
        self.layoutSelection = LayoutSettings.Fullscreen
        self.feedSelections = []
        for i in FeedScreens:
            self.feedSelections.append(FeedList.Overhead)

        self.notificationsMuted = False

        # Menus
        self.layoutMenu = None
        self.selectFeedMenu = None

        # make panels for images
        self.fullScreenPanel = None
        # splitscreen panels
        self.splitLeftPanel = None
        self.splitRightPanel = None

        # initialize the root window
        self.root = tki.Tk()
        self.root.wm_state('zoomed')
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)
        self.root.grid_columnconfigure(3, weight=1)
        self.root.grid_columnconfigure(4, weight=1)
        self.root.grid_columnconfigure(5, weight=1)
        self.root.grid_columnconfigure(6, weight=1)
        self.root.grid_columnconfigure(7, weight=1)
        self.root.grid_columnconfigure(8, weight=1)
        self.root.grid_columnconfigure(9, weight=1)
        self.root.grid_columnconfigure(10, weight=1)
        self.root.grid_columnconfigure(11, weight=1)
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
                                              command=lambda: self.prev_feed(FeedScreens.Main)))
        self.toggleFeedBtns[FeedModificationButtons.MainPrev.value].grid(row=1, column=4, columnspan=2, sticky='nesw')

        self.toggleFeedBtns.append(tki.Button(self.root, text="Next Feed",
                                          command=lambda: self.next_feed(FeedScreens.Main)))
        self.toggleFeedBtns[FeedModificationButtons.MainNext.value].grid(row=1, column=6, columnspan=2, sticky='nesw')


        # Buttons for splitscreen mode
        self.toggleFeedBtns.append(tki.Button(self.root, text="Prev Feed",
                                     command=lambda: self.prev_feed(FeedScreens.Main)))
        self.toggleFeedBtns.append(tki.Button(self.root, text="Next Feed",
                                          command=lambda: self.next_feed(FeedScreens.Main)))

        self.toggleFeedBtns.append(tki.Button(self.root, text="Prev Feed",
                                       command=lambda: self.prev_feed(FeedScreens.Main)))
        self.toggleFeedBtns.append(tki.Button(self.root, text="Next Feed",
                                          command=lambda: self.next_feed(FeedScreens.Main)))


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
        x = 0
        while not self.stopEvent.is_set():

            # Capture Input
            keyVal = cv2.waitKey(1)
            if keyVal & 0xFF == ord('q'):
                break
            if keyVal & 0xFF == ord('a'):
                stitch.calibrate()

            global SCREEN_IDX
            if keyVal & 0xFF == ord('1'):
                SCREEN_IDX = 1
            elif keyVal & 0xFF == ord('2'):
                SCREEN_IDX = 2
            elif keyVal & 0xFF == ord('3'):
                SCREEN_IDX = 3
            elif keyVal & 0xFF == ord('4'):
                SCREEN_IDX = 4

            # Get frame from video feeds
            cam_feeds = [self.get_webcam_frame(x) for x in self.cam_list]

            height, width, channels = cam_feeds[0].shape

            if np.any(self.cam_list == None):
                continue
            else:
                x += 1

            self.display_multiple_feeds(*cam_feeds)

    def display_multiple_feeds(self, *args):
        arglist = []
        for arg in args:
            arglist.append(arg)

        if (len(args) == 1):
            # Don't concatenate if only one image
            # if the panel is not None, we need to initialize it
            self.display_feed(*args)

        else:
            # Concatenate images in list and scale them so that they all fit on screen

            # REMOVE THIS LINE FOR 3 CAMERAS TO WORK AGAAIN YOU FOOOOOOL
            arglist.append(arglist[-1])
            stitched_image = stitch.stitch(arglist)

            # Show feed L
            if (SCREEN_IDX == 1):
                cv2.imshow('Output', args[0])
            # Show feed M
            elif (SCREEN_IDX == 2):
                cv2.imshow('Output', args[1])
            # Show feed R
            elif (SCREEN_IDX == 3):
                cv2.imshow('Output', args[2])
            # Show stitched feed
            else:
                cv2.imshow('Output', stitched_image)
            # image_to_show = cv2.resize(np.concatenate(arglist, axis=1), None, fx=0.6666, fy=0.6666)
            # cv2.imshow('frame', image_to_show)

    def display_feed(self, img_array):
        try:
            # Convert array from BGR to RGB and then to tkinter image
            img_array = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(img_array)
            image = ImageTk.PhotoImage(image)

            # initialize panel if it has not been yet
            if self.fullScreenPanel is None:
                self.fullScreenPanel = tki.Label(image=image)
                self.fullScreenPanel.grid(row=0, column=2, columnspan=8)
                self.fullScreenPanel.image = image

                self.splitLeftPanel = tki.Label(image=image)
                self.splitLeftPanel.image = image
                self.splitRightPanel = tki.Label(image=image)
                self.splitRightPanel.image = image

            # otherwise, update the panel
            else:
                if self.layoutSelection.value == LayoutSettings.Fullscreen.value:
                    self.fullScreenPanel.configure(image=image)
                    self.fullScreenPanel.image = image
                else:
                    # splitscreen so update the two panels
                    # TODO: move this to calling function if there is more than one feed
                    self.splitLeftPanel.configure(image=image)
                    self.splitLeftPanel.image = image
                    self.splitRightPanel.configure(image=image)
                    self.splitRightPanel.image = image


        except RuntimeError as e:
            print("[INFO] caught a RuntimeError")

    def get_webcam_frame(self, capture):
        ret, frame = capture.read()
        frame_to_display = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
        if frame_to_display.shape[0] != 480:
            frame_to_display = cv2.resize(frame_to_display, None, fx=0.444444, fy=0.444444)[:, 106:746, :]

        return cv2.flip(frame_to_display, 1)

    def create_select_layout_window(self):
        self.layoutMenu = menuSelections.LayoutMenu(self)

    def create_select_feed_window(self):
        self.selectFeedMenu = menuSelections.FeedMenu(self)

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

    def switch_to_splitscreen(self):
        self.layoutSelection = LayoutSettings.Splitscreen
        self.selectLayoutBtn.config(text="Make Fullscreen", command=self.switch_to_fullscreen)
        self.fullScreenPanel.grid_forget()
        self.toggleFeedBtns[FeedModificationButtons.MainPrev.value].grid_forget()
        self.toggleFeedBtns[FeedModificationButtons.MainNext.value].grid_forget()
        self.splitLeftPanel.grid(row=0, columnspan=6)
        self.splitRightPanel.grid(row=0, column=6, columnspan=6)
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
        self.feedSelections[feedSelection.value] = FeedList(feedListVals[current.value] + 1)

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
    cam_list = []
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
