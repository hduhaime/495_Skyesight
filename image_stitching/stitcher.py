import cv2
import numpy as np

class Stitcher:
    def __init__(self):
        self.imageL = None
        self.imageM = None
        self.imageR = None
        self.shift = None
        self.hmatL = None
        self.hmatM = None
        self.hmatR = None
        self.ratio = 0.75
        self.reprojThresh = 4.0

    def prepare_for_calibration(self, img):


        #Canny
        #output.append(cv2.Canny(images, 100, 200)
        #Normalization
        gray = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
        eq = cv2.equalizeHist(gray)

        output = eq

        return output

    def calibrate(self):
        (kpL, ftL) = self.describe(self.imageL)
        (kpM, ftM) = self.describe(self.imageM)
        (kpR, ftR) = self.describe(self.imageR)

        if np.any([kpL, kpM, kpR, ftL, ftM, ftR] is None):
            print("ERROR: Unable to find key points or features between images.")
            return

        ptsA = self.match(kpL, kpM, ftL, ftM, self.ratio)
        ptsB = self.match(kpR, kpM, ftR, ftM, self.ratio)

        if np.any(ptsA is None) or np.any(ptsB is None):
            print("ERROR: Unable to match points between images")
            return

        (H1, status) = self.get_homography(ptsA[0], ptsA[1], self.shift[0], 0, self.reprojThresh)
        (H2, status) = self.get_homography(ptsB[0], ptsB[1], 0, 0, self.reprojThresh)

        if H2 is None or H1 is None:
            print("ERROR: Unable to find homography matrix for one or more images.")
            return

        self.hmatM = np.eye(3)
        self.hmatM[0][-1] = self.shift[0]
        self.hmatM[1][-1] = self.shift[1]

        # 1 0 tX
        # 0 1 tY
        # 0 0 1

        self.hmatL = np.matmul(self.hmatM, H1)
        self.hmatR = np.matmul(self.hmatM, H2)


    def stitch(self, images):
        (self.imageL, self.imageM, self.imageR) = images

        max_dim = max(self.imageM.shape[0], self.imageM.shape[1])
        canvas_dim = max_dim * len(images)

        #canvasA = np.zeros((canvas_dim, canvas_dim, 4), np.uint8)
        #canvasB = np.zeros((canvas_dim, canvas_dim, 4), np.uint8)

        self.shift = [max_dim, max_dim]
        if self.hmatL is None or self.hmatR is None:
            self.calibrate()



        #tmp = cv2.warpPerspective(imageL, hMat_LINV, (canvas_dim, canvas_dim))
        #tmp[0:imageM.shape[0], 0:imageM.shape[1], :] = 0.5
        #tmp[offsety:imageM.shape[0] + offsety, offsetx:imageM.shape[1] + offsetx] = imageM
        #canvas = tmp


        resultL = cv2.warpPerspective(self.imageL, self.hmatL, (canvas_dim, canvas_dim))
        resultM = cv2.warpPerspective(self.imageM, self.hmatM, (canvas_dim, canvas_dim))
        resultR = cv2.warpPerspective(self.imageR, self.hmatR, (canvas_dim, canvas_dim))

        canvas = resultR
        canvas[resultL > 0] = resultL[resultL > 0]
        canvas[resultM > 0] = resultM[resultM > 0]

        # Crop out as much negative space as possible
        trim = canvas > 0
        mat = np.array([[y[0] for y in x] for x in trim])
        
        cropped = canvas[np.ix_(mat.any(1), mat.any(0))]


        # canvasA[0:resultA.shape[0], 0:resultA.shape[1]] = resultA
        # resultB_start = shift
        # resultB_end = resultB_start + resultB.shape[1]
        # canvasB[0:resultB.shape[0], resultB_start:resultB_end] = resultB
        # canvasB[0:imageM.shape[0], shift:imageM.shape[1] + shift] = imageM
        #
        # canvasB[canvasA > 0] = 0

        #TODO
        #canvas = resultL
        #canvas[resultR > 0] = resultR[resultR > 0]
        #canvas[resultM > 0] = resultM[resultM > 0]
        #canvasA + canvasB

        return cv2.resize(cropped, None, fx=0.444444, fy=0.444444)

    def get_homography(self, pts1, pts2, shift_x, shift_y, reprojThresh):
        #for pt in pts2:
        #    pt[0] += shift_x
        #    pt[1] += shift_y
        return cv2.findHomography(pts1, pts2, cv2.RANSAC, reprojThresh)
        

    def describe(self, image):
        image = self.prepare_for_calibration(image)
        descriptor = cv2.xfeatures2d.SIFT_create()
        (keypoints, features) = descriptor.detectAndCompute(image, None)
        keypoints = np.float32([kp.pt for kp in keypoints])
        return (keypoints, features)

    def match(self, kp1, kp2, ft1, ft2, ratio):

        # FLANN_INDEX_KDTREE = 1
        # index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        # search_params = dict(checks=50)
        # flann = cv2.FlannBasedMatcher(index_params, search_params)

        matcher = cv2.DescriptorMatcher_create("BruteForce") #flann
        rawMatches = matcher.knnMatch(ft1, ft2, 2)
        matches = []
        for m in rawMatches:
            if len(m) == 2 and m[0].distance < m[1].distance * ratio:
                matches.append((m[0].trainIdx, m[0].queryIdx))

        if len(matches) > 4:
            pts1 = np.float32([kp1[i] for (_, i) in matches])
            pts2 = np.float32([kp2[i] for (i, _) in matches])
            return (pts1, pts2)

        return None

    def drawMatches(self, imageA, imageB, kpsA, kpsB, matches, status):
        # initialize the output visualization image
        (hA, wA) = imageA.shape[:2]
        (hB, wB) = imageB.shape[:2]
        vis = np.zeros((max(hA, hB), wA + wB, 3), dtype="uint8")
        vis[0:hA, 0:wA] = imageA
        vis[0:hB, wA:] = imageB
    
        # loop over the matches
        for ((trainIdx, queryIdx), s) in zip(matches, status):
                # only process the match if the keypoint was successfully
                # matched
                if s == 1:
                        # draw the match
                        ptA = (int(kpsA[queryIdx][0]), int(kpsA[queryIdx][1]))
                        ptB = (int(kpsB[trainIdx][0]) + wA, int(kpsB[trainIdx][1]))
                        cv2.line(vis, ptA, ptB, (0, 255, 0), 1)
    
        # return the visualization
        return vis 
