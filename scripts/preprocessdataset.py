#!/usr/bin/env python3

import os
import numpy as np

class DataProcessor(object):
    """This class preprocesses the sugarbeet data by matching the raw image datat with the annotations"""

    def __init__(self,pathToAnnotations="",pathToOriginalImg="",pathToOutputSet=""):
        print("Initializing DataProcessor")
        self.pathToAnnotations=pathToAnnotations
        self.pathToOriginalImg=pathToOriginalImg
        self.pathToOutputSet=pathToOutputSet
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

    def moveData(self):
        return None

    def run(self):
        print('Processing Data')
        # Get the List of Annotated and Original Images
        img_annotations = self.getFileNames(self.pathToAnnotations,True)
        img_originals = self.getFileNames(self.pathToOriginalImg,True)

        # Remove the Unwanted Info From the Ground Truth
        img_annotations = self.stripSubstring(img_annotations,verbose=True)

        # Match the Annotated Images with the Originals
        self.matchData(img_annotations,np.array(img_originals),verbose=True)

        # Create Training and Test Set

        # Copy the files to a timestamped data folder


        return None

if __name__ == '__main__':
    try:
        preproc = DataProcessor("../data/ijrr_annotations_160523",
            "../data/ijrr_sugarbeets_2016_annotations/CKA_160523/images/rgb")
        preproc.run()
    except:
        print("ERROR, EXCEPTION THROWN")
        pass
