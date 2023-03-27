from decimal import Decimal
import rasterio
import configparser

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
# cat x y width height
    px = yolcoord['x'] * imwidth
    py = yolcoord['y'] * imheight
    pw = yolcoord['width'] * imwidth
    ph = yolcoord['height'] * imheight
    return {
        'x': px,
        'y':py,
        'xf': px + pw,
        'yf': py + ph,
        'width': pw,
        'height': ph
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

conf = read_config('config.ini')
yoloList = read_yolo_file(conf['yoloFile'])
tiffh = None
tiffw = None
with rasterio.open(conf['tiff']) as rastiff:
    tiffh = rastiff.shape[0]
    tiffw = rastiff.shape[1]
    pixlist = list(map(lambda i: yolo_to_pixel(i, tiffw, tiffh), yoloList))
    gpslist = list(map(lambda i:{'x0':rastiff.xy(int(i['x']),int(i['y']))[0],'y0':rastiff.xy(int(i['x']),int(i['y']))[1],'xf':rastiff.xy(int(i['xf']),int(i['yf']))[0],'yf':rastiff.xy(int(i['xf']),int(i['yf']))[1]},pixlist))

print(yoloList[0])
print(gpslist[0])
print(pixlist[0])



