# -*- coding: utf-8 -*-
import codecs
import sys
import os
import gzip

OUTPUT_FOLDER = '/tmp/output-data'
check_test = u"इंडो-एशियन न्यूज सर्विस"

def process_directory(top_level_directory):
    """Processes the text files in input directory and puts the final data as a text file in the output directory.

    """
    file_count=1
    for directory in os.listdir(top_level_directory):
        directory = os.path.join(top_level_directory, directory)
        for file_name in os.listdir(directory):
            file_path = os.path.join(directory, file_name)
            print file_path
            file = codecs.getreader('utf-8')(gzip.open(file_path, 'r'))
            count = 0
            out_file = codecs.open(os.path.join(OUTPUT_FOLDER, '%s.txt' % file_count), 'w', encoding='utf-8')
            out_file.write('%s\n' %(file_path))
            for line in file:
                count += 1
                if count ==1:
                    out_file.write('<headline>\n')
                    headline = line.replace('Hindi News: Boloji.com :','')

                    out_file.write('%s\n' % headline.strip())
                    out_file.write('</headline>\n')
                    out_file.write('<text>\n')
                    continue
                if count < 7 or not line.strip():
                    continue
                if check_test in line or 'Shop Gifts Online' in line:
                    break

                out_file.write('%s' % line)
            out_file.write("</text>")
            out_file.close()
            file_count += 1


if __name__ == '__main__':
    process_directory(sys.argv[1])
