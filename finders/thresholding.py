import cv2 as cv
import numpy as np
import math

def nothing(x):
    pass

barsWindow = 'Bars'
tl = 'Thresh Low'
th = 'Thresh High'

# set up for video capture on camera 0
cap = cv.VideoCapture(0)

# create window for the slidebars
cv.namedWindow(barsWindow, flags = cv.WINDOW_AUTOSIZE)

# create the sliders
cv.createTrackbar(tl, barsWindow, 0, 255, nothing)
cv.createTrackbar(th, barsWindow, 0, 255, nothing)

# set initial values for sliders
cv.setTrackbarPos(tl, barsWindow, 0)
cv.setTrackbarPos(th, barsWindow, 255)

while(True):
    ret, frame = cap.read()
    frame = cv.GaussianBlur(frame, (5, 5), 0)
    copy=frame.copy()
    # convert to GRAYSCALE from BGR
    gray=cv.cvtColor(copy,cv.COLOR_BGR2GRAY)

    # read trackbar positions for all
    hul = cv.getTrackbarPos(tl, barsWindow)
    huh = cv.getTrackbarPos(th, barsWindow)

    # make array for final values
    threshlow = hul
    threshhigh = huh

    # apply the range on a mask
    # maskedFrame = cv.bitwise_and(frame, frame, mask = mask)
    ret,thresh=cv.threshold(gray,hul,huh,cv.THRESH_BINARY)


    # display the camera and masked images
    cv.imshow('Threshold', thresh)
    cv.imshow('Camera', frame)

	# check for q to quit program with 5ms delay
    if cv.waitKey(5) & 0xFF == ord('q'):
        break

# clean up our resources

cap.release()
cv.destroyAllWindows()