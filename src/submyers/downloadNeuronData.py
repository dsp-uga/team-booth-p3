"""
OUTLINE:
    This script simply downloads and unzips a fixed list of files from the GSP
    space for UGA course CSCI8360 (DSP). These files have fixed names and are
    defined in the global variable.
"""

import argparse
import os
import urllib
import zipfile


base_path = 'https://s3.amazonaws.com/neuro.datasets/challenges/neurofinder/'
file_names = ['neurofinder.00.00','neurofinder.00.01',
             'neurofinder.00.02','neurofinder.00.03',
             'neurofinder.00.04','neurofinder.00.05',
             'neurofinder.00.08','neurofinder.00.06',
             'neurofinder.00.10','neurofinder.00.11',
             'neurofinder.01.00','neurofinder.01.01',
             'neurofinder.02.00','neurofinder.02.01',
             'neurofinder.03.00','neurofinder.04.00',
             'neurofinder.04.01','neurofinder.00.00.test',
             'neurofinder.00.01.test','neurofinder.01.00.test', 
             'neurofinder.01.01.test','neurofinder.02.00.test',
             'neurofinder.02.01.test','neurofinder.03.00.test', 
             'neurofinder.04.00.test','neurofinder.04.01.test']          

def main(args):
    # Check to make sure the target directory exists
    if not os.path.exists(args.outputDir):
        raise Exception("ERROR: The dir '"+args.sourceDir+"' does not exist")

    #
    # Now iterate through the fileNames list, download, and unzip each file
    # listed
    # 
    global base_path
    global file_names
    
    #
    # Read in and unzip all files listed
    #
    for file in file_names:
        print("Downloading "+file)
        urllib.urlretrieve(base_path+file+".zip", 
                           args.outputDir+"/"+file+".zip")
        with zipfile.ZipFile(args.outputDir+"/"+file+".zip", "r") as archive:
            archive.extractall(args.outputDir+"/"+file)
        os.remove(args.outputDir+"/"+file+".zip")
        print("Done with "+file)

if __name__ == '__main__':
    #
    # Simply check all command line arguments, then call main with them
    #
    parser = argparse.ArgumentParser(description='This is part of the UGA CSCI\
                                     8360 Project 3. Please vist our GitHub \
                                     project at \
                                     https://github.com/dsp-uga/team-booth-p3 \
                                     for more information regarding data \
                                     organizations, expectations, and examples\
                                     on how to execute out scripts.')

    parser.add_argument('-o','--outputDir', required=True, help='The base \
                        directory storing and unziping the neuron tiff images \
                        and some result files. These names are hard coded into\
                        this script.')

    args = parser.parse_args()
    main(args)



