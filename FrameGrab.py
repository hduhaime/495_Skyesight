import numpy as np
import cv2
from pykinect2 import PyKinectV2
from pykinect2.PyKinectV2 import *
from pykinect2 import PyKinectRuntime


# Height and width passed in to resize to correct resolution
# However, this makes the image warped so we currently ignore those values
# and scale and then snip the image instead
def get_kinect_frame(kinect, height, width):
    # Note: alternate way to do this would be ro not resize the image at all, and just
    # snip it. I think this would make this frame more zoomed in than the others or some shit

    if kinect.has_new_color_frame():
        frame = kinect.get_last_color_frame()

        # Reshape the 1D matrix so that it can be used by cv2.imshow
        reshaped = np.reshape(frame, (1080, 1920, 4))

        # Resize image so that it matches the horizontal resolution of webcams
        resized = cv2.resize(reshaped, None, fx=0.444444, fy=0.444444)

        # Return a sliced portion of the image (we want it to be 480x640x4
        return resized[:, 106:746, :]
    return None


def get_webcam_frame(capture):
    ret, frame = capture.read()
    frame_to_display = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
    return cv2.flip(frame_to_display, 1)


def display_feeds(*args):
    arglist = []
    for arg in args:
        arglist.append(arg)

    if (len(args) == 1):
        # Don't concatenate if only one image
        cv2.imshow('frame', *args)
    else:
        # Concatenate images in list and scale them so that they all fit on screen
        image_to_show = cv2.resize(np.concatenate(arglist, axis=1), None, fx=0.6666, fy=0.6666)
        cv2.imshow('frame', image_to_show)


def main():
    # Get camera feeds
    computer_webcam = cv2.VideoCapture(0)
    attached_webcam = cv2.VideoCapture(1)
    kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color)

    while(True):
        # Get webcam frames
        computer_webcam_frame = get_webcam_frame(computer_webcam)
        attached_webcam_frame = get_webcam_frame(attached_webcam)
        height, width, channels = computer_webcam_frame.shape

        kinect_frame = get_kinect_frame(kinect, height, width)

        if computer_webcam_frame is None or kinect_frame is None:
           continue

        display_feeds(computer_webcam_frame, attached_webcam_frame, kinect_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    computer_webcam.release()
    cv2.destroyAllWindows()


main()
