'''
Name       : CombinePDFs.py
Description: Module with methods to combine PDFs
Date       : 22-Jan-2023
Author     : M. Schmidt
'''

import argparse
import sys
from pypdf import PdfMerger


def parse_args():
    parser = argparse.ArgumentParser(
        prog='Combine PDFs',
        description='Merges PDF files from a folder to a single file',
        epilog='Thank you and have a nice day! :)')

    parser.add_argument('inputFiles', type=str,
        nargs='*', help='Two or more PDF files to be merged')
    parser.add_argument('output', type=str,
        help='Full path to output PDF file')

    args = parser.parse_args(sys.argv[1:])

    return args


def pdf_cat(input_files, output_file):
    try:
        merger = PdfMerger()
        for pdf in input_files:
            merger.append(pdf)
        merger.write(output_file)
        merger.close()
    except:
        print("Error merging PDFs")


if __name__ == '__main__':
    cfg = parse_args()
    pdf_cat(input_files=cfg.inputFiles, output_file=cfg.output)
