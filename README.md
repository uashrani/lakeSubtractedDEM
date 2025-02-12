# lakeSubtractedDEM
Subtracting lake depths from the Minnesota DEM using GRASS GIS and Python.

### Data sources
The lake depth data can be found from MN Geospatial Commons: https://gisdata.mn.gov/dataset/water-lake-bathymetry. The units of lake depth are in negative feet.

The program will also loop through the HUC8 sub-watersheds, found at: https://gisdata.mn.gov/dataset/geos-dnr-watersheds. In [another program](https://github.com/MNiMORPH/GRASS-drainageDitches/blob/main/grassScript.py), I created a text file that padded the N, S, E, and W boundaries of each sub-watershed by 100m. The [output text file](https://github.com/uashrani/lakeSubtractedDEM/blob/main/wsBuffer.txt) is also uploaded to this repository, since the program needs to open it. 

### Python program
#### [stitchDEMs_lakeBathymetry.py](https://github.com/uashrani/lakeSubtractedDEM/blob/main/stitchDEMs_lakeBathymetry.py)
The program adds a 10-m "buffer zone" around the edges of each lake, setting lake depth to 0. (Previously it was null/missing data.) It then resamples and interpolates the buffered lake-depth data from a 5-m resolution to a 1-m resolution. Next, it adds the (negative) depth to the LiDAR and outputs this file. There is an option to output some of the intermediate files as well, if you want to test the program on a small region first.

#### [viewInterpolation_lakeBathymetry.py](https://github.com/uashrani/lakeSubtractedDEM/blob/main/viewInterpolation_lakeBathymetry.py)
If you chose to output the intermediate files earlier, this program plots them. It plots lake depth, the surface LiDAR, and the lake-subtracted LiDAR side-by-side.  

### Initial Outputs
These are a few examples - I ran both the stitching program and the viewing program. The Chain of Lakes and the White Bear Lake seem to have a ring of depth=0 around the edge of the lake, so they blend somewhat smoothly with their surroundings. However, Lake Nokomis has nonzero depth even at the edge, and looks sharp in contrast to its surroundings. I am not sure if a secondary interpolation, across the lake boundary, will be needed in these cases.

#### Chain of Lakes
![chainOfLakes_subtraction](https://github.com/user-attachments/assets/cb29d8ef-d365-46ac-94bd-3f607e1fbe05)

#### Lake Nokomis
![lakeNokomis_subtraction](https://github.com/user-attachments/assets/28ec89d5-378d-4a2f-b54a-b0bf1e7ec336)

#### White Bear Lake
![whiteBearLake_subtraction](https://github.com/user-attachments/assets/8271754e-c299-4dac-bb6b-b999f425ea06)

### Attempted Buffer Zone
After noticing the sharp transition from land to water, one idea was to replace some of the null data outside the edges of the lake by setting depth=0. This did not seem to smooth out the boundary much. 

This is how the buffer zone looked: for testing purposes, I created a buffer of 50m around the lake edges so that I could visually see it worked. Interpolating across this would be the same as with a 10m buffer.
![nokomis_buffer](https://github.com/user-attachments/assets/f7de82cc-10ba-47ce-ae42-f5c310c01c5b)

It looks like the original bathymetry DEM already had a zone of 0 depth around the edge, so all the buffer did was make that zone thicker. To confirm, when I interpolated across the buffered vs the non-buffered DEM, I did not visually see any changes. Even when I took an elevation profile across the lake, the differences between methods were small. 

The line drawn across the lake shows where the profile was taken, and I highlighted in red the regions that I zoom in on. The full elevation profile also has dashed lines showing which regions I zoom in on. These regions show where the buffered and non-buffered DEMs are different from each other. When I interpolated across the buffer, I tried the bilinear vs bicubic methods of interpolation, so these are also shown in the plots.
![profileTransect](https://github.com/user-attachments/assets/1b644496-0131-476f-88bd-d751c1591da8)

![elevProfile](https://github.com/user-attachments/assets/faec3030-7018-4d27-8f8c-61d91b1daf3d)

![elevProfile80s](https://github.com/user-attachments/assets/889f50e1-1a64-4fd0-a0f4-69cfa3192529)

![elevProfile700s](https://github.com/user-attachments/assets/f9c17684-b242-4e17-9980-1a28c68901da)
