import rasterio
import fiona
import os

def splitLine(line: str):
    trimmed = line.replace('\n','')
    pixlist = trimmed.split(' ')
    return {
        'x': pixlist[1],
        'y': pixlist[0],
        'val': pixlist[2]
    }

def readPixels(pixelFile:str):
    with open(pixelFile,'r') as pf:
        lines = pf.readlines()
    pixelList = list(map(lambda i: splitLine(i),lines))
    return pixelList

def transformPix(rasterpath:str,pixList:list):
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
    

def writeShapefile(geolist: list,outfilepath: str,crs:str):
    schema = {
        'geometry':'Point',
        'properties':[('Category','float')]
    }

    with fiona.open(outfilepath, mode='w',driver='ESRI Shapefile',schema=schema,crs=crs) as newshp:
        for gps in geolist:
            row = {
                'geometry':{
                    'type':'Point',
                    'coordinates':gps['coord']},
                'properties':{'Category': gps['cat']}
            }
            newshp.write(row)

def pixel_to_geo(pixel_file:str, tiff_file:str, out_folder:str, out_filename:str):
    pixlist = readPixels(pixel_file)
    crs,geolist = transformPix(tiff_file,pixlist)
    outfilepath = os.path.join(out_folder,out_filename + '.shp')
    writeShapefile(geolist,outfilepath,crs)