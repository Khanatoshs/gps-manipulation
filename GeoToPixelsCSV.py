import os
import traceback
from typing import Iterable
import rasterio
import rasterio.windows
import rasterio.mask
import rasterio.plot
import fiona
import configparser



def read_config(filename) -> dict:
    conf = configparser.ConfigParser()
    conf.read(filename)
    section = 'GEOTOPIXEL'
    tiff = conf[section].get('tiff')
    shape = conf[section].get('shape')
    outfolder = conf[section].get('outfolder')
    outfilename = conf[section].get('outfilename')
    delimiter = conf[section].get('delimiter')
    ret_dict = {
        'tiff':tiff,
        'shape':shape,
        'outfolder':outfolder,
        'outfilename': outfilename,
        'delimiter': delimiter
    }
    return ret_dict

# def writeHeader(file:TextIOWrapper,delimiter:str,columns:Iterable):
#     colStr = ''
#     for col in columns:
#         colStr += col + delimiter
#     colStr = colStr[-1] + '\n'
#     file.write(colStr)

# def writeCSVLine(file: TextIOWrapper,delimiter:str,data:Iterable):
#     dataStr = ''
#     for dat in data:
#         dataStr += str(dat) + delimiter
#     dataStr = dataStr[-1] + '\n'
#     file.write(dataStr)

class CustomCSV:
    def __init__(self,filename:str,mode:str) -> None:
        self.csvFile = open(filename,mode)

    def __enter__(self):
        return self
    
    def __exit__(self,exc_type, exc_value, tb):
        if exc_type is not None:
            traceback.print_exception(exc_type, exc_value, tb)
        self.csvFile.close()
#TODO: check why it doesn't print data
    def writeHeader(self,delimiter:str,columns:Iterable) -> None:
        colStr = ''
        for col in columns:
            colStr += col + delimiter
        colStr = colStr[-1] + '\n'
        self.csvFile.write(colStr)
    
    def writeLineCSV(self,delimiter:str,data:Iterable) -> None:
        dataStr = ''
        for dat in data:
            dataStr += str(dat) + delimiter
        dataStr = dataStr[-1] + '\n'
        self.csvFile.write(dataStr)




conf = read_config('config.ini')

if not os.path.isdir(conf.get('outfolder')):
    os.mkdir(conf.get('outfolder'))

outfile = os.path.join(conf.get('outfolder'), conf.get('outfilename') +'.csv')
delim = conf.get('delimiter')
shapes = None
shp_geometry = None
geoType = ''
with fiona.open(conf.get('shape'),'r') as src_shp:
    print(src_shp.schema)
    # geoType = str(src_shp.schema['geometry'])
    if geoType == 'Point': 
        shapes = list(map(lambda i: {'id': i['id'],'coordinates': i['geometry']['coordinates']},src_shp))
    else:
        shapes = list(map(lambda i: {'id': i['properties']['MERGE_SRC'] + '_' + str(i['properties']['id']),'coordinates': i['geometry']['coordinates'][0] if len(i['geometry']['coordinates']) <=1 else i['geometry']['coordinates']},src_shp))


with rasterio.open(conf.get('tiff')) as src_tiff:
    with CustomCSV(outfile,'w') as outf: 
        if geoType == 'Point':
            outf.writeHeader(delim,('id','geoX','geoY','pX','pY'))
            # writeHeader(outf,delim,('id','coordx','coordy','px','py'))
        else:
            outf.writeHeader(delim,('polyId','pointId','geoX','geoY','pX','pY'))
            # writeHeader(outf,delim,('polyId','pointId','coordy','geoCoords','pixCoords'))
        for shp in shapes:
            if geoType != 'Point':
                for i,cor in enumerate(shp['coordinates']):
                    px,py = src_tiff.index(*cor)
                    outf.writeLineCSV(delim,(str(shp['id']),str(i+1),str(cor[0]),str(cor[1]),str(px),str(py)))
                    # outf.write(str(shp['id']) + ';'  + str(i+1) + ';' + str(cor) + ';' + str((px,py)) + '\n')
            else:
                px,py = src_tiff.index(*shp['coordinates'])
                outf.writeLineCSV(delim,str(shp['id']),str(shp['coordinates'][0]),str(shp['coordinates'][1]),str(px),str(py))
                # outf.write(str(shp['id']) + ',' + str(shp['coordinates'][0]) + ',' + str(shp['coordinates'][1]) + ',' + str(px) + ',' + str(py) + '\n')
            

