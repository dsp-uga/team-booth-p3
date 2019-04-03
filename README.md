# team-booth-p3 - Project 3 - CSCI 8360 - Neuron Finding
## Team Booth

## Member (Ordered by last name alphabetically)
* Abhishek Chatrath (ac06389@uga.edu)
* Priyank Malviya (priyank.malviya@uga.edu)
* Jonathan Myers (submyers@uga.edu)

## Synopsis

We provide one Python script approach for downloading and analyzing microscopic images to derive neuron locations based on visible fluctuations in calcium concentration. Our software takes advantage of Non-Negative Matrix Factorization (NMF) to derive patterns in the image matrixes by building complementary base and factor matrices using gradient decent. These matrices serve, along with image adjustment, serve as a basis for predicting neuron locations.

## Outline

This package comes with the following directories, scripts, and files:

* img/ : Directory holds images referenced by our Wiki page
* src/ : Directory hold scripts for other ideas we tested
* doc/ : Directory holds this assignment's pdf file
* data/ : Contains predictions generated by our software along with parameters used
* downloadNeuronData.py : A python script that will download and extract all matrix values used in this project
* nmfProcess.py : A python script that applies image adjustment and NMF to the target images to generate neuron location predictions

## Expectations

Our python scripts take advantage of skimage and extraction packages. Due to recent changes to Python, you may get these packages through PIP command, such as 

```
$ pip install scikit-image
$ pip install thunder-extraction
```

, or, if you are using Anaconda, commands such as

```
$ conda install -c conda-forge scikit-image
$ conda install -c conda-forge thunder-extraction
```

If you use Anaconda in a Linux or Mac environment, be sure to incorporate the anaconda paths into your global PATH variable, example from .bashrc:

```
PATH=/anaconda3/bin:$PATH
```

## Image Data

The GitHub site https://github.com/codeneuro/neurofinder contains links to the "neurofinder" data we used to evaluate the efficiency of our software. Their website provides a nice introduction to the problem, expectations for the results generated, and links to software used to evaluate performance. DUE NOTE: The links on the page to neurofinder.04.00.test and neurofinder.04.01.test are incorrect; they should be https://s3.amazonaws.com/neuro.datasets/challenges/neurofinder/neurofinder.04.00.test.zip and https://s3.amazonaws.com/neuro.datasets/challenges/neurofinder/neurofinder.04.01.test.zip respectively.

The Python script downloadNeuronData.py could download and extract all neurofinder data for you by executing the following command in our core directory:

```
$ python downloadNeuronData.py -o ./data/
```

This command begins a process downloading all 26 files hard-coded into the script and supported by https://github.com/codeneuro/neurofinder: 17 for training and 9 for testing. Once you have directories storing neurofinder data, you are prepared to apply the filtering and NMF operations discussed in the following section.

## NMF Process

We looked to Thunder-Extraction (https://github.com/thunder-project/thunder-extraction) to gain access to the NMF function that has shown success in previous work (https://github.com/dsp-uga/bath). Application of the NMF function and image processing exists in the "nmfProcess.py" Python script; here is one simple execution using one of the neurofinder data sets:


```
$ python nmfProcess.py -d data/neurofinder.00.00.test/ -o regions.00.00.test.json
```


The process will read through all images in the neurofinder.00.00.test/images/ directory, apply filtering and NMF, and finally generate a regions.00.00.test.json file. Defining the output file isn't required, but it would be helpful later because the nmfProcess.py script only looks at one target neurofinder data set per execution (see later for wrapping results together for later evaluation). In general, execution of nmfProcess.py can take the following arguments:

```
usage: nmfProcess.py [-h] -d SOURCEDIR [-s SAMPLESIZE] [-o OUTPUTFILE] [-norm]
                     [-nmf_k NMF_K] [-nmf_maxIter NMF_MAXITER]
                     [-nmf_percentile NMF_PERCENTILE]
                     [-nmf_overlap NMF_OVERLAP] [-nmf_minSize NMF_MINSIZE]
                     [-fit_chunkSize FIT_CHUNKSIZE] [-fit_padding FIT_PADDING]
                     [-fit_mergeIter FIT_MERGEITER]
                     [-merge_kNearest MERGE_KNEAREST]
```


The script only demands definition of the source directory (the directory generated earlier by unzipping one of the neurofinder data zip files) - all other parameters have default values:


* -o, --outputFile : Name of the output file (Default - "regions.json")
* -norm, --normalize : Normalize the image before NMF (Default - False)
* -nmf_k, --nmf_k: The first NMF parameter, see below (Default - 5)
* -nmf_maxIter, --nmf_maxIter : The second NMF parameter, see below (Default - 20)
* -nmf_percentile, --nmd_percentile : The third NMF parameter, see below (Default - 99)
* -nmf_overlap, --nmf_overlap : The fourth NMF parameter, see below (Default - 0.1)
* -nmf_minSize, --nmf_minSize : The fifth NMF parameter, see below (Default - 20)
* -fit_chunkSize, --fit_chunkSize : The first Fit parameter, see below (Default - 32,32)
* -fit_padding, --fit_padding : The second Fit parameter, see below (Default - 20,20)
* -merge_kNearest, --merge_kNearest : The first Merge parameter, see below (Default - 20)


The derivation of NMF matrixes, building new models from the matrixes, and merging the predicted regions into a consensus result takes place in the nmfProcess.py script function applyNMF. The following block illustrates how the code is called and where command line parameters are referenced:


```
    model = NMF(k=args.nmf_k, max_iter=args.nmf_maxIter,
                percentile=args.nmf_percentile, overlap=args.nmf_overlap,
                min_size=args.nmf_minSize)
    model = model.fit(imageList, chunk_size=chunkSize,
                      padding=padding)
    merged = model.merge(overlap=args.nmf_overlap, max_iter=args.fit_mergeIter,
                         k_nearest=args.merge_kNearest)
    regions = [{'coordinates': region.coordinates.tolist()}
        for region in merged.regions]
```


The padding and chunkSize values are tuples derived from the comma delimited command line arguments, while all other values are simply references to the command line values provided.

## Final Step

The people at https://github.com/codeneuro/neurofinder supplied software to evaluate how well the software you used predicted results. It expects to see results for all 9 of the neurofinder tests, but since our software generates a different region prediction json file for each execution, you will likely need to concatenate all the results together while still maintaining the expected format. We supply a VERY BASIC Perl script in the example data directory (data/nmf/run1) that will take all json files in the current directory that end with "test.json" and concatenates them together to form one json file; this example shows it generating the file regions.json:


```
$ perl merge.pl > regions.json
```


This basic script worked for us, but feel free to replace this script with anything else that maybe more comfortable for you and your work.

## Last Note

Due to many challenges on Google Cloud Platform, Tensorflow, and Watershed approaches, we had to take advantage of techniques that have proven themselves useful over the years, most specifically NMF. Please visit our Wiki page for further discussion on the NMF, the works of others that gave us guidance, and notes on different ideas we looked into.

 
