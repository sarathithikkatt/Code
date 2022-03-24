from sre_constants import SUCCESS
import cv2 
import cv2.aruco as aruco
import numpy as np
import os
from math import atan2, cos, sin, sqrt, pi

def findArucoMarkers(img, markerSize=4, totalmarkers=250, draw=True):
    imGray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    key=getattr(aruco,f'DICT_{markerSize}X{markerSize}_{totalmarkers}')
    arucoDict=aruco.Dictionary_get(key)
    arucoParam=aruco.DetectorParameters_create()
    bbox, ids, rej=aruco.detectMarkers(imGray,arucoDict,parameters=arucoParam)
    if draw:
        aruco.drawDetectedMarkers(img,bbox)
    return [bbox,ids]

def arucoOrientation(bbox,drawId=True):
    tl=bbox[0][0][0],bbox[0][0][1]
    tr=bbox[0][1][0],bbox[0][1][1]
    bl=bbox[0][2][0],bbox[0][2][1]
    br=bbox[0][3][0],bbox[0][3][1]
    orientation=0
    if min(tl,tr,bl,br)==tl:
        orientation=0
    elif min(tl,tr,bl,br)==tr:
        orientation=1
    elif min(tl,tr,bl,br)==br:
        orientation=2
    elif min(tl,tr,bl,br)==bl:
        orientation=3
    

##################################################################################################
# Trignometric shit
    len1 = sqrt(tl[0] * tl[0] + tl[1] * tl[1])
    len2 = sqrt(tr[0] * tr[0] + tr[1] * tr[1])
    dot = tl[0] * tr[0] + tl[1] * tr[1]
    a = dot / (len1 * len2)
    if (a >= 1.0):
        return (orientation*90.0)
    elif (a <= -1.0):
        return pi
    else:
        return (orientation*90.0+cos(a))
# ################################################################################################
def main():
    cap=cv2.VideoCapture(0)

    while True:
        SUCCESS,img=cap.read()
        arucoFound=findArucoMarkers(img)

        if len(arucoFound[0])!=0:
            for bbox, id in zip(arucoFound[0],arucoFound[1]):
                print(arucoOrientation(bbox))
                print(bbox)

        cv2.imshow("image",img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__== "__main__":
    main()