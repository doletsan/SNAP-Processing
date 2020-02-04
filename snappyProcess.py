# Dole Tsan (Dole.Tsan@canada.ca)
# Last update: 2019/12/13
# Python version 2.7
# SNAP version 7.0

# --------------------------------------------------------------------------

# Functions used to perform preprocessing and mosaicing of SNAP images

# Current setting works for Canada Carman products

# --------------------------------------------------------------------------

import snappy
from snappy import ProductIO
from snappy import HashMap
from snappy import GPF
import os

# http://step.esa.int/docs/v6.0/apidoc/engine/

# To create one of these
# Make a graph with the functions and parameters you want
# Open and read the XML
# You want to look for <node id> for the name of the operator
# Then look for <parameters class> and the parameters under it
# It will look like <parameterName>VALUE</parameterName>

# Adds '_finished' to base file name
#   Variables:
#       > name: A full path to a file or folder
#   Return:
#       > A string containing the new name
#   Notes:
#       > 
#   Related:
#       > 
def defaultNaming(name):
    base = os.path.basename(name)

    newName, sep, tail = base.partition('.')
    
    return newName + '_finished' 

# Saves a SNAP product
#   Variables:
#       > product: A SNAP product object
#       > fileName: Full path to file to save product as
#       > fileType: String to represent the type of file to save product as
#   Return:
#       > True if file exists
#       > False if file does not exist
#   Notes:
#       > Check related for supported formats
#       > Extension is optional to be included for the fileName
#   Related:
#       > https://forum.step.esa.int/t/supported-formats/635
def save_product(product, fileName, fileType = 'GeoTiff'):
    ProductIO.writeProduct(product, fileName, fileType)

    return os.path.exists(fileName)

# Applies calibration processing onto a SNAP product
#   Variables:
#       > product: A SNAP product object
#   Return:
#       > SNAP product with calibration applied
#   Notes:
#       > Parameters should be modified as required depending on needs
#   Related:
#       > 
def do_calibration(product):
    # Object to hold parameters
    parameters = HashMap()

    # SNAP Calibration parameters
    parameters.put('auxFile', 'Latest Auxiliary File')
    parameters.put('outputImageInComplex', 'false')
    parameters.put('outputImageScaleInDb', 'false')
    parameters.put('createGammaBand', 'false')
    parameters.put('createBetaBand', 'false')
    parameters.put('outputSigmaBand', 'true')
    parameters.put('outputGammaBand', 'false')
    parameters.put('outputBetaBand', 'false')

    # Applies Calibration to given product
    output = GPF.createProduct('Calibration', parameters, product)

    return output

# Applies speckle filter processing onto a SNAP product
#   Variables:
#       > product: A SNAP product object
#   Return:
#       > SNAP product with speckle filter applied
#   Notes:
#       > Parameters should be modified as required depending on needs
#   Related:
#       > 
def do_speckle_filter(product):
    # Object to hold parameters
    parameters = HashMap()

    # SNAP Speckle Filter parameters
    parameters.put('filter', 'Boxcar')
    parameters.put('filterSizeX', '5')
    parameters.put('filterSizeY', '5')
    parameters.put('dampingFactor', '2')
    parameters.put('estimateENL', 'true')
    parameters.put('enl', '1.0')
    parameters.put('numLooksStr', '1')
    parameters.put('windowSize', '7x7')
    parameters.put('targetWindowSizeStr', '3x3')
    parameters.put('sigmaStr', '0.9')
    parameters.put('anSize', '50')

    # Applies Speckle Filter to given product
    output = GPF.createProduct('Speckle-Filter', parameters, product)

    return output

# Applies terrain correction processing onto a SNAP product
#   Variables:
#       > product: A SNAP product object
#   Return:
#       > SNAP product with terrain correction applied
#   Notes:
#       > Parameters should be modified as required depending on needs
#       > proj variable should be modified to match the projection of the product
#   Related:
#       > 
def do_terrain_correction(product):
    # Object to hold parameters
    parameters = HashMap()

    # Modify to fit the projection of the images
    proj = 'PROJCS["UTM Zone 14 / World Geodetic System 1984",GEOGCS["World Geodetic System 1984",DATUM["World Geodetic System 1984",SPHEROID["WGS 84", 6378137.0, 298.257223563, AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich", 0.0, AUTHORITY["EPSG","8901"]],UNIT["degree", 0.017453292519943295],AXIS["Geodetic longitude", EAST],AXIS["Geodetic latitude", NORTH]],PROJECTION["Transverse_Mercator"],PARAMETER["central_meridian", -99.0],PARAMETER["latitude_of_origin", 0.0],PARAMETER["scale_factor", 0.9996],PARAMETER["false_easting", 500000.0],PARAMETER["false_northing", 0.0],UNIT["m", 1.0],AXIS["Easting", EAST],AXIS["Northing", NORTH]]'

    # SNAP Terrain Correction parameters
    parameters.put('demName', 'SRTM 1Sec HGT')
    parameters.put('externalDEMNoDataValue', '0.0')
    parameters.put('externelDEMApplyEGM', 'true')
    parameters.put('demResamplingMethod', 'BILINEAR_INTERPOLATION')
    parameters.put('imgResamplingMethod', 'BILINEAR_INTERPOLATION')
    parameters.put('pixelSpacingInMeter', '10.0')
    parameters.put('pixelSpacingInDegree', '0.0')
    parameters.put('mapProjection', proj)
    parameters.put('alignToStandardGrid', 'false')
    parameters.put('standardGridOriginX', '0.0')
    parameters.put('standardGridOriginY', '0.0')
    parameters.put('noDataValueAtSea', 'true')
    parameters.put('saveDEM', 'false')
    parameters.put('saveLatLon', 'false')
    parameters.put('saveIncidenceAngleFromEllipsoid', 'false')
    parameters.put('saveLocalIncidenceAngle', 'false')
    parameters.put('saveProjectedLocalIncidenceAngle', 'false')
    parameters.put('saveSelectedSourceBand', 'true')
    parameters.put('outputComplex' ,'false')
    parameters.put('applyRadiometricNormalization', 'false')
    parameters.put('saveSigmaNought', 'false')
    parameters.put('saveGammaNought', 'false')
    parameters.put('saveBetaNought', 'false')
    parameters.put('incidenceAngleForSigma0', 'Use projected local incidence angle from DEM')
    parameters.put('incidenceAngleForGamma0', 'Use projected local incidence angle from DEM')
    parameters.put('auxFile', 'Latest Auxiliary File')

    # Applies Terrain Correction to given product  
    output = GPF.createProduct('Terrain-Correction', parameters, product)

    return output

# SAR mosaics a list of SNAP products into a single image
#   Variables:
#       > product: A SNAP product object
#   Return:
#       > A mosaiced SNAP product
#   Notes:
#       > Parameters should be modified as required depending on needs
#   Related:
#       > 
def do_sar_mosaic(products):
    # Object to hold parameters
    parameters = HashMap()

    # SNAP SAR Mosaic parameters
    parameters.put('resamplingMethod', 'BILINEAR_INTERPOLATION')
    parameters.put('average', 'false')
    parameters.put('normalizeByMean', 'false')
    parameters.put('gradientDomainMosaic', 'false')
    parameters.put('pixelSize', '10.0')
    parameters.put('sceneWidth', '9407')
    parameters.put('sceneHeight', '6661')
    parameters.put('feather', '0')
    parameters.put('maxIterations', '5000')
    parameters.put('convergenceThreshold', '1.0E-4')

    # Applies SAR Mosaic to create a single product
    output = GPF.createProduct('SAR-Mosaic', parameters, products)

    return output

# Applies preprocessing to a list of product paths and saves them as a TIFF file
#   Variables:
#       > files: A list of full paths to SNAP-compatible files
#       > dest: Full path to folder to save images to
#       > nameFunc: A function with a single parameter that determines the name of the new image file
#   Return:
#       > A list of paths referring to the new processed images
#   Notes:
#       > The nameFunc function should not return a full path, just a name
#       > SNAP-compatible files are those that can be read into SNAP
#       > Attempts to read file or the product.xml if it fails
#       > Performs Calibration -> Speckle Filter -> Terrain Correction
#   Related:
#       > 
def pre_process(files, dest, nameFunc = defaultNaming):

    # List to keep track of processed image paths
    output = []

    # Iterates through list of files
    print('Starting...')
    for i in files:
        print('Reading product...')

        # Try reading the file path by itself
        try:
            product = ProductIO.readProduct(i)
        except:
            # Try reading a product.xml within the file
            try:
                print('Checking product.xml...')
                product = ProductIO.readProduct(os.path.join(i, 'product.xml'))
            except:
                print('Snap could not read product: %s' % i)
                continue
            
        print('Applying corrections...')

        # Apply preprocessing
        calibratedProduct = do_calibration(product)
        spkFilterProduct = do_speckle_filter(calibratedProduct)
        terCorrectedProduct = do_terrain_correction(spkFilterProduct)

        print('Creating product...')

        # Saving new product
        name = os.path.join(dest, nameFunc(i) + '.tif')
        ProductIO.writeProduct(terCorrectedProduct, name, 'GeoTiff')

        # Properly dispose in memory and close
        product.dispose()
        product.closeIO()

        output.append(name)

    return output

# Applies SAR mosaic to a list of SNAP files and saves as a TIFF file
#   Variables:
#       > files: A list of full paths to SNAP-compatible files
#       > fileName: Path to save the new product
#   Return:
#       > Boolean if file saved successfully
#   Notes:
#       > 
#   Related:
#       > 
def process_mosaic(files, fileName):
    
    products = [ProductIO.readProduct(i) for i in files]

    mosaic = do_sar_mosaic(products)

    return save_product(mosaic, fileName, 'GeoTiff')


