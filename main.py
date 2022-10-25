from genericpath import isdir
import os
os.environ["OPENCV_IO_MAX_IMAGE_PIXELS"] = pow(2,40).__str__()
import cv2

import rasterio
import rasterio.windows
import rasterio.mask
import rasterio.plot
import fiona
import configparser
from matplotlib import pyplot



def read_config(filename) -> dict:
    conf = configparser.ConfigParser()
    conf.read(filename)
    section = 'SOURCES'
    tiff = conf[section].get('tiff')
    shape = conf[section].get('shape')
    outfolder = conf[section].get('outfolder')
    outfilename = conf[section].get('outfilename')
    outfiletype = conf[section].get('outfiletype')
    ret_dict = {
        'tiff':tiff,
        'shape':shape,
        'outfolder':outfolder,
        'outfilename': outfilename,
        'outfiletype': outfiletype
    }
    return ret_dict




conf = read_config('config.ini')

if not os.path.isdir(conf.get('outfolder')):
    os.mkdir(conf.get('outfolder'))

outfile = os.path.join(conf.get('outfolder'),'coordinates.csv')

shapes = None
shp_geometry = None
with fiona.open(conf.get('shape'),'r') as src_shp:
    print(src_shp.schema)
    shapes = list(map(lambda i: {'id': i['id'],'coordinates': i['geometry']['coordinates']},src_shp))
    # shp_geometry = [feature['geometry'] for feature in src_shp]
with rasterio.open(conf.get('tiff')) as src_tiff:
    with open(outfile,'w') as outf: 
        outf.write('id,coordx,coordy,px,py\n')
        # print(shapes[0]['coordinates'])
        for shp in shapes:
            px,py = src_tiff.index(*shp['coordinates'])
            outf.write(str(shp['id']) + ',' + str(shp['coordinates'][0]) + ',' + str(shp['coordinates'][1]) + ',' + str(px) + ',' + str(py) + '\n')

