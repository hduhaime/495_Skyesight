# import the necessary packages
from __future__ import print_function
import argparse
from imutils.video import VideoStream
import time
from PIL import Image
from PIL import ImageTk
import Tkinter as tki
import threading
import datetime
import imutils
import cv2
import os

class Graphics:

	def __init__(self, vs):
		# store the video stream object and output path, then initialize
		# the most recently read frame, thread for reading frames, and
		# the thread stop event
		self.vs = vs
		self.frame = None
		self.thread = None
		self.stopEvent = None
 
		# initialize the root window and image panel
		self.root = tki.Tk()
		self.panel = None

		# # create a button, that when pressed, will take the current
		# # frame and save it to file
		# btn = tki.Button(self.root, text="Snapshot!",
		# 	command=self.takeSnapshot)
		# btn.pack(side="bottom", fill="both", expand="yes", padx=10,
		# 	pady=10)
 
		# start a thread that constantly pools the video sensor for
		# the most recently read frame
		self.stopEvent = threading.Event()
		self.thread = threading.Thread(target=self.videoLoop, args=())
		self.thread.start()
 
		# set a callback to handle when the window is closed
		self.root.wm_title("PyImageSearch PhotoBooth")
		self.root.wm_protocol("WM_DELETE_WINDOW", self.onClose)


