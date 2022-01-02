import cv2
import math
import numpy as np


cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)

while(True):
    ret, frame = cap.read()
    copy=frame.copy()
    gray=cv2.cvtColor(copy,cv2.COLOR_BGR2GRAY)
    ret,thresh=cv2.threshold(gray,217,255,cv2.THRESH_BINARY)


    contours, hierarchy = cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(image=copy, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)
    cv2.imshow('contour',copy)




    cv2.imshow('Camera', frame)
    cv2.imshow('Binary', thresh)
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()