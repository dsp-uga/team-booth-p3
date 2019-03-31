#!/usr/bin/python

import numpy as np
import cv2
import glob
import os
from matplotlib import pyplot as plt
import argparse
import re

#===========#
## SUMMARY ##
#-----------#
#
# This script takes a target directory with images and performs
# the following steps:
#   1) Convert all images to simply black or white (0 or 1)
#   2) Itereate through each sequence of frames (say 4 frames in a row)
#      and XORs the content
#   3) Applies CV2 blurFilter to the resulting images
#   4) Iterates through all images generated to find the largest occurrance
#      of each image generated
#   5) Takes each ring found and looks through all images again to find its
#      largest occurrence
#   6) Take the largest occurrence of each ring found and generate output
#      file for later evaluation
#
# NOTICE: These steps are intrensically hypothetical in meaning/effectiveness,
# so this work will likely come under some concerns, but it's a start...
#

#
# This function takes all files and converts their pixels to simply 0s and 1s
#
def convertToBlackAndWhite(args, imageList):
    # Loop through all files
    for imageName in imageList:
        imageName = imageName.replace(".tiff",".png")
        if not os.path.exists(args.workDir+"/"+imageName):
            img = cv2.imread(args.sourceDir+"/"+imageName)
            channels = cv2.split(img)
            h = channels[1].shape[0]
            w = channels[1].shape[1]
            for y in range(0,h):
                for x in range(0,w):
                    if( channels[1][y,x] > 0 ):
                        channels[1][y,x] = 1
                    else:
                        channels[1][y,x] = 0
            plt.imsave(args.workDir+"/"+imageName,channels[1],cmap='gray')

def buildIntersectChannels(args, imageListPng, startIdx ):
    images = []
    for idx in range(0,args.sampleSize):
        targIdx = startIdx+idx
        name = cv2.imread(args.workDir+"/"+imageListPng[targIdx],0)
        images.append(name)
    h = images[0].shape[0]
    w = images[0].shape[1]
    finalImage = cv2.imread(args.workDir+"/"+imageListPng[startIdx+idx],0)
    for y in range(0,h):
        for x in range(0,w):
            for idx in range(0,args.sampleSize):
                if( idx == 0 ):
                    if( images[idx][y,x] == 255 and images[idx][y,x]==images[idx+1][y,x] ):
                        finalImage[y,x] = 255
                    else:
                        finalImage[y,x] = 0
                else:
                    if( finalImage[y,x] == 255 and images[idx][y,x] == finalImage[y,x] ):
                        finalImage[y,x] = 255
                    else:
                        finalImage[y,x] = 0
            if( finalImage[y,x] == 255 ):
                finalImage[y,x] = 1;
    finalImage = cv2.bilateralFilter(finalImage, 9, 75, 75)
    plt.imsave(args.workDir+"/finalImage"+str(startIdx)+"."+str(args.sampleSize)+".png",finalImage,cmap="gray",vmin=0,vmax=1.5)

def main(args):
    # 
    # Start by checking to ensure all command line arguments are valid
    #
    if not os.path.exists(args.sourceDir):
        raise Exception("ERROR: The dir '" + args.sourceDir + "' does not exist")
    if not os.path.exists(args.workDir):
        raise Exception("ERROR: The dir '" + args.workDir + "' does not exist")
    if args.sampleSize < 1 or args.sampleSize > 10:
        raise Exception("ERROR: The sample size must be in the inclusive range 1 <= size <= 10")
    
    if args.sourceDir.endswith("/"):
        args.sourceDir = args.sourceDir[:-1]
    if args.workDir.endswith("/"):
        args.workDir = args.workDir[:-1]

    print(args.sourceDir + ", " + args.workDir)

    # Make a list of all files
    imageList = [re.sub('^.*\/([^\/]+)$',r'\1',f) for f in glob.glob(args.sourceDir + "/image*.tiff")]

    print("M1 - " + imageList[0])

    # Change the images to black and white
    convertToBlackAndWhite(args,imageList)
    print("M2")
    imageListPng = []
    for imageName in imageList:
        print("M3 - " + imageName)
        imageName = imageName.replace(".tiff",".png")
        imageListPng.append(imageName)

    # Process the image files to generate new image files
    for idx in range(0,len(imageListPng)-args.sampleSize):
        if not os.path.exists(args.workDir+"/finalImage"+str(idx)+"."+str(args.sampleSize)+".png"):
            buildIntersectChannels(args,imageListPng,idx)
            print(imageListPng[idx])


if __name__ == '__main__':
    #
    # Simply check all command line arguments, then call main with them
    #
    parser = argparse.ArgumentParser(description='This is part of the UGA CSCI 8360 Project 3. Please vist our GitHub project at https://github.com/dsp-uga/team-booth-p3 for more information regarding data organizations, expectations, and examples on how to execute out scripts.')

    parser.add_argument('-d','--sourceDir', required=True, help='The base directory storing neuron tiff images. Images are expected to have names that take the form imageXXXXX.tiff, where Xs are integers.')
    parser.add_argument('-w','--workDir', required=True, help='A path to a working directory where files might be placed temporarily.')
    parser.add_argument('-s','--sampleSize', required=False, type=int, default=5, help='Defines the number of consecutive images used to make initial guesses. (def. 4)')
    parser.add_argument('-o','--outputFile', required=False, default='regions.json', help='Defines the output file to which this program will write predictions.')

    args = parser.parse_args()
    main(args)




