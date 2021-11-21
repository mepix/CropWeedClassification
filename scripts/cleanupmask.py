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
        self.color_contour = (0,255,255)
        self.contour_min_area = 50

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

        # Find Contours in Image
        contours, hierarchy = cv.findContours(img_gray, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        # Find Contour Bounding Boxes
        contours_poly = [None]*len(contours)
        bound_rect = [None]*len(contours)
        for i, c in enumerate(contours):
            contours_poly[i] = cv.approxPolyDP(c, 3, True)
            bound_rect[i] = cv.boundingRect(contours_poly[i])

        if showImage:
            for i in range(len(contours)):
                cv.drawContours(img, contours_poly, i, self.color_contour)
                cv.rectangle(img, (int(bound_rect[i][0]), int(bound_rect[i][1])), \
                    (int(bound_rect[i][0]+bound_rect[i][2]), int(bound_rect[i][1]+bound_rect[i][3])), self.color_contour, 2)
            cv.imshow("Contours",img)
            cv.waitKey(0)

        # Break Up the Image Into Multiple Images
        for i in range(len(bound_rect)):
            r = bound_rect[i]
            if cv.contourArea(contours[i]) < self.contour_min_area:
                continue
            if debug: print(r)
            img_crop = img[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
            cv.imshow("Image"+str(i), img_crop)
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
