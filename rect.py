import cv2
import argparse
import imutils

camera = cv2.VideoCapture(0)

# ap=argparse._ArgumentParser()
# ap.add_argument("-i","--image",required=True,help=)

while(True):
    _, image = camera.read()
    gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    blurred=cv2.GaussianBlur(gray,(5,5),0)
    thresh=cv2.threshold(blurred,60,255,cv2.THRESH_BINARY)
    # threshcopy=thresh
    cnts=cv2.findContours(blurred,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts=imutils.grab_contours(cnts)
    for c in cnts:
        M=cv2.moments(c)
        cX=int(M["m10"] / M["m00"])
        cY=int(M["m01"] / M["m00"])
        cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
        cv2.circle(image, (cX, cY), 7, (255, 255, 255), -1)
        cv2.putText(image, "center", (cX - 20, cY - 20),
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        cv2.imshow("Stuff",image)
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break
camera.release()
cv2.destroyAllWindows()