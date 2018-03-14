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


stitch = stitch_impl.Stitcher()
SCREEN_IDX = 1


class Graphics:
    def __init__(self, cam_list):
        self.thread = None
        self.stopEvent = None

        # Set layout, feed, and notification options
        self.layoutSelection = LayoutSettings.Fullscreen
        self.feedSelection = FeedList.Overhead
        self.notificationsMuted = False

        # Menus
        self.layoutMenu = None
        self.selectFeedMenu = None

        # initialize the root window
        self.root = tki.Tk()
        self.root.attributes('-fullscreen', True)

        # Format three buttons on bottom of screen
        self.selectLayoutBtn = tki.Button(self.root, text="Select Layout",
                                          command=self.create_select_layout_window)
        self.selectLayoutBtn.grid(row=1, column=0, sticky='nesw')
        self.changeFeedBtn = tki.Button(self.root, text="Change Feed",
                                        command=self.create_select_feed_window)
        self.changeFeedBtn.grid(row=1, column=1, sticky='nesw')
        self.muteNotificationsBtn = tki.Button(self.root, text="Notifications Unmuted",
                                               command=self.mute_unmute_notifications)
        self.muteNotificationsBtn.grid(row=1, column=2, sticky='nesw')

        self.panel = None

        self.cam_list = cam_list

        # create button on bottom of screen

        # start a thread that constantly pools the video sensor for
        # the most recently read frame
        self.stopEvent = threading.Event()
        self.thread = threading.Thread(target=self.video_loop, args=())
        self.thread.start()

        # set a callback to handle when the window is closed
        self.root.wm_title("Skyesight")
        self.main_menu = tki.Menu(self.root)
        self.main_menu.add_command(label="Quit", command=self.on_close)
        self.root.config(menu=self.main_menu)

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

            if self.panel is None:
                self.panel = tki.Label(image=image)
                self.panel.grid(row=0, columnspan=3, sticky='nesw')
                self.panel.image = image

            # otherwise, simply update the panel
            else:
                self.panel.configure(image=image)
                self.panel.image = image
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

    def mute_unmute_notifications(self):
        if self.notificationsMuted:
            self.notificationsMuted = False
            self.muteNotificationsBtn.config(text="Notifications Unmuted")
        else:
            self.notificationsMuted = True
            self.muteNotificationsBtn.config(text="Notifications Muted")


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
