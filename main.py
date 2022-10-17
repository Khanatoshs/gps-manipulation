import rasterio
import rasterio.windows
import rasterio.mask
import rasterio.plot
import fiona
import configparser
import matplotlib as plt

def read_config(filename) -> dict:
    conf = configparser.ConfigParser()
    conf.read(filename)
    section = 'SOURCES'
    tiff = conf[section].get('tiff')
    shape = conf[section].get('shape')
    ret_dict = {
        'tiff':tiff,
        'shape':shape
    }
    return ret_dict


conf = read_config('config.ini')
shapes = None
shp_geometry = None
with fiona.open(conf.get('shape'),'r') as src_shp:
    shapes = list(map(lambda i: {'id': i['id'],'coordinates': i['geometry']['coordinates']},src_shp))
    shp_geometry = [feature['geometry'] for feature in src_shp]

src_tiff = rasterio.open(conf.get('tiff'))
print(shapes[0]['coordinates'])
px,py = src_tiff.index(*shapes[0]['coordinates'])
print(px,py)
#TODO: Finish trying to get square. Just need to add the bounds and aply the window function below
# rasterio.windows.Window()
# out_image, out_transform = rasterio.mask.mask(src_tiff, shp_geometry,crop=True)
# out_meta = src_tiff.meta