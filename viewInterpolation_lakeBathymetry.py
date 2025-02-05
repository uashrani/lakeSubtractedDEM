# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 14:05:24 2024

@author: Uma
"""

import rioxarray
import numpy as np
import matplotlib.pyplot as plt

#%% Compare bathymetry file with the LiDAR

baseName = 'whiteBearLake'
baseName = 'outputs/' + baseName + '/' + baseName

# These are the same file names and directories that the stitching program outputted
fileStitched=baseName + '_stitched.tif'
fileLidar=baseName + '_lidar.tif'
fileInterp=baseName + '_interp.tif'

fig, axs = plt.subplots(1, 3, figsize=(18, 10))
fig.suptitle('Comparison of Stitched vs Individual DEMs', y=0.93)

# Plot interpolated lake depth: multiply the depth by -0.3048 to convert from ft to m
rasInterp=rioxarray.open_rasterio(fileInterp, masked=True).squeeze()
p0 = axs[0].pcolormesh(rasInterp.x, rasInterp.y, -.3048 * rasInterp.data, cmap='Blues')
rasInterp.close()       # close each raster before opening the next one

# Lake depth gets its own colorbar
c0 = fig.colorbar(p0, ax=axs[0], location='bottom', pad=0.07)
c0.set_label('Depth [m]')

## Now plot full DEMs
# Plot the lake-subtracted DEM, and find the data min and max for the colorbar
rasStitched=rioxarray.open_rasterio(fileStitched, masked=True).squeeze()
vmin,vmax=np.nanmin(rasStitched.data), np.nanmax(rasStitched.data)
p2 = axs[2].pcolormesh(rasStitched.x, rasStitched.y, rasStitched.data, vmin=vmin, vmax=vmax)
rasStitched.close()

# Plot the LiDAR DEM, sharing a colorbar with the lake-subtracted one
rasLidar=rioxarray.open_rasterio(fileLidar, masked=True).squeeze()
p1 = axs[1].pcolormesh(rasLidar.x, rasLidar.y, rasLidar.data, vmin=vmin, vmax=vmax)
rasLidar.close()

titles = ['Interpolated Bathymetry', '1m LiDAR', 'Summed LiDAR and Bathymetry']

for (i,ax) in enumerate(axs):
    ax.set_xlabel('Easting [m]')
    ax.set_ylabel('Northing [m]')
    ax.set_title(titles[i])
    
c = fig.colorbar(p2, ax=[axs[1],axs[2]], location='bottom', \
                  pad=0.07, shrink=0.8)
c.set_label('Elevation [m]')





