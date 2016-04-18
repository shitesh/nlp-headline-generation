import codecs
import os
import sys
from decoding import initialise_all, get_file_headings
from Utils import remove_tags_from_line


def get_file_path(input_path):
    """Creates a temp file which maintains the format in which decoding algorithm implements it.

    """
    temp_location = '/tmp/trial.txt'
    out_file = codecs.open(temp_location, 'w', encoding='utf-8')
    in_file = codecs.open(input_path, 'r', encoding='utf-8')

    line = in_file.readline() # <Headline>
    headline = in_file.readline() # actual headline
    while line.strip() != '<text>':
        line = in_file.readline()

    line = in_file.readline()
    while line.strip()!= '</text>':
        out_file.write(line)
        line = in_file.readline()

    out_file.close()
    headline = remove_tags_from_line(headline.split())
    return headline, temp_location


def process_directory(input_dir, output_dir):
    """Processes all the files in input directory and writes the output to a different directory

    """
    for file_name in os.listdir(input_dir):
        output_file = os.path.join(output_dir, '%sprocessed.txt' % file_name)
        out_file = codecs.open(output_file, 'w', encoding='utf-8')
        headline, file_path = get_file_path(os.path.join(input_dir, file_name))
        top_sentences = get_file_headings(file_path, len(headline.split()))
        out_file.write('%s\n' % headline.strip())
        sentences = '\n'.join(top_sentences)
        out_file.write(sentences)
        out_file.close()

if __name__ == '__main__':
    initialise_all()
    process_directory(sys.argv[1], sys.argv[2])
