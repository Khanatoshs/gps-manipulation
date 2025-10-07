import os
import traceback
import logging
from typing import Iterable
import cv2
from decimal import Decimal
import rasterio
import fiona

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

def map_shape(shape):
    logging.debug("[DEBUG] --- Original shape data: " + str(shape))
    id = shape['id']
    coordinates =  shape['geometry']['coordinates']
    resdict = {
        'Fid':id,
        'coordinates':coordinates
    }
    resdict.update(shape['properties'])
    logging.debug("[DEBUG] --- Obtained object: " + str(resdict))
    return resdict

def get_row(px,py,cat,shape,index=None,cor=None,required = None,showP = True):
    auxList = []
    if showP:
        auxList.append(str(shape['Fid']))
    if index is not None:
        auxList.append(str(index))
    for k,it in shape.items():
        if showP:
            if k != 'Fid' and k != 'coordinates':
                auxList.append(str(it))
        else:
            if k == required:
                auxList.append(str(it))
    if cor is not None:
        auxList.append(str(cor[0]))
        auxList.append(str(cor[1]))
    else:
        auxList.append(str(shape['coordinates'][0]))
        auxList.append(str(shape['coordinates'][1]))
    auxList.append(str(px))
    auxList.append(str(py))
    auxList.append(cat)
    # print(auxList)
    return auxList
    

def process_shapefile(shapefile:str,cat:str,geoType:str,src_tiff,listCSV:list,req,showP):
    shapes = None
    print('--- OPENING SHAPE FILE: ' + shapefile + ' ---')
    logging.debug("[DEBUG] --- Opening shapefile: " + shapefile)
    try:
        with fiona.open(shapefile,'r') as src_shp:
            logging.debug("[DEBUG] --- shapefile INFO: " + str(src_shp.crs))
            logging.debug("[DEBUG] --- shapefile INFO: " + str(src_shp.driver))
            logging.debug("[DEBUG] --- shapefile INFO: " + str(src_shp.bounds))
            logging.debug("[DEBUG] --- shapefile INFO: " + str(src_shp.schema))
            geoType = str(src_shp.schema['geometry'])
            typeId = False
            if len(src_shp.schema['properties'].keys()) == 1 and list(src_shp.schema['properties'].keys())[0] == 'Field':
                typeId = True 
            if geoType == 'Point' or geoType == '3D Point':
                shapes = list(map(lambda i:map_shape(i),src_shp))
            else:
                shapes = list(map(lambda i: {'Fid': i['properties']['MERGE_SRC'] + '_' + str(i['properties']['id']),'coordinates': i['geometry']['coordinates'][0] if len(i['geometry']['coordinates']) <=1 else i['geometry']['coordinates']},src_shp))
    except FileNotFoundError as e:
        logging.error(e)
        print("ERROR --- FILE NOT FOUND: " + str(e))
    logging.debug("[DEBUG] --- shapes: " + str(shapes))
    print('--- FOUND ' + str(len(shapes)) + ' SHAPES OF TYPE: ' + str(geoType) + ' ---')
    for shp in shapes:
        if geoType != 'Point' and geoType != '3D Point':
            print(str(shp['coordinates']))
            for i,cor in enumerate(shp['coordinates']):
                print(cor)
                py,px = src_tiff.index(*cor)
                listCSV.append(get_row(px, py, cat, shp,i+1,cor))
        else:
            py,px = src_tiff.index(*shp['coordinates'])
            listCSV.append(get_row(px, py, cat, shp,required=req,showP=showP))
    logging.debug("[DEBUG] --- list for CSV: " + str(listCSV))
    return geoType


def writeCSV(outfile:str,delim:str,listCSV:list,headers:Iterable):
    print('--- WRITING TO FILE: ' + outfile  + ' ---')
    with CustomCSV(outfile,'w') as outf: 
        outf.writeHeader(delim,headers)
        for line in listCSV:
            outf.writeLineCSV(delim,line)
    print('--- FINISHED WRITING FILE ---')

def get_headers(shapefile:str,geoType:str,showP:bool,requiredCol):
    headers = []
    if showP:
        if geoType == 'Point' or geoType == '3D Point':
            headers = ['Fid']
        else:
            headers = ['polyId','pointId']
        with fiona.open(shapefile) as shpfile:
            logging.debug("[DEBUG] --- Extra properties: " + str(shpfile.schema['properties'].keys()))
            for k in shpfile.schema['properties'].keys():
                headers.append(k)
    else:
        headers = [requiredCol]
    headers.extend(['geox','geoy','px','py','category'])
    return headers
            


# Create image with red dots at the coordinates
def create_image_with_dots(coordinates, tiff):
    image = cv2.imread(tiff,cv2.IMREAD_UNCHANGED)
    for line in coordinates:
        cv2.circle(image, (int(line[-3]),int(line[-2])), radius=20, color=(0, 0, 255), thickness=-1)  # Red color in BGR

    return image

def view_image(im):
    # Display the image
    cv2.imshow("Image with Red Dots", im)
    cv2.waitKey(0)  # Wait for a key press
    cv2.destroyAllWindows()

    # Optionally, save the image to a file
def save_image(im,save_path):
    save_path = save_path + '_red_dots.png'
    cv2.imwrite(save_path, im)



def geo_to_pixel(out_folder:str,out_file:str,shapes:list,tiff_path:str,categories:list,same_category:bool = True,
                 delimiter:str = ',',order_by:str = '',save_preview:bool = True, show_properties:bool = True, loglevel:str = 'INFO'):

    logLevel = loglevel.upper()
    logging.basicConfig(filename="GeoLog.log",level=logLevel)
    fiona.log.setLevel('INFO')
    rasterio.log.setLevel('INFO')

    if not os.path.isdir(out_folder):
        os.mkdir(out_folder)

    outfile = os.path.join(out_folder, out_file +'.csv')
    delim = delimiter
    shapefiles = shapes
    if len(shapefiles) == 1 and os.path.isdir(shapefiles[0]):
        shapedir = shapefiles[0]
        shapefiles = []
        for r, d, f in os.walk(shapedir):
            for file in f:
                if '.shp' in file and '.xml' not in file:
                    shapefiles.append(os.path.join(r, file))
    cats = categories
    same_category = same_category
    tiff = tiff_path
    orderby = order_by
    showP = show_properties
    geoType = ''

    try:
        with rasterio.open(tiff) as rasterTiff:
            logging.debug("[DEBUG] --- Raster info : " + str(rasterTiff.crs))
            logging.debug("[DEBUG] --- Raster info: " + str(rasterTiff.bounds))
            listCSV = []
            geoType = ''
            for i,shp in enumerate(shapefiles):
                if same_category:
                    cat = cats[0]
                else:
                    cat = cats[i]
                geoType = process_shapefile(shp,cat,geoType,rasterTiff,listCSV,orderby,showP)
            headers = get_headers(shapefiles[0], geoType,showP,orderby)
            logging.debug("[DEBUG] --- Headers of CSV file: " + str(headers))
            try:
                orderIndex = headers.index(orderby)
                logging.debug("[DEBUG] --- Found propertie to order by at index: " + str(orderIndex))
            except ValueError as e:
                logging.error(e)
                print("--- COULD NOT FIND ORDERBY VALUE ---")
                print(e)
                print("--- ORDERING BY FIRST ELEMENT")
            finally:
                logging.debug("[DEBUG] --- Using orderIndex = 0")
                orderIndex = 0
            listCSV.sort(key=lambda elem: int(elem[orderIndex]))
            writeCSV(outfile,delim,listCSV,headers)
    except FileNotFoundError as e:
        logging.error(e)
        print("ERROR --- FILE NOT FOUND: " + str(e))

    
    im = create_image_with_dots(listCSV,tiff)
    
    if save_preview:
        save_image(im,os.path.join(out_folder, out_file))