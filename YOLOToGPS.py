import os
from decimal import Decimal
import rasterio
import configparser
import fiona
import pprint

def read_config(filename) -> dict:
    conf = configparser.ConfigParser()
    conf.read(filename)
    section = 'YOLOTOGPS'
    yoloFile = conf[section].get('yolofile')
    tiff = conf[section].get('tiff')
    outfolder = conf[section].get('outfolder')
    outfilename = conf[section].get('outfilename')
    ret_dict = {
        'tiff':tiff,
        'yoloFile':yoloFile,
        'outfolder':outfolder,
        'outfilename': outfilename
    }
    return ret_dict

def yolo_to_pixel(yolcoord:dict,imwidth,imheight):
# cat xc yc width height
    pxc = yolcoord['x'] * imwidth
    pyc = yolcoord['y'] * imheight
    pw = yolcoord['width'] * imwidth
    ph = yolcoord['height'] * imheight
    pxf = pxc + (pw//2)
    pyf = pyc + (ph//2)
    px0 = pxc - (pw//2)
    py0 = pyc - (ph//2)
    return {
        'x': px0,
        'y':py0,
        'xf': pxf,
        'yf': pyf,
        'xc': pxc,
        'yc': pyc,
        'width': pw,
        'height': ph,
        'cat': yolcoord['cat']
    }

def split_yolo_line(yolLine:str):
    yoltrim = yolLine.replace('\n', '')
    yolsplit = yoltrim.split(' ')
    return {
        'cat': int(yolsplit[0]),
        'x': Decimal(yolsplit[1]),
        'y': Decimal(yolsplit[2]),
        'width': Decimal(yolsplit[3]),
        'height': Decimal(yolsplit[4])
    }

def read_yolo_file(filename:str):
    with open(filename,'r') as yolf:
        lines = yolf.readlines()
    
    yolList = (list(map(lambda i: split_yolo_line(i),lines)))
    return yolList
def main():
    conf = read_config('config.ini')
    yoloList = read_yolo_file(conf['yoloFile'])
    tiffh = None
    tiffw = None
    crs = None
    with rasterio.open(conf['tiff']) as rastiff:
        crs = str(rastiff.crs)
        tiffh = rastiff.shape[0]
        tiffw = rastiff.shape[1]
        pixlist = list(map(lambda i: yolo_to_pixel(i, tiffw, tiffh), yoloList))
        gpslist = list(map(lambda i:{'lat0':rastiff.xy(int(i['y']),int(i['x']))[0],'lon0':rastiff.xy(int(i['y']),int(i['x']))[1],'latf':rastiff.xy(int(i['yf']),int(i['xf']),)[0],'lonf':rastiff.xy(int(i['yf']),int(i['xf']))[1],'latc':rastiff.xy(int(i['yc']),int(i['xc']))[0],'lonc':rastiff.xy(int(i['yc']),int(i['xc']))[1],'cat':i['cat']},pixlist))
        
    schema = {
        'geometry':'Point',
        'properties':[('Category','str')]
    }

    outfile = os.path.join(conf.get('outfolder'), conf.get('outfilename') +'.shp')

    with fiona.open(outfile, mode='w',driver='ESRI Shapefile',schema=schema,crs=crs) as newshp:
        for gps in gpslist:
            row = {
                'geometry':{
                    'type':'Point',
                    'coordinates':(gps['latc'],gps['lonc'])},
                'properties':{'Category': gps['cat']}
            }
            newshp.write(row)

if __name__ == '__main__':
    main()


