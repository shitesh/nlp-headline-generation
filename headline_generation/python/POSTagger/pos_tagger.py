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
    count =1
    for directory in os.listdir(input_directory):
        directory_path = os.path.join(input_directory, directory)
        for file_name in os.listdir(directory_path):
            file_path = os.path.join(directory_path, file_name)
            out_path = os.path.join(output_directory, '%s_TAGGED.txt' % count)
            count += 1

            input_file = open(file_path, 'r')
            output_file = open(out_path, 'w')

            tags = []
            for line in input_file:
                line = line.strip()
                if '<Headline>' in line:
                    output_file.write('<Headline>\n')
                    line = line.replace('<Headline>', '')

                elif line in ['</Headline>', '<text>', '</text>']:
                    output_file.write('%s\n' % line.strip())
                    tags.append(line.strip())
                    continue

                parts = line.split()
                if '</Headline>' in tags and len(parts) < 5:
                    continue

                line = line.decode('utf-8')
                parts = line.split(u'।')
                for part in parts:
                    if not part:
                        continue
                    part = part.encode('utf-8')

                    # need to remove trailing whitespace after each word
                    words = part.split()
                    words = [word.strip() for word in words]
                    part = ' '.join(words)

                    tagged_text = tagger.tagRawSentence(DICT, part)
                    output_file.write('%s\x01' % tagged_text)
                output_file.write('\n')
            output_file.close()

if __name__ == '__main__':
    initialise()
    parse_directory(sys.argv[1], sys.argv[2])
