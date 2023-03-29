import numpy as np
import cv2
import os
import pprint
import configparser

def configReader(filename):
    section = 'MERGELAYERS'
    conf = configparser.ConfigParser()
    conf.read(filename)
    rgb = conf[section].get('rgb')
    newlayers = conf[section].get('newlayers')
    filelist = conf[section].get('filelist').split(',')
    returnDict = {
        'rgb':rgb,
        'newlayers':newlayers,
        'filelist':filelist
    }
    return returnDict


def main(rgb,filelist):
# def main():
    
    # imrgb = cv2.imread(rgb,cv2.IMREAD_UNCHANGED)
    # print(imrgb.shape)
    # newfil = filelist[0]
    # newimg = cv2.imread(newfil,cv2.IMREAD_UNCHANGED)
    # immerge = np.concatenate((imrgb,newimg),axis=len(imrgb.shape) - 1 )
    

    # cv2.imwrite("testMerge.tif",immerge)
    # for file in filelist:
    #     imnew = cv2.imread(file,cv2.IMREAD_UNCHANGED)
    #     immerge = np.concatenate((imrgb,imnew),axis=2)
    #     imrgb = immerge
    # a = np.array([[[120,220,100],[120,218,100],[110,200,150]],
    #             [[100,200,100],[120,150,100],[110,250,150]],
    #             [[80,220,100],[120,100,100],[110,100,150]]])
    # a = np.array([[[121.0],[110.0],[170.0]],
    #             [[110.6],[84.5],[210.5]],
    #             [[510.5],[120.0],[182.0]]])
    # b = np.array([[[120.0],[120.0],[110.0]],
    #             [[100.6],[80.5],[200.5]],
    #             [[50.5],[170.0],[180.0]]])
    a =np.matrix(
        [[1,33,44,55],
        [10,22,55,60],
        [100,330,440,550]]
        )
    b = np.matrix(
        [[22.5,26.33,88,100.66],
        [10.22,22.36,55.99,685],
        [100.4,330.9,440.6,550.3]]
        )
    # print(a.shape)
    # print(b.shape)
    anew = a[:,:,np.newaxis]
    bnew = b[:,:,np.newaxis]
    # print(anew.shape)
    pprint.pprint(print(b))
    lastmerge = np.concatenate((anew,b),axis=2)
    # lastmerge = np.column_stack((anew,b))
    print(lastmerge)
    # pprint.pprint(np.append(a,b,axis=1))
        # print(imrgb.shape)

if __name__ == '__main__':
    conf = configReader('config.ini')
    main(conf['rgb'],conf['filelist'])
    # main(None,None,None)
