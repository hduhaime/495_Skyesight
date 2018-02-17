"""
Image stitching driver implementation
"""
import os
import argparse
import imutils
import cv2
import code
import sys

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('-i', '--input-dir', required=True, help='Path to image input directory')
    args = vars(ap.parse_args())

    dir = args['input_dir'].strip(' ')
    input_dir = os.path.join(os.getcwd(), dir)
    image_files = sorted(os.listdir(input_dir))
    image_files = [os.path.join(input_dir, x) for x in image_files]
    print(image_files)


if __name__ == '__main__':
    main()


