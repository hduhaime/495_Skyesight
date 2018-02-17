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

        M1 = self.match(kpL, kpM, ftL, ftM, ratio, reprojThresh) 
        M2 = self.match(kpR, kpM, ftR, ftM, ratio, reprojThresh) 

        (matches, H1, status) = M1
        (matches, H2, status) = M2

        dst_dim = int(canvas_dim / 2)

        resultA = cv2.warpPerspective(imageL, H1, (dst_dim, dst_dim))
        resultB = cv2.warpPerspective(imageR, H2, (dst_dim, dst_dim))

        canvas[0:resultA.shape[0], 0:resultA.shape[1]] = resultA
        canvas[0:resultB.shape[0], dst_dim:] = resultB

        return canvas

    def describe(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        descriptor = cv2.xfeatures2d.SIFT_create()
        (keypoints, features) = descriptor.detectAndCompute(image, None)
        keypoints = np.float32([kp.pt for kp in keypoints])
        return (keypoints, features)

    def match(self, kp1, kp2, ft1, ft2, ratio, reprojThresh):
        matcher = cv2.DescriptorMatcher_create("BruteForce")
        rawMatches = matcher.knnMatch(ft1, ft2, 2)
        matches = []
        for m in rawMatches:
            if len(m) == 2 and m[0].distance < m[1].distance * ratio:
                matches.append((m[0].trainIdx, m[0].queryIdx))

        if len(matches) > 4:
            pts1 = np.float32([kp1[i] for (_, i) in matches])
            pts2 = np.float32([kp2[i] for (i, _) in matches])
            (H, status) = cv2.findHomography(pts1, pts2, cv2.RANSAC, reprojThresh)
            return (matches, H, status)

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

