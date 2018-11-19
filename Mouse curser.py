import cv2
import numpy as np
from pynput.mouse import Button, Controller
import wx


pinchFlag=0# setting the pinch, which will be useful for the code to determine whether to click or drag
while True :
    .
    . #part of the color detection code
    .
    #Variable setup#
    mouse=Controller()
    app=wx.App(False)
    (sx,sy)=wx.GetDisplaySize()
    (camx,camy)=(320,240)

#to get the screen resolution we need an wx app then we can use the wx.GetDisplaySize() to get the screen resolution.#


#Reminder of the color recognition code's two last lines
    maskFinal=maskClose
    conts,h=cv2.findContours(maskFinal.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)


    if(len(conts)==2): #2 contours => scrolling
        # logic for the open gesture, move mouse without click
        x1,y1,w1,h1=cv2.boundingRect(conts[0])
        x2,y2,w2,h2=cv2.boundingRect(conts[1])
        # drawing rectangle over the objects
        cv2.rectangle(img,(x1,y1),(x1+w1,y1+h1),(255,0,0),2)
        cv2.rectangle(img,(x2,y2),(x2+w2,y2+h2),(255,0,0),2)
        #centre coordinate of first object
        cx1=x1+w1/2
        cy1=y1+h1/2
        # centre coordinate of the 2nd object
        cx2=x2+w2/2
        cy2=y2+h2/2
        # centre coordinate of the line connection both points
        cx=(cx1+cx2)/2
        cy=(cy1+cy2)/2
        # Drawing the line
        cv2.line(img, (cx1,cy1),(cx2,cy2),(255,0,0),2)
        # Drawing the point (red dot)
        cv2.circle(img, (cx,cy),2,(0,0,255),2)

        #positioning the mouse curser according to the calculated coordinate

        if(pinchFlag==1): #perform only if pinch is on
            pinchFlag=0 # setting pinch flag off
            mouse.release(Button.left)
        mouseLoc=(sx-(cx*sx/camx), cy*sy/camy)
        mouse.position=mouseLoc
        while mouse.position!=mouseLoc:
            pass
    elif(len(conts)==1):# implementing the click function
        :
        :
        if(pinchFlag==0): #perform only if pinch is off
            pinchFlag=1 # setting pinch flag on
            mouse.press(Button.left)
        mouseLoc=(sx-(cx*sx/camx), cy*sy/camy)
        mouse.position=mouseLoc
        while mouse.position!=mouseLoc:
            pass
    cv2.imshow("cam",img)
    cv2.waitKey(5)
