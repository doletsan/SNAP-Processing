# Dole Tsan (Dole.Tsan@canada.ca)
# Last update: 2019/12/11
# Python version 2.7
# SNAP version 7.0

# --------------------------------------------------------------------------

# Processes a directory of products and then mosaics them together depending
#   on the '_FQ##_Date####_'

# Call the preprocessAndMosaic() function with the directory as the parameter

# --------------------------------------------------------------------------

from snappyProcess import *
from mosaic import *

import re
import os
import sys

# Applies preprocessing to each product file in the directory and creates new
#   files in a 'processed' folder within the same directory. Performs calibration,
#   speckle filter, and backscatter on the products.
#   Variables:
#       > directory: Full file path to the product folder
#   Return:
#       > Two lists, first is a list of the paths to the processed products, the
#           second is a list of the paths to the original products that could not
#           be processed
#   Notes:
#       > New file name is the same with '_processed' appended to the end
#   Related:
#       > 
def preprocessAndMosaic(directory, delete = False):

    files = os.listdir(directory)
    assert(len(files) > 0, 'No files found in directory')
    files = [os.path.join(directory, x) for x in files]
    
    dest = os.path.join(directory, 'processed')
    if not os.path.exists(dest):
        os.makedirs(dest)

    print('Beginning preprocessing')
    processed = pre_process(files, dest, (lambda x: os.path.basename(x) + '_processed'))

    if len(processed) != len(files):
        print('Number of files processed does not match input')
        print('Processed %d out of %d' % (len(processed), len(files)))

    print('Performing mosaicing')
    return performMosaic(dest, delete)


# Can call from command line, requires one system argument for the directory
if __name__ == '__main__':

    # Check if there are 2 system inputs
    #   Should be [ThisScript.py, directory]
    if len(sys.argv) != 2 or len(sys.argv) != 3:
        print('Wrong number of arguments')
    else:
        directory = sys.argv[1]

        try:
            delete = sys.argv[2]
        except:
            delete = False

        preprocessAndMosaic(directory, delete)
