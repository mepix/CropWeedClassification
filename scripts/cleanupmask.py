#!/usr/bin/env python3

import os
import datetime
import shutil
import numpy as np
import cv2 as cv
import sys
import matplotlib.pyplot as plt

class CleanUpMask(object):
    """This script cleans up the noise in the mask annotations"""

    def __init__(self):
        print("Initializing Mask Cleanup Utility")

    def findUniqueColorClasses(self,filePath,showHistogram=False,showImage=False,debug=True):
        # Open Each Image
        img = cv.imread(filePath)
        if debug: print(img.shape)
        if img is None:
            sys.exit("Could not read the image.")

        # Convert the images to greyscale
        img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        if debug: print(img_gray.shape)

        # Show the GreyScale Image
        if showImage:
            cv.imshow('Gray image', img_gray)
            cv.waitKey(0)


        # Find the unique, dominate colors in the image
        hist = cv.calcHist([img_gray], [0], None, [256], [0, 256])
        # hist /= hist.sum() # normalize
        if debug: print(hist)
        if showHistogram:
            plt.plot(hist)
            plt.ylabel('some numbers')
            plt.show()

        # # Apply Blob Detector
        # params = cv.SimpleBlobDetector_Params()
        # # Filter by Area.
        # params.filterByArea = True
        # params.minArea = 1500
        #
        # # Filter by Circularity
        # params.filterByCircularity = False
        # params.minCircularity = 0.1
        #
        # # Filter by Convexity
        # params.filterByConvexity = True
        # params.minConvexity = 0.87
        #
        # # Filter by Inertia
        # params.filterByInertia = True
        # params.minInertiaRatio = 0.01
        #
        # detector = cv.SimpleBlobDetector_create(params)
        # keypoints = detector.detect(img_gray)
        # if showImage:
        #     im_with_keypoints = cv.drawKeypoints(img_gray, keypoints, np.array([]), (0,0,255), cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        #     cv.imshow("Keypoints", im_with_keypoints)
        #     cv.waitKey(0)

        # Find
        # ret, thresh = cv.threshold(img_gray, 150, 255, cv.THRESH_BINARY)
        thresh = img_gray
        contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        if showImage:
            cv.drawContours(img, contours, -1, (0,255,255), 3)
            cv.imshow("Contours",img)
            cv.waitKey(0)



        return None

if __name__ == '__main__':
    # try:
        cleanup = CleanUpMask()
        cleanup.findUniqueColorClasses("../data/CleaningTests/InputTest.png",True,True)
        cv.destroyAllWindows()
    # except:
        print("ERROR, EXCEPTION THROWN")
        pass
