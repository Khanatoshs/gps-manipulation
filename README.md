# gps-manipulation
Python program to manipulate gps data and extract necessary data for research

# GEO To Pixel Script

The script works by inputing a SHP file and a Georeferenced .tif Image.  The inputs must be included in the config file, a sample is provided here.
Currently it only outputs a CSV file.

## Instructions:

Create a config.ini file
Copy de data from config_sample.ini
Fill the fields with custom data
The config file only needs to be filled in the section [GEOTOPIXEL]

### Instructions on how to fill config section:
```
tiff = (path to your .tif file)
shapes = (path to your .shp files, can be multiple)
categories = (categories you wish to assign to each shapefile, they must be in the same order as the shape files)
outfoldername = (path to the folder where you want the results)
outfilename = (name of the file wth the results no file extension is needed)
orderby = (Name of the field you wih to sort the list with)
delimiter = (the type of delimiter you want to use for the csv the default should be , )
```
