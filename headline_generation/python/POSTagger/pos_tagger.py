# -*- coding: utf-8 -*-
import os
import sys
from RDRPOSTagger.pSCRDRtagger.RDRPOSTagger import RDRPOSTagger
from RDRPOSTagger.Utility.Utils import readDictionary


DICTIONARY_LOCATION = '../Models/POS/Hindi.DICT'
RDR_LOCATION = '../Models/POS/Hindi.RDR'
tagger, DICT = None, None


def initialise():
    global tagger, DICT
    tagger = RDRPOSTagger()
    tagger.constructSCRDRtreeFromRDRfile(RDR_LOCATION)
    DICT = readDictionary(DICTIONARY_LOCATION)


def parse_directory(input_directory, output_directory):
    global tagger, DICT

    for file_name in os.listdir(input_directory):
        file_path = os.path.join(input_directory, file_name)
        out_path = os.path.join(output_directory, '%s_TAGGED' % file_name)

        input_file = open(file_path, 'r')
        output_file = open(out_path, 'w')

        line = input_file.readline()
        tags = []
        for line in input_file:
            line = line.strip()
            if line in ['<headline>', '</headline>', '<text>', '</text>']:
                output_file.write('%s\n' % line.strip())
                tags.append(line.strip())
                continue
            parts = line.split()
            if '</headline>' in tags and len(parts) < 5:
                continue
            line = line.decode('utf-8')
            parts = line.split(u'।')
            for part in parts:
                if not part:
                    continue
                part = part.encode('utf-8')
                tagged_text = tagger.tagRawSentence(DICT, part)
                output_file.write('%s\x01' % tagged_text)
            output_file.write('\n')
        output_file.close()

if __name__ == '__main__':
    initialise()
    parse_directory(sys.argv[1], sys.argv[2])