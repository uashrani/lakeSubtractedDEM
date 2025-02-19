# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 14:19:07 2024

@author: Uma
"""

import grass.script as gs
import pandas as pd
import math
import os

bufferFile = 'bufferShp.txt'    # name of file containing buffer around each subwatershed, whether the file exists yet or not
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
    gs.run_command('v.db.select', map=mapName, format='csv', file='tmp.txt')
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
        
    bufferBox.to_csv(bufferFile, index=False)
    
    return bufferBox
    
#%% Create bounding-box text file
bufferBox = createBoundingBox()

