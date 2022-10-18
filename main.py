from genericpath import isdir
import os
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
    outfolder = conf[section].get('outfolder')
    ret_dict = {
        'tiff':tiff,
        'shape':shape,
        'outfolder':outfolder
    }
    return ret_dict




conf = read_config('config.ini')

if not os.path.isdir(conf.get('outfolder')):
    os.mkdir(conf.get('outfolder'))

outfile = os.path.join(conf.get('outfolder'),'test_tiff.tif')

shapes = None
shp_geometry = None
with fiona.open(conf.get('shape'),'r') as src_shp:
    shapes = list(map(lambda i: {'id': i['id'],'coordinates': i['geometry']['coordinates']},src_shp))
    # shp_geometry = [feature['geometry'] for feature in src_shp]

src_tiff = rasterio.open(conf.get('tiff'))
print(shapes[0]['coordinates'])
px,py = src_tiff.index(*shapes[0]['coordinates'])
patch_size = 100
print(px,py)

window = rasterio.windows.Window(px-patch_size//2,py - patch_size//2,patch_size,patch_size)
print(window)
clip = src_tiff.read(window=window)
meta = src_tiff.meta
meta['width'],meta['height'] = patch_size,patch_size
meta['transform'] = rasterio.windows.transform(window,src_tiff.transform)

with rasterio.open(outfile,'w',**meta) as dst:
    dst.write(clip)

#TODO: check why the result image is blank

# out_image, out_transform = rasterio.mask.mask(src_tiff, shp_geometry,crop=True)
# out_meta = src_tiff.meta