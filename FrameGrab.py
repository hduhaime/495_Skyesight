import sys
import numpy as np
import cv2
import image_stitiching.stitcher.impl.__main__ as stitch_impl
import code

stitch = stitch_impl.Stitcher()
SCREEN_IDX = 1

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
    if frame_to_display.shape[0] != 480:
        frame_to_display = cv2.resize(frame_to_display, None, fx=0.444444, fy=0.444444)[:, 106:746, :]

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

        # REMOVE THIS LINE FOR 3 CAMERAS TO WORK AGAAIN YOU FOOOOOOL
        arglist.append(arglist[-1])
        stitched_image = stitch.stitch(arglist)

        #Show feed L
        if(SCREEN_IDX == 1):
            cv2.imshow('Output', args[0])
        #Show feed M
        elif(SCREEN_IDX == 2):
            cv2.imshow('Output', args[1])
        #Show feed R
        elif(SCREEN_IDX == 3):
            cv2.imshow('Output', args[2])
        #Show stitched feed
        else:
            cv2.imshow('Output', stitched_image)
        #image_to_show = cv2.resize(np.concatenate(arglist, axis=1), None, fx=0.6666, fy=0.6666)
        #cv2.imshow('frame', image_to_show)


def main():

    num_cams = int(sys.argv[1])

    # Get camera feeds
    cam_list = []
    for x in range(0, num_cams):
        cam_list.append(cv2.VideoCapture(x))

    x = 0
    while(True):

        #Capture Input
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
        cam_feeds = [get_webcam_frame(x) for x in cam_list]

        height, width, channels = cam_feeds[0].shape

        if np.any(cam_feeds == None):
           continue
        else:
            x += 1

        display_feeds(*cam_feeds)




    # When everything done, release the capture
    for cam in cam_list:
        cam.release()

    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
