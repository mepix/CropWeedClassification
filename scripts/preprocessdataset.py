#!/usr/bin/env python3

import os
import datetime
import shutil
import numpy as np

class DataProcessor(object):
    """This class preprocesses the sugarbeet data by matching the raw image datat with the annotations"""

    def __init__(self,pathToAnnotations="",pathToOriginalImg="",pathToOutputSet=""):
        """The initializing expects paths to annotated and original data as well as an output directory"""
        print("Initializing DataProcessor")
        self.pathToAnnotations=pathToAnnotations
        self.pathToOriginalImg=pathToOriginalImg
        self.pathToOutputSet=pathToOutputSet
        self.startTime = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        print("File Paths to be Used:")
        print("-->Annotations:",self.pathToAnnotations)
        print("-->Original Images:",self.pathToOriginalImg)
        print("-->Output:",self.pathToOutputSet)

    def getFileNames(self,path,verbose=False):
        """This function returns a list of all files in the target path"""
        filenames = next(os.walk(path), (None, None, []))[2]
        if verbose: print(filenames)
        return filenames

    def stripSubstring(self,string_list,sub="_GroundTruth_color",verbose=False):
        """Remove substring from all strings in the list"""
        out_list = []
        for s in string_list:
            stripped = s.replace(sub,"")
            out_list.append([stripped,s])

        out_list = np.array(out_list)
        if verbose: print(out_list)
        return out_list #first col: stripped, second col: original

    def matchData(self,a_arr,b_arr,verbose=False,debug=False):
        """Matches items in list a with items in list b"""
        if verbose:
            print("Length of a:",len(a_arr))
            print("Length of b:",len(b_arr))

        # Create variables for matches
        match_count = 0
        matches = []

        # Check if each item in a is present somewhere in b
        for i in range(len(a_arr)):
        # for a in a_arr[:,0]:
            # Search for the index of the match
            result = np.where(b_arr==a_arr[i,0])
            if debug: print(a_arr[i,0],result[0])
            # Check if we have a match
            if len(result) > 0 and len(result[0]) > 0:
                matches.append(a_arr[i,:])
                match_count += 1

        if verbose: print("Matches Found:",match_count)
        return np.array(matches)

    def copyData(self,data_matches,pct_test=None,debug=True):
        """This function copies the matched original/annotated images into the output direcoty"""
        # Get the directory names
        dir_set = os.path.join(self.pathToOutputSet,"Set_"+self.startTime)
        dir_original = os.path.join(dir_set,"Original")
        dir_ground_truth = os.path.join(dir_set,"GroundTruth")
        if debug:
            print(dir_set)
            print(dir_original)
            print(dir_ground_truth)

        # Create Directories
        os.makedirs(dir_set)
        os.makedirs(dir_original)
        os.makedirs(dir_ground_truth)

        # Only make directories to split test/train if required
        if pct_test is not None:
            dir_set_test = os.path.join(dir_set,"Test")
            dir_set_train = os.path.join(dir_set,"Train")
            if debug: print(dir_set_test)
            if debug: print(dir_set_train)
            os.makedirs(dir_set_test)
            os.makedirs(dir_set_train)

            # Create Array of Random Indexes to split Train/Test Cases
            num_test = pct_test * len(data_matches)
            np.random.randint(0,10,20) # TODO:NYI:SPLIT TEST/TRAIN

        # Iterate Through the data
        for i in range(len(data_matches)):
            print("Preparing to Copy:",data_matches[i,:])
            # Move the Original Image
            shutil.copy(os.path.join(self.pathToOriginalImg,data_matches[i,0]),dir_original)

            # Move the Ground Truth
            shutil.copy(os.path.join(self.pathToAnnotations,data_matches[i,1]),dir_ground_truth)

        return None

    def run(self):
        print('Processing Data')
        # Get the List of Annotated and Original Images
        img_annotations = self.getFileNames(self.pathToAnnotations,False)
        img_originals = self.getFileNames(self.pathToOriginalImg,False)

        # Remove the Unwanted Info From the Ground Truth String
        img_annotations = self.stripSubstring(img_annotations,verbose=False)

        # Match the Annotated Images with the Originals
        img_matches = self.matchData(img_annotations,np.array(img_originals),verbose=False)

        # Copy the files to a timestamped data folder
        self.copyData(img_matches)

        return None

if __name__ == '__main__':
    try:
        preproc = DataProcessor("../data/ijrr_annotations_160523",
            "../data/ijrr_sugarbeets_2016_annotations/CKA_160523/images/rgb",
            "../data/")
        preproc.run()
    except:
        print("ERROR, EXCEPTION THROWN")
        pass
