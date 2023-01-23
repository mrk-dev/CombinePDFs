'''
Name       : combine_helper.py
Description: Helper methods for Combine PDFs
Date       : 22-Jan-2023
Author     : M. Schmidt
'''

import os
import time
import CombinePDFs


def combinepdfs(source_folder, output_file):
    pdfs = get_pdfs(source_folder)

    ret_val = len(pdfs)

    if len(pdfs) > 1:
        writepdf(output_file, pdfs)
    else:
        print("1 or fewer PDFs to combine.  No work done.")

    return ret_val


def monitorpdfs(source_folder, output_file, delay_seconds=5):
    delay_seconds = 5 if delay_seconds < 0 else delay_seconds

    print("\n*** START AUTO PDF COMBINE ***\n")
    print("Monitoring {0} for pdfs every {1} seconds.".format(source_folder, delay_seconds))
    print("Output saved to {0}.".format(output_file))

    while 1==1:  # go forever until program killed

        time.sleep(delay_seconds) 
        print("Checking folder...", end='')

        pdfs = get_pdfs(source_folder)

        if len(pdfs) > 1:
            print("found {0} pdfs".format(len(pdfs)))
            outfile = get_outfile_name(output_file)

            writepdf(outfile, pdfs)
            delete_pdfs(pdfs)
        else:
            print("nothing found")


def writepdf(outfile, pdfs):
    print("Outfile-->{0}".format(outfile))
    outfile = open(outfile, "wb")
    CombinePDFs.pdf_cat(pdfs, outfile)
    print("Done.")

    return len(pdfs)


def delete_pdfs(pdf_list):
    for pdf in pdf_list:
        try:
            os.remove(pdf)
        except:
            print("***ERROR*** could not delete {0}".format(pdf))


def get_pdfs(source_folder):
    pdfs = []
    for f in os.listdir(source_folder):
        if f.lower().endswith(".pdf"):
            print("-->{0}".format(f))
            pdfs.append(os.path.abspath(os.path.join(source_folder,f)))

    pdfs.sort()

    return pdfs


def get_outfile_name(base_name):
    test_filename = base_name
    while os.path.exists(test_filename):
        file_name, ext = os.path.splitext(test_filename)
        
        # extract digits from end of file name
        strpos = len(file_name) - 1
        count = 0
        while str.isdigit(file_name[strpos]):
            strpos -= 1
        if strpos < len(file_name) -1:
            count = int(file_name[strpos+1:])
            file_name = file_name[:strpos+1]

        count += 1
        test_filename = "{0}{1}{2}".format(file_name, count, ext)

    return test_filename
