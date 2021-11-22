#!/usr/bin/env python3

import os
import datetime
import shutil
import numpy as np
import cv2 as cv
import sys
import matplotlib.pyplot as plt
import pandas as pd


class CleanUpMask(object):
    """This script cleans up the noise in the mask annotations"""

    def __init__(self):
        print("Initializing Mask Cleanup Utility")
        self.contour_color = (0,255,255)
        self.contour_min_area = 200
        self.frame_count = 0

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


        # Convert the mask to greyscale
        mask_gray = cv.cvtColor(mask, cv.COLOR_BGR2GRAY)
        if debug:
            print(img.shape)
            print(mask_gray.shape)

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
            img_vis = img.copy()
            for i in range(len(contours)):
                cv.drawContours(img_vis, contours_poly, i, self.contour_color)
                cv.rectangle(img_vis, (int(bound_rect[i][0]), int(bound_rect[i][1])), \
                    (int(bound_rect[i][0]+bound_rect[i][2]), int(bound_rect[i][1]+bound_rect[i][3])), self.contour_color, 2)
            cv.imshow("Contours",img_vis)
            cv.waitKey(0)

        # Break Up the Image Into Multiple Images for each class
        output = [] # Image Name + Label
        for i in range(len(bound_rect)):
            r = bound_rect[i]
            if debug: print(r)

            # Filter out the contours that are too small
            if cv.contourArea(contours[i]) < self.contour_min_area:
                continue

            # Crop the Image and Mask to the desired ROI
            img_crop = img[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
            mask_crop = mask_gray[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]

            # Assign the Label and New Image Name
            label_crop = self.getDominateShade(mask_crop,showHistogram,debug)
            name_crop = "Image-"+f'{self.frame_count:06}'+".png"
            self.frame_count += 1 # Increment Frame Counter

            # Append to the output array
            output.append([name_crop,label_crop])

            # Resize & Save the Image
            img_out = cv.resize(img_crop,(512,512))
            cv.imwrite(self.output_dir+name_crop,img_out)

            if showImage: cv.imshow(name_crop, img_crop)
        if showImage: cv.waitKey(0)

        return np.array(output)

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
            plt.ylabel('number of pixels')
            plt.show()

        # Return the Index of the Maximum Value
        return np.argmax(hist)

    def cleanLabels(self,data,verbose=False,debug=False):
        """
        1 (Sugar Beets) + 9 (Weeds) = 10 Classes

        Currently 17 classes, some are mislabelled, This function manually
        relables the classes

        0: '75' = Sugar Beet
        1: '[57]' = Weed (Type: Blue)
        2: '[186]' = Weed (Type: Neon Green)
        3: '[163,166]' = Weed (Type: Orange)
        4: '[171,185]' = Weed (Type: Cyan)
        5: '[193,194]' = Weed (Type: Gold)
        6: '[203,214]' = Weed (Type: Sea Green)
        7: '[134,149]' = Weed (Type: Grey)
        8: '[105,116]' = Weed (Type: Unknown)
        9: '[28]' = Weed (Type: Unknown)

        Identified:    [ x     x     x     x     x     x     x     x     x     x     x     x     x     x     x    x    x  ]
        Vals:          ['105' '116' '134' '149' '163' '166' '171' '173' '175' '185' '193' '194' '203' '214' '28' '57' '75']
        Counts:        [ 102   9     21    21    650   7     2     26    33    21    235   15    109   25    17   3604 1756]
        Labels:        [ 8     8     7     7     3     3     4     4     4     2     5     5     6     6     9    1    0]
        """

        # Remove the first garbage entry from np.empty[]
        data = data[1:-1,:]
        if debug and verbose: print(data)
        if debug: print(data.shape)
        vals, counts = np.unique(np.sort(data[:,1]),return_counts=True)
        if debug:
            print(vals)
            print(counts)

        # Manually Assign Labels
        labels = np.empty([data.shape[0],1])
        labels[data[:,1]=='105']=8
        labels[data[:,1]=='116']=8
        labels[data[:,1]=='134']=7
        labels[data[:,1]=='149']=7
        labels[data[:,1]=='163']=3
        labels[data[:,1]=='166']=3
        labels[data[:,1]=='171']=4
        labels[data[:,1]=='173']=4
        labels[data[:,1]=='175']=4
        labels[data[:,1]=='185']=2
        labels[data[:,1]=='193']=5
        labels[data[:,1]=='194']=5
        labels[data[:,1]=='203']=6
        labels[data[:,1]=='214']=6
        labels[data[:,1]=='28']=9
        labels[data[:,1]=='57']=1
        labels[data[:,1]=='75']=0

        vals, counts = np.unique(labels,return_counts=True)
        if debug:
            print(labels)
            print(vals)
            print(counts)

        return np.hstack((data,labels))

    def regroupImg(self,key):
        # Make a Directory for Each Class
        labels = np.unique(key[:,2])
        for i in labels:
            os.makedirs(os.path.join(self.output_dir,"Class"+i))

        # Iterate Through the Data and Move to the Appropriate Directory
        for i in range(len(key)):
            a = os.path.join(self.output_dir,key[i,0])
            b = os.path.join(self.output_dir,"Class"+key[i,2],key[i,0])
            shutil.copy(a,b)

        return None

    def run(self,img_dir,mask_dir,output_dir,verbose=True,debug=True):
        """
        This function batch processes the images and masks contained in their
        respective directories. The output data is stored in a new directory
        along with a file titled key.csv that maps the image names to the
        appropriate label.
        """

        # Determine the File Names
        self.img_dir = img_dir
        self.mask_dir = mask_dir
        self.output_dir = output_dir
        if verbose:
            print("Image Directory:",self.img_dir)
            print("Mask Directory:",self.mask_dir)
            print("Output Directory:",self.output_dir)

        img_filenames = next(os.walk(self.img_dir), (None, None, []))[2]
        mask_filenames = next(os.walk(self.mask_dir), (None, None, []))[2]

        if debug and verbose:
            print(img_filenames)
            print(mask_filenames)

        # Iterate Over the images
        image_label_pairs = np.empty([1,2])
        for i in range(len(img_filenames)):

            # Open up the Mask and the Original Image
            img_path = os.path.join(self.img_dir,img_filenames[i])
            mask_path = os.path.join(self.mask_dir,mask_filenames[i])
            if not self.openImages(img_path,mask_path):
                continue # Skip bad reads

            # Split the Masks
            new_data = self.splitMasks(self.img,self.mask,False,False)
            image_label_pairs = np.vstack((image_label_pairs,new_data))

            # Add to Larger Table
            if verbose: print(new_data)

        # Clean, then save Image + Label Pairs
        image_label_pairs = self.cleanLabels(image_label_pairs,verbose,debug)
        if debug: print(image_label_pairs)
        pd.DataFrame(image_label_pairs).to_csv(self.output_dir+"key.csv",header=None,index=None)

        return image_label_pairs

def testSingleImage():
    cleanup = CleanUpMask()
    cleanup.openImages("../data/CleaningTests/Original0123.png","../data/CleaningTests/GroundTruth0123.png")
    new_img_list1 = cleanup.splitMasks(cleanup.img,cleanup.mask,False,True)
    cleanup.openImages("../data/CleaningTests/Original0123.png","../data/CleaningTests/GroundTruth0123.png")
    new_img_list2 = cleanup.splitMasks(cleanup.img,cleanup.mask,False,True)
    new_img_list = np.vstack((new_img_list1,new_img_list2))
    print(new_img_list)
    cv.destroyAllWindows()

def testBatchImage():
    cleanup = CleanUpMask()
    key = cleanup.run(
        "../data/Set_Clean/Original/",
        "../data/Set_Clean/GroundTruth/",
        "../data/Set_Clean/Split/")
    cleanup.regroupImg(key)

def testRegroupImage():
    cleanup = CleanUpMask()
    cleanup.output_dir = "../data/Set_Clean/Split/"
    cleanup.regroupImg("123")


if __name__ == '__main__':
    try:
        # testSingleImage()
        testBatchImage()
        # testRegroupImage()
    except:
        print("ERROR, EXCEPTION THROWN")
        pass
