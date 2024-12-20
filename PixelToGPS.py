import configparser
import rasterio
import cv2
import fiona


def read_config(filename) -> dict:
    conf = configparser.ConfigParser()
    conf.read(filename)
    section = 'PIXELTOGPS'
    pixelfile = conf[section].get('pixelfile')
    tiff = conf[section].get('tiff')
    outfolder = conf[section].get('outfolder')
    outfilename = conf[section].get('outfilename')
    ret_dict = {
        'tiff':tiff,
        'pixelFile':yoloFile,
        'outfolder':outfolder,
        'outfilename': outfilename
    }
    return ret_dict

def splitLine(line: str):
    trimmed = line.replace('\n','')
    pixlist = trimmed.split(' ')
    return {
        'x': pixlist[1],
        'y': pixlist[0],
        'val': pixlist[2]
    }

def readPixels(pixelFile):
    with open(pixelFile,'r') as pf:
        lines = pf.readlines()
    pixelList = list(map(lambda i: splitLine(i),lines))
    return pixelList

def transformPix():
    return

def main():
    return

if __name__ == '__main__':
    main()


