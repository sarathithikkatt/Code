import cv2
import numpy as np
import math

def distance(x1, y1, x2, y2):
    """
    Calculate distance between two points
    """
    dist = math.sqrt(math.fabs(x2-x1)**2 + math.fabs(y2-y1)**2)
    return dist

def find_color1(frame):
    """
    Filter "frame" for HSV bounds for color1 (inplace, modifies frame) & return coordinates of the object with that color
    """
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv_lowerbound = np.array([0, 132, 101]) #replace THIS LINE w/ your hsv lowerb
    hsv_upperbound = np.array([179, 227, 255])#replace THIS LINE w/ your hsv upperb
    mask = cv2.inRange(hsv_frame, hsv_lowerbound, hsv_upperbound)
    res = cv2.bitwise_and(frame, frame, mask=mask) #filter inplace
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
            return (700, 700), False #faraway point
    else:
        return (700, 700), False #faraway point

def find_color2(frame):
    """
    Filter "frame" for HSV bounds for color1 (inplace, modifies frame) & return coordinates of the object with that color
    """
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
            return (700, 700), True #faraway point
    else:
        return (700, 700), True #faraway point

def dist(x,y,u,v):
    return str(math.sqrt((u-x)**2+(v-y)**2))

cap = cv2.VideoCapture(1,cv2.CAP_DSHOW)

while(1):
    timer=cv2.getTickCount()
    _, orig_frame = cap.read()
    #we'll be inplace modifying frames, so save a copy
    copy_frame = orig_frame.copy() 
    (color1_x, color1_y), found_color1 = find_color1(copy_frame)
    (color2_x, color2_y), found_color2 = find_color2(copy_frame)

    #draw circles around these objects
    cv2.circle(copy_frame, (color1_x, color1_y), 20, (255, 0, 0), -1)
    cv2.circle(copy_frame, (color2_x, color2_y), 20, (0, 128, 255), -1)

    if found_color1 and found_color2:
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
        
        distance_text=""
        if(angle_text!=np.NaN):
            distance_text=dist(color1_x,color1_y,color2_x,color2_y)

        #CHANGE FONT HERE
        cv2.putText(copy_frame, "angle="+angle_text, (30,60), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 128, 229), 2)
        cv2.putText(copy_frame, "distance="+distance_text, (30,90), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 128, 229), 2)

        fps =str(int(cv2.getTickFrequency()/(cv2.getTickCount()-timer)))
        cv2.putText(copy_frame,"FPS:"+fps,(30,30),cv2.FONT_HERSHEY_COMPLEX, 1, (0, 128, 229), 2)

    cv2.imshow('AngleCalc', copy_frame)
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()