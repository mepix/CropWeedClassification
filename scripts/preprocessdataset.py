#!/usr/bin/env python3

import os
import datetime
import numpy as np

class DataProcessor(object):
    """This class preprocesses the sugarbeet data by matching the raw image datat with the annotations"""

    def __init__(self,pathToAnnotations="",pathToOriginalImg="",pathToOutputSet=""):
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

    def moveData(self,data_matches,pct_test,debug=True):
        # Get the directory names
        dir_set = os.path.join(self.pathToOutputSet,"Set_"+self.startTime)
        dir_set_test = os.path.join(dir_set,"Test")
        dir_set_train = os.path.join(dir_set,"Train")
        if debug:
            print(dir_set)
            print(dir_set_test)
            print(dir_set_train)

        # Create Directories
        os.makedirs(dir_set)
        os.makedirs(dir_set_test)
        os.makedirs(dir_set_train)

        # Create Array of Random Indexes to split Train/Test Cases
        num_test = pct_test * len(data_matches)
        np.random.randint(0,10,20)

        # Iterate Through the data


        return None

    def run(self):
        print('Processing Data')
        # Get the List of Annotated and Original Images
        img_annotations = self.getFileNames(self.pathToAnnotations,True)
        img_originals = self.getFileNames(self.pathToOriginalImg,True)

        # Remove the Unwanted Info From the Ground Truth String
        img_annotations = self.stripSubstring(img_annotations,verbose=True)

        # Match the Annotated Images with the Originals
        img_matches = self.matchData(img_annotations,np.array(img_originals),verbose=True)

        # Create Training and Test Set
        self.moveData()

        # Copy the files to a timestamped data folder


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
