TNTPOSTagger.py:

This script is based on Siva Reddys' implementation of POS tagger(https://bitbucket.org/sivareddyg/hindi-part-of-speech-tagger).

This file takes as input folder containing the data source.

Usage: python TNTPOSTagger.py path_of_directory_containing_data

Steps:
1) Parses the directory to collect all the files in the directory
2) Runs the POS tagger on each file
3) Creates the output file 
4) Generates the output for each file in word/Tag format

