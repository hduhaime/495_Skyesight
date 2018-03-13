import cv2

def main():
    test_cam = cv2.VideoCapture(0)

    while(True):
        keyVal = cv2.waitKey(1)
        if keyVal & 0xFF == ord('q'):
            break

        ret, frame = test_cam.read()
        frame_to_display = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
        cv2.imshow('frame', frame)

    test_cam.release()
    cv2.destroyAllWindows()



main()
