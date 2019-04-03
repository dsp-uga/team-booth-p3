"""
OUTLINE:
    This script is designed to take one target dataset, process the data, and
    generate a prdiction for neurons. This program followed many of the ideas
    outlined in the assignment regarding NMF along with instatiation approaches
    illustrated in previous projects including:
        https://github.com/dsp-uga/bath
        https://gist.github.com/freeman-lab/330183fdb0ea7f4103deddc9fae18113
        


See https://github.com/codeneuro/neurofinder-python for more information on 
neurofinder
  $ pip install neurofinder


"""

"""
Packages
"""
import skimage #import io, filters
import glob
import os
import re
import argparse
import numpy
import json
import cv2
from extraction import NMF

"""
Global Variables
""" 

imageNameList = []
imageList = []
chunkSize = ()
padding = ()
regions = []

"""
Subrutines
"""

def readAllImages(args):
    # Read in all image file names
    global imageNameList 
    imageNameList = [re.sub('^.*\/images\/([^\/]+)$',r'\1',file) for file 
                     in glob.glob(args.sourceDir + "/images/image*.tiff")]

    # Now read in the gray scale image
    global imageList
    idx = 0
    for name in imageNameList:
        imageList.append(skimage.io.imread(args.sourceDir+"/images/"+name, 
                                           as_gray=True))
        idx += 1
        if idx%250 == 0:
            print("idx = "+str(idx))

"""
The clean images function takes advantage of a range of numpy functions that
were shown potentially useful in the project https://github.com/dsp-uga/bath
"""
def cleanImages(args):
    print("Cleaning images")
    global imageList
    
    # Normalize the image values if requested
    if( args.normalize ):
        for idx in range(0,len(imageList)):
            cv2.normalize(imageList[idx], imageList[idx], 0, 255, cv2.NORM_MINMAX)

"""
This is the core application function that calculates NMF for the images and
geneartes a prediction file from the resulting values, learned about this 
approach for using the functions in https://github.com/dsp-uga/bath
"""
def applyNMF(args):
    print("Applying NMF")
    global imageList
    global chunkSize
    global padding
    global regions
    
    model = NMF(k=args.nmf_k, max_iter=args.nmf_maxIter, 
                percentile=args.nmf_percentile, overlap=args.nmf_overlap, 
                min_size=args.nmf_minSize)
    model = model.fit(imageList, chunk_size=chunkSize, 
                      padding=padding)
    merged = model.merge(overlap=args.nmf_overlap, max_iter=args.fit_mergeIter, 
                         k_nearest=args.merge_kNearest)
    regions = [{'coordinates': region.coordinates.tolist()} 
        for region in merged.regions]

"""
Write the output to a target file
"""
def writeResults(args):
    print("Writing results")
    global regions
    
    dataSetName = re.sub('^.*neurofinder\.([^\/]+)$',r'\1',args.sourceDir)
    
    output = {"dataset": dataSetName, "regions": regions };
    with open(args.outputFile, 'w') as outfile:
        json.dump(output, outfile)

"""
MAIN    
"""
def main(args):
    # 
    # Start by checking to ensure all command line arguments are valid
    #
    if not os.path.exists(args.sourceDir):
        raise Exception("ERROR: The dir '" + args.sourceDir \
                        + "' does not exist")
    arr = re.split(",",args.fit_chunkSize)
    if len(arr)!=2 or not arr[0].isdigit() or not arr[1].isdigit():
        raise Exception("ERROR: The chunk size expects two integers comma "\
                        "delimited (no space!)")
    global chunkSize
    chunkSize = (int(arr[0]),int(arr[1]))
    arr = re.split(",",args.fit_padding)
    if len(arr)!=2 or not arr[0].isdigit() or not arr[1].isdigit():
        raise Exception("ERROR: The padding expects two integers comma "\
                        "delimited (no space!)")
    global padding
    padding = (int(arr[0]),int(arr[1]))
    
    if args.sourceDir.endswith("/"):
        args.sourceDir = args.sourceDir[:-1]
    
    # Start by reading in all images
    readAllImages(args)
    
    # Clean images if requested
    cleanImages(args)
    
    applyNMF(args)
    
    writeResults(args)
    
"""
Read Command Lines
"""   
if __name__ == '__main__':
    #
    # Simply check all command line arguments, then call main with them
    #
    parser = argparse.ArgumentParser(description='This is part of the UGA ' + \
                                'CSCI 8360 Project 3. Please vist ' + \
                                'our GitHub project at ' + \
                                'https://github.com/dsp-uga/team-booth-p3 ' + \
                                'for more information regarding data' + \
                                ' organizations, expectations, and ' + \
                                'examples on how to execute out scripts.')

    parser.add_argument('-d','--sourceDir', required=True, \
                        help='The base directory storing neuron tiff ' + \
                        'images in an images sub-directory. Images are ' + \
                        'expected to have names that ' + \
                        'take the form imageXXXXX.tiff, where Xs are ' + \
                        'integers. The directory''s name is expected to '+ \
                        'be the sample name (ex neurofinder.00.00)')
    parser.add_argument('-o','--outputFile', required=False, 
                        default='regions.json', help='Defines the output ' + \
                        'file to which this program will write predictions.')
    parser.add_argument('-norm','--normalize',required=False, default=False, 
                        action='store_true', help='Apply normalizetion ' + \
                        'to the image (default False)')
    parser.add_argument('-nmf_k','--nmf_k', required=False, type=int, \
                        default=5, help='The k argument to the ' + \
                        'thunder-extraction NMF function (default 5)')
    parser.add_argument('-nmf_maxIter','--nmf_maxIter', required=False, \
                        type=int, default=20, help='Maximum number of ')
    parser.add_argument('-nmf_percentile','--nmf_percentile', required=False, \
                        type=int, default=99, help='fill later...')
    parser.add_argument('-nmf_overlap','--nmf_overlap', required=False, \
                        type=float, default=0.1, help='fill later...')
    parser.add_argument('-nmf_minSize','--nmf_minSize', required=False, \
                        type=int, default=20, help='fill later...')
    parser.add_argument('-fit_chunkSize','--fit_chunkSize', required=False, \
                        default="32,32", help='fill later...')
    parser.add_argument('-fit_padding','--fit_padding', required=False, \
                        default="20,20", help='fill later...')
    parser.add_argument('-fit_mergeIter','--fit_mergeIter', required=False, \
                        type=int, default=5, help='fill later...')
    parser.add_argument('-merge_kNearest','--merge_kNearest', required=False, \
                        type=int, default=20, help='fill later...')
    
    args = parser.parse_args()
    main(args)







