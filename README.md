# 495_Overhead

This application currently creates a panorama of three video feeds taken by two webcameras and a kinect by stitching the three images together. It also enables manual recalibration on keyboard input as well as toggling between each camera feed and the stitched feed.

Requirements:
1) Windows 10 Operating System
2) One Microsoft Kinect
3) Two USB Webcameras
4) Libraries: 
  ```
    comtypes==1.1.4
    imutils==0.4.5
    numpy==1.14.0
    opencv-contrib-python==3.4.0.12
    opencv-python==3.4.0.12
    pykinect2==0.1.0
  ```

Setup:
1) run the command `pip install -r requirements.txt`
2) `python3 FrameGrab.py`

The application accepts the following user keyboard
1) `q` - Quits the Program
2) `a` - recalibrates the camera feeds for image stitching
3) Numberkeys 1-4 - Toggles between the feeds


Infrared Sensors Research
https://www.mouser.com/ProductDetail/SparkFun-Electronics/SEN-13959/?qs=wwacUt%252bV97u8zvpWEUiqvw%3D%3D&gclid=CjwKCAiA8bnUBRA-EiwAc0hZk5Gbmuo5_SjD2euzMF-DB9jgNoD3PM6PEI31G3nICwMRqO8GBTqLDBoCuLQQAvD_BwE

https://www.youtube.com/watch?v=iNXfADw0M9Y

Image Stitching Research 

https://www.pyimagesearch.com/2016/01/11/opencv-panorama-stitching/
https://docs.opencv.org/3.4.0/
https://stackoverflow.com/questions/45965333/removing-parts-of-the-image-with-opencv


(Python getting requirements)[http://www.idiotinside.com/2015/05/10/python-auto-generate-requirements-txt/]
