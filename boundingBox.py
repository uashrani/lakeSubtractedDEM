# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 14:19:07 2024

@author: Uma

Creates text file with rectangular bounding box around each HUC8 sub-watershed
Pads the watershed extent by 100m in each direction
"""

import grass.script as gs
import pandas as pd
import math

bufferFile = 'wsBuffer.txt'    # name of output file w/ padded HUC8 boundaries
mapName = 'dnr_watersheds_dnr_level_04_huc_08_majors'   # vector layer in Grass GIS
hucLevel = 'HUC_8'   # column name in the shapefile metadata

#%% Function definition

def createBoundingBox():
    """ Finds the extent of each subwatershed, 
    and calculates a rectangular bounding box padded by 100m 
    Outputs a DataFrame with the bounds and saves to file bufferFile"""
    
    # Grass GIS adds attribute columns with the extent of each subwatershed
    gs.run_command('v.to.db', map=mapName, option='bbox', \
                   columns=['n', 's', 'e', 'w'], overwrite=True)
        
    # Output the attribute table with the new columns as tmp.txt, and read it in
    gs.run_command('v.db.select', map=mapName, format='csv', file='tmp.txt', overwrite=True)
    rawBox = pd.read_csv('tmp.txt', dtype={'HUC4': 'str', 'HUC_8': 'str'})
    bufferBox = rawBox.copy()

    # Round N and E extents up to nearest integer, and round S and W down
    # Pad the subwatershed extent with 100m on each side
    for upCol in ['n','e']:
        col2 = pd.Series([(math.ceil(item)+100) for item in rawBox[upCol]])
        bufferBox[upCol]=col2
        
    for downCol in ['s', 'w']:
        col2 = pd.Series([(math.floor(item)-100) for item in rawBox[downCol]])
        bufferBox[downCol]=col2
        
    colArea = (bufferBox['n']-bufferBox['s'])*(bufferBox['e']-bufferBox['w'])
    bufferBox['rectArea']=colArea
        
    bufferBox.to_csv(bufferFile, index=False)
    
    return bufferBox
    
#%% Create bounding-box text file
bufferBox = createBoundingBox()

