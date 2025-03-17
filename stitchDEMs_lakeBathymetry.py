# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 12:58:59 2025

@author: Uma

Uses the lake bathymetry dataset from MN Geospatial Commons
(5-m resolution raster data of lake depths, with null values for land)
to create a DEM with lake depths subtracted.

The primary dataset is 1-m LiDAR.

Looping through each HUC8 sub-watershed, the program
    - resamples and interpolates the 5-m lake depths to 1-m resolution
    - subtracts lake depth from the LiDAR (note on signs and units below)
    - Outputs the new DEM for that sub-watershed to a file
    
Note: The lake bathymetry dataset has units of ft, and also is entirely negative numbers.
This is accounted for in the r.mapcalc calculation.
"""

import grass.script as gs
import grass.grassdb.data as gdb
import pandas as pd
import os

wsBufferFile = 'wsBuffer.txt'   # this was created in grassScript.py
bathFile = '/home/uashrani/Documents/lake_bathymetric_elevation_model.tif'       # MN Geospatial Commons data
lidarFile = '/media/uashrani/topobathy-ditch/MinnesotaLiDAR.tif'         # Path to 1m LiDAR

# The program creates the following two layers in your GRASS location
DEM_1m = 'demSource'
DEM_5m = 'lakeBathymetry'   

# Where output files will be written (each gets their own sub-directory inside)
outParentDir = '/media/uashrani/topobathy-ditch/outputs/'

#%% Function definition
 
def clipResampInterpStitch(n, s, e, w, outName, testing):
    """ Takes N, S, E, W boundaries of the specified region (usually a sub-watershed). 
    Interpolates the bathymetry to 1m in this region, converts units, 
    and adds the negative depth to the full surface DEM. 
    Outputs to a raster (tiff) file given by outName.
    
    If testing is True, the function outputs the interpolated lake depths 
    and the original LiDAR before lakes were subtracted. 
    These can be helpful for plotting, but would slow the program down on a large scale.
    """
    
    outDir = outParentDir + outName + '/'
    if not os.path.exists(outDir):
        os.mkdir(outDir)

    # Set computational region to the inputted coordinates
    gs.run_command('g.region', flags='p', n=n, s=s, e=e, w=w, res=1)

    # Now interpolate/resample the grown lake-depth DEM across that region
    interpBath = outName + '_interp'
    gs.run_command('r.resamp.interp', input=DEM_5m, output=interpBath, overwrite=True)   
    
    # Add the negative lake depths to the surface DEM. The .3048 is to convert from ft to m
    subtractedName = outName + '_subtracted'
    expression = subtractedName + ' = ' + '.3048 * if(isnull(' + interpBath + '), 0, ' \
        + interpBath + ')' + ' + ' + DEM_1m
    gs.run_command('r.mapcalc', expression=expression, overwrite=True)  
    # Convert to height above baseline in cm, lets us represent as int
    intName = outName + '_int'
    # Pseudocode: intName = round((DEM - 100) * 100)
    expression = intName + ' = ' + 'round((' + subtractedName + '-100)*100)'
    gs.run_command('r.mapcalc', expression=expression, overwrite=True)
    # Output the new lake-subtracted DEM for that region
    gs.run_command('r.out.gdal', flags='f', input=intName, output=outDir + outName+'.tif', \
                   format='GTiff', createopt="COMPRESS=LZW,BIGTIFF=YES", overwrite=True, type='UInt16')
        
    # Output the files for some of the intermediate steps, only if you want to test the program
    if testing==True:
        # Interpolated lake depths
        gs.run_command('r.out.gdal', input=interpBath, output=outDir + interpBath + '.tif', \
                          format='GTiff', createopt="COMPRESS=LZW,BIGTIFF=YES", overwrite=True)
        # LiDAR 
        gs.run_command('r.out.gdal', input=DEM_1m, output=outDir + outName+'_lidar.tif', \
                       format='GTiff', createopt="COMPRESS=LZW,BIGTIFF=YES", overwrite=True)
        
    
#%% Looping through sub-watersheds
    
# text file with HUC8 sub-watershed boundary definitions
wsBuffer = pd.read_csv(wsBufferFile, dtype={'HUC4': 'str', 'HUC_8': 'str'})

# Create external links to the lake bathymetry and LiDAR datasets
if not (gdb.map_exists(DEM_5m, 'raster')):
    gs.run_command('r.external', input=bathFile, output=DEM_5m, flags='r')
    
if not (gdb.map_exists(DEM_1m, 'raster')):
    gs.run_command('r.external', input=lidarFile, output=DEM_1m, flags='r')

# Eventually loop through all sub-watersheds, but test a couple for now
# Index positions of certain watersheds: 
#   - Thief River(i=63) - test watershed
#   - Redwood River(i=6) - test watershed
#   - Rainy River(i=78) - largest in area
#   - Upper Wapsipinicon River(i=28) - smallest in area
for i in [63]:    #range(len(wsBuffer)):    # Loop over subwatersheds
    subWS = wsBuffer.iloc[i]
    n, s, e, w = subWS['n'], subWS['s'], subWS['e'], subWS['w']     # Subwatershed boundaries - for test purposes use a smaller region
    outName = 'HUC_' + subWS['HUC_8']
    
    clipResampInterpStitch(n, s, e, w, outName, False)
       