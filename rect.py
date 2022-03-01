import cv2 as cv
import numpy as np
import math

cap = cv.VideoCapture(0)



while(True):
    ret, frame = cap.read()
    # frame = cv.GaussianBlur(frame, (5, 5), 0)
    copy=frame.copy()

    # cv.imshow('Threshold', thresh)
    cv.imshow('Camera', frame)

    if cv.waitKey(5) & 0xFF == ord('q'):
        break


cap.release()
cv.destroyAllWindows()