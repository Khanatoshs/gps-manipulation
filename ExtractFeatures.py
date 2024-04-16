import configparser
import fiona
import rasterio
import numpy as np
import cv2
import os
from rasterio import features

from rasterio.plot import reshape_as_image
import rasterio.mask
from rasterio.features import rasterize

import pandas as pd
import geopandas as gpd
from shapely.geometry import mapping, Point, Polygon
from shapely.ops import unary_union

import numpy as np
import cv2
import matplotlib.pyplot as plt

os.environ["OPENCV_IO_MAX_IMAGE_PIXELS"] = pow(2,40).__str__()

def read_config(filename) -> dict:
    conf = configparser.ConfigParser()
    conf.read(filename)
    section = 'EXTRACTFEATURES'
    tiff = conf[section].get('tiff')
    shapes = conf[section].get('shapes').split(',')
    categories = conf[section].get('categories').split(',')
    outfolder = conf[section].get('outfolder')
    logLevel = conf[section].get('logLevel')
    ret_dict = {
        'tiff':tiff,
        'shapes':shapes,
        'categories':categories,
        'outfolder':outfolder,
        'logLevel': logLevel,
    }
    return ret_dict


def process_shapefile(shapefile):
    with fiona.open(shapefile,'r') as src_shp:
        geoType = str(src_shp.schema['geometry'])
        typeId = False
        if geoType == 'Polygon':
            shapes = list(map(lambda i: {'Class':  'Class_'+ i['properties']['Class'],'coordinates': i['geometry']['coordinates'][0] if len(i['geometry']['coordinates']) <=1 else i['geometry']['coordinates']},src_shp))
    return shapes

def transform(shapeclass,raster):
    listCoords = []
    for coords in shapeclass:
        for coord in shape['coordinates'][0][0]:
            py,px = raster.index(*coord)
            shape['poly'].append([px,py])


def createmask(shapelist,ortho,resfolder,raster):
    for shape in shapelist:
        mask = np.zeros((ortho.shape),np.uint8)
        for polysgroup in shape['coordinates']:
            for polys in polysgroup:
                polycoord = []
                for coords in polys:
                    py,px = raster.index(*coords)
                    polycoord.append([px,py])
                cv2.fillPoly(mask,[np.array(polycoord,dtype=np.int32)],(255,255,255))
        cv2.imwrite(os.path.join(resfolder,str(shape['Class'])+ '_mask.png') , mask)

def readgraysacle(img_src):
    ortho = cv2.imread(img_src,cv2.IMREAD_UNCHANGED)
    img_gray = cv2.cvtColor(ortho, cv2.COLOR_BGRA2GRAY)
    return img_gray

def main():
    confdict = read_config('config.ini')
    shpfiles = confdict['shapes']
    shplist = []
    # i = 1
    #for shp in shpfiles:
    #    generate_mask(confdict['tiff'],shp,confdict['outfolder'],'resmask' + str(i) + '.png')
    #    i += 1
    for shp in shpfiles:
        shplist.extend(process_shapefile(shp))

    img = readgraysacle(confdict['tiff'])
    with rasterio.open(confdict['tiff']) as raster:
        createmask(shapelist=shplist,ortho=img,resfolder=confdict['outfolder'],raster=raster)

    
#Possible function using rasterio only. Needs to be fixed
def generate_mask(raster_path, shape_path, output_path, file_name):
    
    """Function that generates a binary mask from a vector file (shp or geojson)
    
    raster_path = path to the .tif;

    shape_path = path to the shapefile or GeoJson.

    output_path = Path to save the binary mask.

    file_name = Name of the file.
    
    """
    
    #load raster
    
    with rasterio.open(raster_path, "r") as src:
        raster_img = src.read()
        raster_meta = src.meta
    
    #load o shapefile ou GeoJson
    train_df = gpd.read_file(shape_path)
    
    #Verify crs
    if train_df.crs != src.crs:
        print(" Raster crs : {}, Vector crs : {}.\n Convert vector and raster to the same CRS.".format(src.crs,train_df.crs))
        
        
    #Function that generates the mask
    def poly_from_utm(polygon, transform):
        poly_pts = []

        poly = unary_union(polygon)
        for i in np.array(poly.exterior.coords):

            poly_pts.append(~transform * tuple(i))

        new_poly = Polygon(poly_pts)
        return new_poly
    
    
    poly_shp = []
    im_size = (src.meta['height'], src.meta['width'])
    for num, row in train_df.iterrows():
        if row['geometry'].geom_type == 'Polygon':
            poly = poly_from_utm(row['geometry'], src.meta['transform'])
            poly_shp.append(poly)
        else:
            for p in row['geometry']:
                poly = poly_from_utm(p, src.meta['transform'])
                poly_shp.append(poly)

    mask = rasterize(shapes=poly_shp,
                     out_shape=im_size)
    
    #Salve
    mask = mask.astype("uint16")
    
    bin_mask_meta = src.meta.copy()
    bin_mask_meta.update({'count': 1})
    os.chdir(output_path)
    with rasterio.open(file_name, 'w', **bin_mask_meta) as dst:
        dst.write(mask * 255, 1)




if __name__ == '__main__':
    main()