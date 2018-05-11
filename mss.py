"""
--------------------------------------------------------------------------
Michael D. Saneke
Robotics Final Project
OpenCV Code

Meanshift Algorithm retrieved from OpenCV Documentation:
https://docs.opencv.org/trunk/db/df8/tutorial_py_meanshift.html
--------------------------------------------------------------------------
"""


import socket
import time
from socket import socket, AF_INET, SOCK_DGRAM

import numpy as np
import cv2

#Set up socket connection between OpenCV program and EV3 robot
def send(direction):
    server = '192.168.2.2' #Robot IP address
    port = 8000            #Port number for connection
    size = 1024



    command = direction #Data to be sent to robot passed as an argument
    command = bytes(command, 'utf-8')  #Converting data to bytes since socket sends data as bytes


    mySocket = socket( AF_INET, SOCK_DGRAM )


    mySocket.sendto(command,(server,port))
    time.sleep(1)

#Meanshift Algorithm
def track():

    font = cv2.FONT_HERSHEY_SIMPLEX

    cap = cv2.VideoCapture(0)

    # take first frame of the video
    ret,frame = cap.read()

    # setup initial location of window
    # r,h,c,w - region of image
    #           simply hardcoded the values
    r,h,c,w = 250,80,650,80  
    track_window = (c,r,w,h)

    # set up the ROI for tracking
    roi = frame[r:r+h, c:c+w]
    hsv_roi =  cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_roi, np.array((0., 60.,32.)), np.array((180.,255.,255.)))
    roi_hist = cv2.calcHist([hsv_roi],[0],mask,[180],[0,180])
    cv2.normalize(roi_hist,roi_hist,0,255,cv2.NORM_MINMAX)

    # Setup the termination criteria, either 10 iteration or move by at least 1 pt
    term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )

    while(1):
        ret ,frame = cap.read()

        if ret == True:
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            dst = cv2.calcBackProject([hsv],[0],roi_hist,[0,180],1)

            # apply meanshift to get the new location
            ret, track_window = cv2.meanShift(dst, track_window, term_crit)

            # Draw it on image
            x,y,w,h = track_window
            img2 = cv2.rectangle(frame, (x,y), (x+w,y+h), 255,2)
            cv2.imshow('img2',img2)
            
            
            """
            My code to send commands to EV3 based on the direction the object being tracked moves
            """
            # x is the x cordinate of region of interest
            if (x > 750):     
                send('right') #Send right to make the robot move right
        
                
            if (x < 450):
                send('left') #Send left to make the robot move left
                
            
            k = cv2.waitKey(60) & 0xff
            
            if k == 27:
                break
            else:
                cv2.imwrite(chr(k)+".jpg",img2)
            
        else:
            break

    cap.release()
    cv2.destroyAllWindows()
    print(cap.isOpened())



def main():
    
    track()


main()
