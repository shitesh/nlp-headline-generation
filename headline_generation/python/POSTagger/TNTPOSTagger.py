#!/usr/bin/python
# -*- coding: utf-8 -*
import os
import sys
print sys.getdefaultencoding()
from sys import argv
#For reading command line input
#Usage: python NewParser2.py "/home/mandyamd/Downloads/pos_tagger/hindi-pos-tagger-3.0/data">myout22.txt
script, input = argv

#########################################Structure Definitions#################################################################
#this counter maintains the word count in a particular line
Word_Count_In_Line = 0
#This Structure stores the files in a particular input directory
Files_in_Directory = []
#File Count used to number the output files
FileCount =0
#########################################Structure Definitions#################################################################

######################################### Functions ###########################################################################
#Loops over the directory to get available files  
def GetFilesInFolder():
    for dirName, subdirList, fileList in os.walk(input):
            for fname in fileList:
                if fname.endswith(".txt"):
                    fn = os.path.join(dirName,fname)
                    Files_in_Directory.append(fn)
#This function executes POS tagger and writes the contents to "hindi.output"
def Execute_POSTagger(fname):
    print "filename:"+fname
    command1 = "cat "+fname+" | ./bin/unitok.py -l hindi -n | sed -e 's/?/./g' | sed -e 's/^\.$/.\\n<\/s>\\n<s>/g' |  ./bin/normalize_vert.py  > hindi.tmp.words"

    os.system(command1)
    print "Executed command 1"
    commnad2 = "./bin/tnt -v0 -H models/hindi   hindi.tmp.words | sed -e 's/\t\+/\t/g' | ./bin/lemmatiser.py models/hindi.lemma | ./bin/tag2vert.py > hindi.output"
    os.system(commnad2)
    print "Executed command 2"
    os.system("rm hindi.tmp.words")
    print "Executed command 3"

#open each file,Get it POS tagged and write the contents to Output file
def Generate_POS_Tagged_Files():
    file_data = ""	
    global FileCount,Word_Count_In_Line	
    for fname in Files_in_Directory:
       with open(fname, 'r') as filename:
        #this structure appends the words and tags and finally this string is written to output file.
        file_data = ""

	# Contains words from input file with tags
    	Output_file_data = []
	
        Execute_POSTagger(fname)

        #file pointer to new output file generated for each of the input files
        FileP = "out"+str(FileCount)+".txt"
        outFile =  open(FileP,'w')
	
        FileCount = FileCount+1
	#File pointer to the output file from SivaReddy POS Tagger
	inputFile = open('hindi.output','r')

        for line in inputFile:

            line = line.strip()
            WordOfLine = line.split()

            for word in WordOfLine:

                    if Word_Count_In_Line==0:
                        TempString = ""+word+"/"

                    if Word_Count_In_Line==2:
                        TempString = TempString+word
                    	Output_file_data.append(TempString)
                    	Word_Count_In_Line=0
                    	break
            	    Word_Count_In_Line = Word_Count_In_Line+1
        print "data collected:"
        for TaggedOutput in Output_file_data:
                file_data = file_data+" "+TaggedOutput
        print file_data
	
	
        print "writing to file: "+FileP
        outFile.write(file_data)
        outFile.close()
	file_data = ""	
	inputFile.close()
######################################### Functions ###########################################################################


######################################### Main function ###########################################################################

GetFilesInFolder()
Generate_POS_Tagged_Files()


######################################### Main function ###########################################################################



