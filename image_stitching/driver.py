"""
Image stitching driver implementation
"""
import os
import argparse
import imutils
import cv2
import code
import sys
from stitcher import Stitcher

def main():
    stitcher = Stitcher()
    while True:
        leftCam = cv2.VideoCapture(2)
        rearCam = cv2.VideoCapture(1)
        rightCam = cv2.VideoCapture(0)

        #ap = argparse.ArgumentParser()
        #ap.add_argument('-i', '--input-dir', required=True, help='Path to image input directory')
        #args = vars(ap.parse_args())

        #dir = args['input_dir'].strip(' ')
        #input_dir = os.path.join(os.getcwd(), dir)
        #image_files = sorted(os.listdir(input_dir))
        #image_files = [os.path.join(input_dir, x) for x in image_files]
        #images = [imutils.resize(cv2.imread(x), width=400) for x in image_files]
        images = []
        images.append(leftCam.read()[1])
        images.append(rearCam.read()[1])
        images.append(rightCam.read()[1])
        images = [imutils.resize(cv2.flip(x, 1), width=400) for x in images]

        try:
            result = stitcher.stitch(images)
            cv2.imshow("Stitched", result)
        except RuntimeError:
            cv2.waitKey(100)
            continue

        cv2.waitKey(100)




if __name__ == '__main__':
    main()


