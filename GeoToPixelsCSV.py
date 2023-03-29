from genericpath import isfile
import os
import traceback
from typing import Iterable
import rasterio
import rasterio.windows
import rasterio.mask
import rasterio.plot
import fiona
import configparser


def makeConf():
    strConf = '[GEOTOPIXEL]+\n'
    strConf += 'tiff=\n'
    strConf += 'shapes=\n'
    strConf += 'categories=\n'
    strConf += 'outfolder=\n'
    strConf += 'outfilename=\n'
    strConf += 'delimiter=,\n'
    with open('config.ini','w') as confF:
        confF.write(strConf)

def read_config(filename) -> dict:
    conf = configparser.ConfigParser()
    conf.read(filename)
    section = 'GEOTOPIXEL'
    tiff = conf[section].get('tiff')
    shapes = conf[section].get('shapes').split(',')
    categories = conf[section].get('categories').split(',')
    outfolder = conf[section].get('outfolder')
    outfilename = conf[section].get('outfilename')
    delimiter = conf[section].get('delimiter')
    ret_dict = {
        'tiff':tiff,
        'shapes':shapes,
        'categories':categories,
        'outfolder':outfolder,
        'outfilename': outfilename,
        'delimiter': delimiter
    }
    return ret_dict

class CustomCSV:
    def __init__(self,filename:str,mode:str) -> None:
        self.csvFile = open(filename,mode)

    def __enter__(self):
        return self
    
    def __exit__(self,exc_type, exc_value, tb):
        if exc_type is not None:
            traceback.print_exception(exc_type, exc_value, tb)
        self.csvFile.close()

    def writeHeader(self,delimiter:str,columns:Iterable) -> None:
        colStr = ''
        for col in columns:
            colStr += col + delimiter
        colStr = colStr[:-1] + '\n'
        self.csvFile.write(colStr)
    
    def writeLineCSV(self,delimiter:str,data:Iterable) -> None:
        dataStr = ''
        for dat in data:
            dataStr += str(dat) + delimiter
        dataStr = dataStr[:-1] + '\n'
        self.csvFile.write(dataStr)

def process_shapefile(shapefile:str,cat:str,geoType:str,src_tiff,listCSV:list):
    shapes = None
    print('--- OPENING SHAPE FILE: ' + shapefile + ' ---')
    with fiona.open(shapefile,'r') as src_shp:
        geoType = str(src_shp.schema['geometry'])
        typeId = False
        if len(src_shp.schema['properties'].keys()) == 1 and list(src_shp.schema['properties'].keys())[0] == 'Field':
            typeId = True 
        if geoType == 'Point':
            if typeId:
                shapes = list(map(lambda i: {'id': i['properties']['Field'],'coordinates': i['geometry']['coordinates']},src_shp))    
            else:
                shapes = list(map(lambda i: {'id': i['id'],'coordinates': i['geometry']['coordinates']},src_shp))
        else:
            shapes = list(map(lambda i: {'id': i['properties']['MERGE_SRC'] + '_' + str(i['properties']['id']),'coordinates': i['geometry']['coordinates'][0] if len(i['geometry']['coordinates']) <=1 else i['geometry']['coordinates']},src_shp))

    print('--- FOUND ' + str(len(shapes)) + ' SHAPES OF TYPE: ' + str(geoType) + ' ---')
    for shp in shapes:
        if geoType != 'Point':
            for i,cor in enumerate(shp['coordinates']):
                px,py = src_tiff.index(*cor)
                listCSV.append((str(shp['id']),str(i+1),str(cor[0]),str(cor[1]),str(px),str(py),cat))
        else:
            px,py = src_tiff.index(*shp['coordinates'])
            listCSV.append((str(shp['id']),str(shp['coordinates'][0]),str(shp['coordinates'][1]),str(px),str(py),cat))
    return geoType


def writeCSV(outfile:str,delim:str,listCSV:list,headers:Iterable):
    print('--- WRITING TO FILE: ' + outfile  + ' ---')
    with CustomCSV(outfile,'w') as outf: 
        outf.writeHeader(delim,headers)
        for line in listCSV:
            outf.writeLineCSV(delim,line)
    print('--- FINISHED WRITING FILE ---')


def main():
    if not os.path.exists('config.ini'):
        print('THE FILE config.ini WAS CREATED, PLEASE INPUT INITIAL DATA IN FILE')
        makeConf()

    conf = read_config('config.ini')

    if not os.path.isdir(conf.get('outfolder')):
        os.mkdir(conf.get('outfolder'))

    outfile = os.path.join(conf.get('outfolder'), conf.get('outfilename') +'.csv')
    delim = conf.get('delimiter')
    shapefiles = conf.get('shapes')
    categories = conf.get('categories')
    tiff = conf.get('tiff')
    # shapes = None
    geoType = ''

    with rasterio.open(tiff) as rasterTiff:
        listCSV = []
        geoType = ''
        for i,shp in enumerate(shapefiles):
            geoType = process_shapefile(shp,categories[i],geoType,rasterTiff,listCSV)
        if geoType == 'Point':
            headers = ('id','geoX','geoY','pX','pY','category')
        else:
            headers = ('polyId','pointId','geoX','geoY','pX','pY','category')
        listCSV.sort(key=lambda elem: int(elem[0]))
        writeCSV(outfile,delim,listCSV,headers)

    

    # print('--- OPENING SHAPE FILE: ' + conf.get('shape') + ' ---')
    # with fiona.open(conf.get('shape'),'r') as src_shp:
    #     geoType = str(src_shp.schema['geometry'])
    #     typeId = False
    #     if len(src_shp.schema['properties'].keys()) == 1 and list(src_shp.schema['properties'].keys())[0] == 'Field':
    #         typeId = True 
    #     if geoType == 'Point':
    #         if typeId:
    #             shapes = list(map(lambda i: {'id': i['properties']['Field'],'coordinates': i['geometry']['coordinates']},src_shp))    
    #         else:
    #             shapes = list(map(lambda i: {'id': i['id'],'coordinates': i['geometry']['coordinates']},src_shp))
    #     else:
    #         shapes = list(map(lambda i: {'id': i['properties']['MERGE_SRC'] + '_' + str(i['properties']['id']),'coordinates': i['geometry']['coordinates'][0] if len(i['geometry']['coordinates']) <=1 else i['geometry']['coordinates']},src_shp))

    # print('--- FOUND ' + str(len(shapes)) + ' SHAPES OF TYPE: ' + str(geoType) + ' ---')
    # print('--- OPENING TIFF FILE: ' + conf.get('tiff') + ' ---')
    # with rasterio.open(conf.get('tiff')) as src_tiff:
    #     print('--- WRITING TO FILE: ' + outfile  + ' ---')
    #     with CustomCSV(outfile,'w') as outf: 
    #         if geoType == 'Point':
    #             outf.writeHeader(delim,('id','geoX','geoY','pX','pY'))
    #             # writeHeader(outf,delim,('id','coordx','coordy','px','py'))
    #         else:
    #             outf.writeHeader(delim,('polyId','pointId','geoX','geoY','pX','pY'))
    #             # writeHeader(outf,delim,('polyId','pointId','coordy','geoCoords','pixCoords'))
    #         for shp in shapes:
    #             if geoType != 'Point':
    #                 for i,cor in enumerate(shp['coordinates']):
    #                     px,py = src_tiff.index(*cor)
    #                     outf.writeLineCSV(delim,(str(shp['id']),str(i+1),str(cor[0]),str(cor[1]),str(px),str(py)))
    #                     # outf.write(str(shp['id']) + ';'  + str(i+1) + ';' + str(cor) + ';' + str((px,py)) + '\n')
    #             else:
    #                 px,py = src_tiff.index(*shp['coordinates'])
    #                 outf.writeLineCSV(delim,(str(shp['id']),str(shp['coordinates'][0]),str(shp['coordinates'][1]),str(px),str(py)))
    #                 # outf.write(str(shp['id']) + ',' + str(shp['coordinates'][0]) + ',' + str(shp['coordinates'][1]) + ',' + str(px) + ',' + str(py) + '\n')
    #     print('--- FINISHED WRITING FILE ---')

if __name__ == '__main__':
    main()