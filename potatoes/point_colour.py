import cv2
import numpy as np
import math

cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
target_x=int(cv2.CAP_PROP_FRAME_HEIGHT/2)
target_y=int(cv2.CAP_PROP_FRAME_WIDTH/2)

def distance(x1, y1, x2, y2):
    dist = math.sqrt(math.fabs(x2-x1)**2 + math.fabs(y2-y1)**2)
    return dist

# Blue
def find_point1(frame):
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv_lowerbound = np.array([0, 132, 101])
    hsv_upperbound = np.array([179, 227, 255])
    mask = cv2.inRange(hsv_frame, hsv_lowerbound, hsv_upperbound)
    res = cv2.bitwise_and(frame, frame, mask=mask)
    cnts, hir = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len(cnts) > 0:
        maxcontour = max(cnts, key=cv2.contourArea)
        #Find center of the contour 
        M = cv2.moments(maxcontour)
        if M['m00'] > 0 and cv2.contourArea(maxcontour) > 1000:
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            return (cx, cy), True
        else:
            return (700, 700), False
    else:
        return (700, 700), False

# Red
def find_point2(frame):    
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv_lowerbound=np.array([0,28,226])
    hsv_upperbound=np.array([66,243,255])
    mask = cv2.inRange(hsv_frame, hsv_lowerbound, hsv_upperbound)
    res = cv2.bitwise_and(frame, frame, mask=mask)
    cnts, hir = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len(cnts) > 0:
        maxcontour = max(cnts, key=cv2.contourArea)
        #Find center of the contour 
        M = cv2.moments(maxcontour)
        if M['m00'] > 0 and cv2.contourArea(maxcontour) > 2000:
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            return (cx, cy), True #True
        else:
            return (700, 700), True
    else:
        return (700, 700), True

def find_click(event,x,y,float,params):
    if event==cv2.EVENT_LBUTTONDOWN:
        return(x,y), True
    else:
        return(target_x,target_y),False
        

while(1):
    _, orig_frame = cap.read()
    copy_frame = orig_frame.copy() 
    cv2.imshow('AngleCalc', copy_frame)
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break
    (color1_x, color1_y), found_point1 = find_point1(copy_frame)
    # (target_x, target_y) = (0,0)
    (target_x, target_y)=cv2.setMouseCallback("AngleCalc",find_click)

    #draw circles around the objects
    cv2.circle(copy_frame, (color1_x, color1_y), 5, (255, 0, 0), -1)
    cv2.circle(copy_frame, (target_x, target_y), 5, (0, 128, 255), -1)

    if found_point1 and found_point2:
        #trig stuff to get the line
        hypotenuse = distance(color1_x, color1_x, color2_x, color2_y)
        horizontal = distance(color1_x, color1_y, color2_x, color1_y)
        vertical = distance(color2_x, color2_y, color2_x, color1_y)
        if(hypotenuse!=0):
            angle = np.arcsin(vertical/hypotenuse)*180/math.pi
        # else:
        #     angle=0

        #draw all 3 lines
        cv2.line(copy_frame, (color1_x, color1_y), (color2_x, color2_y), (0, 0, 255), 1)
        cv2.line(copy_frame, (color1_x, color1_y), (color2_x, color1_y), (0, 0, 255), 1)
        cv2.line(copy_frame, (color2_x, color2_y), (color2_x, color1_y), (0, 0, 255), 1)

        #put angle text (allow for calculations upto 180 degrees)
        angle_text = ""
        if color2_y < color1_y and color2_x > color1_x:
            angle_text = str(angle)
        elif color2_y < color1_y and color2_x < color1_x:
            angle_text = str(180 - angle)
        elif color2_y > color1_y and color2_x < color1_x:
            angle_text = str(180 + angle)
        elif color2_y > color1_y and color2_x > color1_x:
            angle_text = str(360 - angle)
        
        #CHANGE FONT HERE
        cv2.putText(copy_frame, angle_text, (color1_x-30, color1_y), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 128, 229), 2)

cap.release()
cv2.destroyAllWindows()