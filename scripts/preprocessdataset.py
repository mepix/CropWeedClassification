#!/usr/bin/env python3

import os

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
            out_list.append(stripped)
        if verbose: print(out_list)
        return out_list

    def matchData(self,a,b):
        return None

    def moveData(self):
        return None

    def run(self):
        print('Processing Data')
        # Get the List of Annotated and Original Images
        img_annotations = self.getFileNames(self.pathToAnnotations,True)
        img_originals = self.getFileNames(self.pathToOriginalImg,True)

        # Remove the Unwanted Info From the Ground Truth
        img_annotations_no_sub = self.stripSubstring(img_annotations,verbose=True)

        # Match the Annotated Images with the Originals

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
