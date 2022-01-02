import cv2

cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)

tracker=cv2.legacy.TrackerMOSSE_create()
success, img=cap.read()
bound=cv2.selectROI("Trial",img,False)
print(bound)
tracker.init(img,bound)

def drawBox():
    return 0
    
while True:    
    timer=cv2.getTickCount()
    success, img=cap.read()

    success,bound=tracker.update(img)

    if success:
        drawBox()
    else:
        cv2.putText(img,"Lost",(75,75),cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,0.7,(0,0,255),2)


    fps=str(int(cv2.getTickFrequency()/(cv2.getTickCount()-timer)))
    cv2.putText(img,fps,(75,50),cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,0.7,(0,0,255),2)
    cv2.imshow("Trial",img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()