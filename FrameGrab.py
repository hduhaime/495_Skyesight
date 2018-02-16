import numpy as np
import cv2
from pykinect2 import PyKinectV2
from pykinect2.PyKinectV2 import *
from pykinect2 import PyKinectRuntime

webcam = cv2.VideoCapture(0)

kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color)

while(True):
    # Capture frame-by-frame
    ret, webcamframe = webcam.read()

    height, width, channels = webcamframe.shape

    # Our operations on the frame come here
    frame_to_display = cv2.cvtColor(webcamframe, cv2.COLOR_BGR2BGRA)

    frame_to_display = cv2.flip(frame_to_display, 1)

    if kinect.has_new_color_frame():

        kinectframe = kinect.get_last_color_frame()
        reshaped = np.reshape(kinectframe, (1080, 1920, 4))
        kinect_resized = cv2.resize(reshaped, (width, height))
        shape = kinect_resized.shape

        # Display the resulting frame
        cv2.imshow('frame', np.concatenate((frame_to_display, kinect_resized), axis=1))

        kinectframe = None


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
webcam.release()
cv2.destroyAllWindows()