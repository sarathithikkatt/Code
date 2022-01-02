import cv2
import math
import numpy as np

target_x,target_y=0,0

def distance(x1, y1, x2, y2):
    dist = math.sqrt(math.fabs(x2-x1)**2 + math.fabs(y2-y1)**2)
    return dist

def red_color(frame):
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv_lowerbound = np.array([146,0,226])
    hsv_upperbound = np.array([179,255,255])
    mask = cv2.inRange(hsv_frame, hsv_lowerbound, hsv_upperbound)
    res = cv2.bitwise_and(frame, frame, mask=mask)
    cnts, hir = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len(cnts) > 0:
        maxcontour = max(cnts, key=cv2.contourArea)
        
        M = cv2.moments(maxcontour)
        if M['m00'] > 0 and cv2.contourArea(maxcontour) > 1000:
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            return (cx, cy), True
        else:
            return (700, 700), False
    else:
        return (700, 700), False

def blue_color(frame):
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv_lowerbound = np.array([71,0,226])
    hsv_upperbound = np.array([145,255,255])
    mask = cv2.inRange(hsv_frame, hsv_lowerbound, hsv_upperbound)
    res = cv2.bitwise_and(frame, frame, mask=mask)
    cnts, hir = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
    if len(cnts) > 0:
        maxcontour = max(cnts, key=cv2.contourArea)

        M = cv2.moments(maxcontour)
        if M['m00'] > 0 and cv2.contourArea(maxcontour) > 1000:
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            return (cx, cy), True
        else:
            return (700, 700), False
    else:
        return (700, 700), False

def orientation(color1_x,color1_y,color2_x,color2_y):
    hypotenuse = distance(color1_x, color1_x, color2_x, color2_y)
    horizontal = distance(color1_x, color1_y, color2_x, color1_y)
    vertical = distance(color2_x, color2_y, color2_x, color1_y)
    if(hypotenuse!=0):
        angle = np.arcsin(vertical/hypotenuse)*180/math.pi
    cv2.line(copy_frame, (color1_x, color1_y), (color2_x, color2_y), (0, 0, 255), 1)
    cv2.line(copy_frame, (color1_x, color1_y), (color2_x, color1_y), (0, 0, 255), 1)
    cv2.line(copy_frame, (color2_x, color2_y), (color2_x, color1_y), (0, 0, 255), 1)

    angle_text = ""
    if color2_y < color1_y and color2_x > color1_x:
        angle_text = str(angle)
    elif color2_y < color1_y and color2_x < color1_x:
        angle_text = str(180 - angle)
    elif color2_y > color1_y and color2_x < color1_x:
        angle_text = str(180 + angle)
    elif color2_y > color1_y and color2_x > color1_x:
        angle_text = str(360 - angle)
    return angle_text

def mousepoints(event,x,y,flags,params):
    global target_x,target_y
    if event==cv2.EVENT_LBUTTONDOWN:
        target_x,target_y= x,y
    elif(event==cv2.cv2.EVENT_RBUTTONDOWN):
        target_x,target_y=0,0

cap = cv2.VideoCapture(1,cv2.CAP_DSHOW)

while(True):
    timer=cv2.getTickCount()
    ret, frame = cap.read()
    copy_frame = frame.copy() 
    (color1_x, color1_y), found_red = red_color(copy_frame)
    (color2_x, color2_y), found_blue = blue_color(copy_frame)
    
    cv2.imshow("Orginal Feed",frame)
    fps =str(int(cv2.getTickFrequency()/(cv2.getTickCount()-timer)))
    cv2.putText(copy_frame,"FPS:"+fps,(30,30),cv2.FONT_HERSHEY_COMPLEX, 1, (0, 128, 229), 2)
    if(found_red and found_blue):

        angle=orientation(color1_x,color1_y,color2_x,color2_y)
        cv2.putText(copy_frame, "orientation="+angle, (30,60), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 128, 229), 2)
        if(target_x!=0 and target_y!=0):

            target_angle=orientation(color1_x,color1_y,target_x,target_y)
            target_distance=distance(color1_x,color1_y,target_x,target_y)
            cv2.putText(copy_frame, "angle="+str(target_angle), (30,90), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 128, 229), 2)
            cv2.putText(copy_frame, "distance="+str(target_distance), (30,120), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 128, 229), 2)

            
        cv2.imshow('Angle', copy_frame)
            
        cv2.setMouseCallback('Angle',mousepoints)  

    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()