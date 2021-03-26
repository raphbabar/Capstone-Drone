"""
Created on Mon Feb  8 18:50:30 2021

@author: Raphael
https://github.com/cheng0560011/circle-detection
https://www.pyimagesearch.com/2015/01/19/find-distance-camera-objectmarker-using-python-opencv/#pyi-pyimagesearch-plus-optin-modal
"""
import cv2
import numpy as np

# set video resolution to 480p
def make_480p():
    cap.set(3,640)
    cap.set(4,480)
def make_240p():
    cap.set(3,320)
    cap.set(4,240)

# capture video from Pi Camera using OpenCV
cap = cv2.VideoCapture(0)
width  = cap.get(3)
height = cap.get(4)
print("heigh & width is", height, width, "\n")
#h,w,d = cap.shape
#print("heigh, width and depth is", h,w,d, "\n")

make_240p()
# capture the next frame in the camera and obtain return boolean value if frame is received
ret, background = cap.read()
# convert image to grayscale
background = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)

while True :
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = gray-background 
    
    # find circle
    if ret :
        #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # convert videofram 2 gray image
        cv2.GaussianBlur(gray, (5, 5), 0)
        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 5, 300, param1=50, param2=300, minRadius=50, maxRadius=60) #GitHub
        #r = 100
        #circles = cv2.HoughCircles(gray,cv2.HOUGH_GRADIENT,1,20,param1=50,param2=30,minRadius=r,maxRadius=r+10)
        
        #circles = None
        if circles is not None:
            #count = 0
            circles = np.uint16(np.around(circles))
        
            for i in circles[0,:]:
                # draw the inner circle
                cv2.circle(frame,(i[0],i[1]),i[2],(0,255,0),2)
                cv2.circle(frame,(i[0],i[1]),2,(0,0,255),10)
                #font = cv2.FONT_HERSHEY_SIMPLEX
                #txt = ('[' + str(i[0]) + ',' + str(i[1]) + ']')
                #cv2.putText(frame, txt, (100,100+count*50), font, 1, (255,0,0), 1)
                #count = count+1    
    
    start_x = int((width/2)-75)
    start_y = int((height/2)-75)
    end_x = int((width/2)+75)
    end_y = int((height/2)+75)
    #print(width, height)
    #print(start_x, start_y)
    #print(circles)
    frame = cv2.rectangle(frame,(start_x,start_y),(end_x,end_y),(0,255,0),3)
    
    #if (circle[0][0]>start_x) and (circle[0][0]<end_x) and (circle[0][1]>start_y) and (circle[0][1]<end_y):
        #font = cv2.FONT_HERSHEY_SIMPLEX
        #txt = ('Inside')
        #cv2.putText(frame, txt, (10,10), font, 1, (255,0,0), 1)
    
    cv2.imshow('detected', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllwindows()