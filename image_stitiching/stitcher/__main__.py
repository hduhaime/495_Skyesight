"""
Image stitching driver implementation
"""
import os
import argparse
import imutils
import cv2
from stitcher.impl.__main__ import Stitcher

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('-i', '--input-dir', required=True, help='Path to image input directory')
    args = vars(ap.parse_args())

    input_dir = args['input_dir']

    image_files = sorted(os.listdir(input_dir))
    image_files = [os.path.join(input_dir, x) for x in image_files]
    images = [imutils.resize(cv2.imread(x), width=400) for x in image_files]

    stitcher = Stitcher()
    result = stitcher.stitch(images)

    cv2.imshow("Result", result)
    cv2.waitKey(0)


if __name__ == '__main__':
    main()


