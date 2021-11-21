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
        self.contour_color = (0,255,255)
        self.contour_min_area = 50

    def openImages(self,pathToImg,pathToMask):
        """Accepts the string path to the original image and associated mask"""
        # Open the Images
        self.img = cv.imread(pathToImg)
        self.mask = cv.imread(pathToMask)

        # Report Success
        if self.img is None or self.mask is None:
            return False
        else: return True

    def splitMasks(self,img,mask,showHistogram=False,showImage=False,debug=True):
        if debug: print(img.shape)

        # Convert the images to greyscale
        mask_gray = cv.cvtColor(mask, cv.COLOR_BGR2GRAY)
        if debug: print(mask_gray.shape)

        # Show the GreyScale Image
        if showImage:
            cv.imshow('Gray image', mask_gray)
            cv.waitKey(0)

        # Find Contours in Image
        contours, hierarchy = cv.findContours(mask_gray, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        # Find Contour Bounding Boxes
        contours_poly = [None]*len(contours)
        bound_rect = [None]*len(contours)
        for i, c in enumerate(contours):
            contours_poly[i] = cv.approxPolyDP(c, 3, True)
            bound_rect[i] = cv.boundingRect(contours_poly[i])
        if showImage:
            for i in range(len(contours)):
                cv.drawContours(img, contours_poly, i, self.contour_color)
                cv.rectangle(img, (int(bound_rect[i][0]), int(bound_rect[i][1])), \
                    (int(bound_rect[i][0]+bound_rect[i][2]), int(bound_rect[i][1]+bound_rect[i][3])), self.contour_color, 2)
            cv.imshow("Contours",img)
            cv.waitKey(0)

        # Break Up the Image Into Multiple Images
        for i in range(len(bound_rect)):
            r = bound_rect[i]
            if debug: print(r)

            # Filter out the contours that are too small
            if cv.contourArea(contours[i]) < self.contour_min_area:
                continue
            # Crop the Image to the desired ROI
            img_crop = img[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
            label = self.getDominateShade(img_crop,showHistogram,debug)
            if showImage: cv.imshow("Image-"+str(i)+"-"+str(label), img_crop)
        if showImage: cv.waitKey(0)

        return None

    def getDominateShade(self,mask_gray,showHistogram=False,debug=True):
        """Returns the dominate shade in a grayscale image"""
        # Find the unique, dominate colors in the image
        hist = cv.calcHist([mask_gray], [0], None, [256], [0, 256])

        # Drop the first value since it's only the background
        hist = np.array(hist[1:-1,:])
        if debug: print("Histogram Shape:",hist.shape)

        # hist /= hist.sum() # normalize
        if debug: print(hist)
        if showHistogram:
            plt.plot(hist)
            plt.ylabel('some numbers')
            plt.show()

        # Return the Index of the Maximum Value
        return np.argmax(hist)

if __name__ == '__main__':
    # try:
        cleanup = CleanUpMask()
        cleanup.splitMasks("../data/CleaningTests/InputTest.png",True,True)
        cv.destroyAllWindows()
    # except:
        print("ERROR, EXCEPTION THROWN")
        pass
