import cv2
import numpy as np
#https://medium.com/@kennethjiang/calibrate-fisheye-lens-using-opencv-333b05afa0b0

DIM=(640, 480)
K=np.array([[269.6616655760057, 0.0, 322.2636869266894], [0.0, 270.57327145833693, 211.76621398914702], [0.0, 0.0, 1.0]])
D=np.array([[-0.04175871736401356], [-0.0031884652828571736], [0.0006001904789516924], [-0.0009174281553332885]])
def undistort(img):
    #img = cv2.imread(img_path)
    h,w = img.shape[:2]
    map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, DIM, cv2.CV_16SC2)
    undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
    cv2.imshow("undistorted", undistorted_img)


def undistort_2(img, balance=0.0, dim2=None, dim3=None):
    #0 only uses best, 1 uses all
    #mg = cv2.imread(img_path)
    dim1 = img.shape[:2][::-1]  # dim1 is the dimension of input image to un-distort
    assert dim1[0] / dim1[1] == DIM[0] / DIM[
        1], "Image to undistort needs to have same aspect ratio as the ones used in calibration"
    if not dim2:
        dim2 = dim1
    if not dim3:
        dim3 = dim1
    scaled_K = K * dim1[0] / DIM[0]  # The values of K is to scale with image dimension.
    scaled_K[2][2] = 1.0  # Except that K[2][2] is always 1.0
    # This is how scaled_K, dim2 and balance are used to determine the final K used to un-distort image. OpenCV document failed to make this clear!
    new_K = cv2.fisheye.estimateNewCameraMatrixForUndistortRectify(scaled_K, D, dim2, np.eye(3), balance=balance)
    map1, map2 = cv2.fisheye.initUndistortRectifyMap(scaled_K, D, np.eye(3), new_K, dim3, cv2.CV_16SC2)
    undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
    cv2.imshow("undistorted", undistorted_img)


def main():
    test_cam = cv2.VideoCapture(1)

    while(True):
        keyVal = cv2.waitKey(1)
        if keyVal & 0xFF == ord('q'):
            break

        ret, frame = test_cam.read()
        undistort_2(frame)
        cv2.imshow("distorted", frame)
        #frame_to_display = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
        #cv2.imshow('frame', frame)

    test_cam.release()
    cv2.destroyAllWindows()



main()
