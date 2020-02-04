# Dole Tsan (Dole.Tsan@canada.ca)
# Last update: 2019/12/10
# Python version 2.7
# Arcpy version 10.5
# SNAP version 7.0

# --------------------------------------------------------------------------

# Mosaics a directory of folders together depending on the '_FQ##_Date####_'

# Call the performMosaic() function with the directory as the parameter

# --------------------------------------------------------------------------

from snappyProcess import *
import itertools
import re
import os
import sys

# Reads product name for the FQ and date
#   Variables:
#       > x: A string containing the product name
#   Return:
#       > A string containing the FQ and date
#       > None if it cannot be found
#   Notes:
#       > Uses regex to parse filename
#   Related:
#       > 
def parseProductName(x):
    reg = re.search('_(FQ[0-9W]{1,3}_[0-9]{8})_', x, re.IGNORECASE)
    
    if (reg == None):
        return None
    return reg.group(1)

# Groups products in the provided list by the FQ and date
#   Variables:
#       > myList: A list of strings for the products paths
#   Return:
#       > A list of lists where the inner list refers to the groups
#   Notes:
#       > Uses regex to parse filename
#   Related:
#       > 
def groupS2Files(myList):
    myList.sort()

    groupedList = list()
    
    for key, group in itertools.groupby(myList, parseProductName):
        groupedList.append(list(group))

    return groupedList

# Groups product files with similar FQ and dates to create a new mosaiced product
#   Variables:
#       > directory: Full file path to the product folder
#       > delete: Boolean to delete files used in mosaicing process
#   Return:
#       > Two lists, first is a list of the paths to the processed products, the
#           second is a list of the paths to the original products that could not
#           be processed
#   Notes:
#       > Creates a new folder within the directory called 'mosaic'
#       > File name is 'FQ##_[Date]_mosaic.tif'
#   Related:
#       > 
def performMosaic(directory, delete = False):

    # Get list of products in directory, basename only
    files = os.listdir(directory)

    # Checks that there are files in the directory
    assert(len(files) != 0, 'Could not determine files in directory')

    # Create new folder to save files into
    saveLocation = os.path.join(directory, 'mosaic')
    if not os.path.exists(saveLocation):
        os.makedirs(saveLocation)

    groupedFiles = groupS2Files(files)

    finished = list()
    unfinished = list()
    
    for i in range(len(groupedFiles)):
        print('Working on group %d' % (i + 1))
        
        group = groupedFiles[i]

        # Creates a file name based on one of the rasters in the group
        #   Should be the same name since same FQ and date
        saveName = os.path.join(saveLocation, parseProductName(group[0]) + '_mosaic')

        # Concatenate old directory to file to get product
        group = [os.path.join(directory, x) for x in group]

        try:
            print('Beginning mosaic process...')
            process_mosaic(group, saveName)

            if delete:
                print('Deleting pre-mosaiced files...')
                for j in group:
                    os.remove(j)
            
            finished.append(saveName)
        except:
            print('Could not process group %d' % (i + 1))
            unfinished.append(group)

    return finished, unfinished

# Can call from command line, requires one system argument for the directory
if __name__ == '__main__':

    # Check if there are 2 system inputs
    #   Should be [ThisScript.py, directory]
    if len(sys.argv) != 2:
        print('Wrong number of arguments')
    else:
        
        # Read system arguments for directory path
        directory = sys.argv[1]

        # Perform mosaicing, save into 2 variables
        #   finished = list of file names for created products
        #   unfinished = list of lists for each group that failed
        finished, unfinished = performMosaic(directory)

        print('Finished: %d files created' % len(finished))
        print('Unfinished: %d groups failed' % len(unfinished))
   
    
