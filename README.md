# lakeSubtractedDEM
Subtracting lake depths from the Minnesota DEM using GRASS GIS and Python.

### Data sources
The lake depth data can be found from MN Geospatial Commons: https://gisdata.mn.gov/dataset/water-lake-bathymetry. The units of lake depth are in negative feet.

### Python program
#### stitchDEMs_lakeBathymetry.py
The program resamples and interpolates the lake depth data from a 5-m resolution to a 1-m resolution. It then adds the (negative) depth to the LiDAR and outputs this file. There is an option to output some of the intermediate files as well, if you want to test the program on a small region first.

#### viewInterpolation_lakeBathymetry.py
If you chose to output the intermediate files earlier, this program plots them. It plots lake depth, the surface LiDAR, and the lake-subtracted LiDAR side-by-side.  

### Outputs
#### Chain of Lakes
![chainOfLakes_subtraction](https://github.com/user-attachments/assets/cb29d8ef-d365-46ac-94bd-3f607e1fbe05)

#### Lake Nokomis
![lakeNokomis_subtraction](https://github.com/user-attachments/assets/28ec89d5-378d-4a2f-b54a-b0bf1e7ec336)

#### White Bear Lake
![whiteBearLake_subtraction](https://github.com/user-attachments/assets/8271754e-c299-4dac-bb6b-b999f425ea06)
