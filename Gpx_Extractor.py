import xml.etree.ElementTree as ET
import os

gpxFile = '/home/leonardo/Leo/Projects/GPS_Manipulation/Data/Vlad/Waypoints_2025-01-31.gpx'

tree  = ET.parse(source=gpxFile)
root = tree.getroot()
print(root.attrib)
for child in root:
    print(child.tag,child.attrib)
    for gc in child:
        tag = str(gc.tag).replace()