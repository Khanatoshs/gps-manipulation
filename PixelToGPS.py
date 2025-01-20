import configparser
import rasterio
import fiona
import os

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
        'pixelfile':pixelfile,
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

def transformPix(rasterpath,pixList:list):
    geolist = []
    crs = None
    with rasterio.open(rasterpath) as raster:
        crs = str(raster.crs)
        for pix in pixList:
            geo = raster.xy(pix['y'],pix['x'])
            geolist.append({
                'coord':geo['coords'],
                'cat':pix['val']
                })
    return crs,geolist
    

def writeShapefile(geolist,outfilepath,crs):
    schema = {
        'geometry':'Point',
        'properties':[('Category','Double')]
    }

    with fiona.open(outfilepath, mode='w',driver='ESRI Shapefile',schema=schema,crs=crs) as newshp:
        for gps in geolist:
            row = {
                'geometry':{
                    'type':'Point',
                    'coordinates':gps},
                'properties':{'Category': gps['cat']}
            }
            newshp.write(row)

def main():
    conf = read_config('config.ini')
    pixlist = readPixels(conf['pixelfile'])
    crs,geolist = transformPix(conf['tiff'],pixlist)
    outfilepath = os.path.join(conf['outfolder'],conf['outfile'])
    writeShapefile(geolist,outfilepath,crs)


if __name__ == '__main__':
    main()


