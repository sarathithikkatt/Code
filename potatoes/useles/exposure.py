import cv2

cap = cv2.VideoCapture(1)
# cap.set(cv2.CAP_PROP_EXPOSURE,-8)

while(True):
    ret, frame = cap.read()
    frame.set(cv2.CAP_PROP_EXPOSURE,-8)
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()