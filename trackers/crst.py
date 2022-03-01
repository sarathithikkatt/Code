import cv2

cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)

tracker=cv2.legacy.TrackerCSRT_create()
success, img=cap.read()
bbox=cv2.selectROI("Trial",img,False)
print(bbox)
tracker.init(img,bbox)

def drawBox(img,bbox):
    x,y,w,h=int(bbox[0]),int(bbox[1]),int(bbox[2]),int(bbox[3])
    cv2.rectangle(img,(x,y),((x+w),(y+h)),(255,0,255),3,1)
    cv2.putText(img,"Tracking",(75,75),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,255))
    
while True:    
    timer=cv2.getTickCount()
    success, img=cap.read()

    success,bbox=tracker.update(img)

    if success:
        drawBox(img,bbox)
    else:
        cv2.putText(img,"Lost",(75,75),cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,0.7,(0,0,255),2)


    fps=str(int(cv2.getTickFrequency()/(cv2.getTickCount()-timer)))
    cv2.putText(img,fps,(75,50),cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,0.7,(0,0,255),2)
    cv2.imshow("Trial",img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()