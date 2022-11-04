import numpy as np
import cv2
import os
import pprint
import configparser

def configReader(filename):
    section = 'MERGELAYERS'
    conf = configparser.ConfigParser()
    conf.read(filename)
    rgb = conf[section].get('')
    newlayers = conf[section].get('')
    filelist = conf[section].get('').split(',')
    returnDict = {
        rgb,
        newlayers,
        filelist
    }
    return returnDict


# def main(rgb,newlayers,filelist):
def main():
    
    a = np.array([[[120,220,100],[120,218,100],[110,200,150]],
                [[100,200,100],[120,150,100],[110,250,150]],
                [[80,220,100],[120,100,100],[110,100,150]]])
    b = np.array([[[120.0],[120.0],[110.0]],
                [[100.6],[80.5],[200.5]],
                [[50.5],[170.0],[180.0]]])
    pprint.pprint(np.concatenate((a,b),axis=2))
    



if __name__ == '__main__':

    main()
