import cv2
import numpy as np

class Stitcher:
    def stitch(self, images):
        (imageL, imageM, imageR) = images
        ratio = 0.75
        reprojThresh = 4.0

        canvas_dim = max(imageM.shape[0], imageM.shape[1]) * len(images)

        canvas = np.zeros((canvas_dim, canvas_dim, 3), np.uint8)

        maskL = np.zeros((imageL.shape[0], imageL.shape[1]))
        maskM = np.zeros((imageM.shape[0], imageM.shape[1]))
        maskR = np.zeros((imageR.shape[0], imageR.shape[1]))

        (kpL, ftL) = self.describe(imageL)
        (kpM, ftM) = self.describe(imageM)
        (kpR, ftR) = self.describe(imageR)

        dst_dim = int(canvas_dim / 2)
        shift = int(dst_dim - (imageM.shape[1] / 2)) 

        (pts1, pts2) = self.match(kpL, kpM, ftL, ftM, ratio) 
        (H1, status) = self.get_homography(pts1, pts2, shift, 0, reprojThresh)

        (pts1, pts2) = self.match(kpR, kpM, ftR, ftM, ratio)
        (H2, status) = self.get_homography(pts1, pts2, 0, 0, reprojThresh)

        resultA = cv2.warpPerspective(imageL, H1, (dst_dim, dst_dim))
        resultB = cv2.warpPerspective(imageR, H2, (dst_dim, dst_dim))

        canvas[0:resultA.shape[0], 0:resultA.shape[1]] = resultA
        resultB_start = shift
        resultB_end = resultB_start + resultB.shape[1]
        canvas[0:resultB.shape[0], resultB_start:resultB_end] = resultB
        canvas[0:imageM.shape[0], shift:imageM.shape[1] + shift] = imageM

        return canvas

    def get_homography(self, pts1, pts2, shift_x, shift_y, reprojThresh):
        for pt in pts2:
            pt[0] += shift_x
            pt[1] += shift_y
        return cv2.findHomography(pts1, pts2, cv2.RANSAC, reprojThresh)
        

    def describe(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        descriptor = cv2.xfeatures2d.SIFT_create()
        (keypoints, features) = descriptor.detectAndCompute(image, None)
        keypoints = np.float32([kp.pt for kp in keypoints])
        return (keypoints, features)

    def match(self, kp1, kp2, ft1, ft2, ratio):
        matcher = cv2.DescriptorMatcher_create("BruteForce")
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

