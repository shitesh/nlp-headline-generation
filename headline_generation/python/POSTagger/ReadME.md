**TNTPOSTagger.py:**

This script is based on Siva Reddys' implementation of POS tagger (https://bitbucket.org/sivareddyg/hindi-part-of-speech-tagger).  

This file takes as input folder containing the data source.  

Usage: python TNTPOSTagger.py path_of_directory_containing_data  

Steps:  
1) Parses the directory to collect all the files in the directory  
2) Runs the POS tagger on each file  
3) Creates the output file   
4) Generates the output for each file in word/Tag format  


**pos_tagger.py**

This script is based on RDRPOSTagger(https://github.com/datquocnguyen/RDRPOSTagger). Its a rule based tagger that employs an error-driven approach to automatically construct tagging rules in the form of a binary tree. This provides a faster way to tag Hindi text. The details can be found at -  [RDRPOSTagger](http://rdrpostagger.sourceforge.net/)  

Usage : python pos_tagger.py input_directory output_directory  

The script takes two arguments as input:  
1. path of directory containing Hindi text files.  
2. path of directory where output is stored.  

It reads each file from the input directory and creates a corresponding file in output directory. The output file is created by appending 'TAGGED' to the input file name.  

