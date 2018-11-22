import cv2
import numpy as np
from pynput.mouse import Button, Controller
import wx

mouse=Controller()
app=wx.App(False)
(sx,sy)=wx.GetDisplaySize()
(camx,camy)=(320,240)

# lowerBound = np.array([33, 100, 40])
# upperBound = np.array([102, 255, 255])
# vert clair

# lowerBound = np.array([56, 133, 95])
# upperBound = np.array([107, 255, 191])
# vert foncé

c1,c2=regarde_la_couleur()
lowerBound=np.array(c1)
upperBound=np.array(c2)

# lowerBound = np.array([56, 133, 95])
# upperBound = np.array([107, 255, 191])

cam = cv2.VideoCapture(0)
cam.set(3,camx)
cam.set(4,camy)
kernelOpen = np.ones((5, 5))
kernelClose = np.ones((20, 20))

pinchFlag=0

while True:
    ret, img = cam.read()
    img = cv2.resize(img, (340, 220))

    # convert BGR to HSV
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # create the Mask
    mask = cv2.inRange(imgHSV, lowerBound, upperBound)
    # morphology
    maskOpen = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernelOpen)
    maskClose = cv2.morphologyEx(maskOpen, cv2.MORPH_CLOSE, kernelClose)

    maskFinal = maskClose
    _,conts,h = cv2.findContours(maskFinal.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    if(len(conts)==2):
        x1,y1,w1,h1=cv2.boundingRect(conts[0])
        x2, y2, w2, h2 = cv2.boundingRect(conts[1])
        #drawing rectangle over the objects
        cv2.rectangle(img, (x1, y1), (x1 + w1, y1 + h1), (255, 0, 0), 2)
        cv2.rectangle(img, (x2, y2), (x2 + w2, y2 + h2), (255, 0, 0), 2)
        #centre coordinate of first object
        cx1=int(x1+w1/2)
        cy1=int(y1+h1/2)
        #centre coordinate of second object
        cx2=int(x2+w2/2)
        cy2=int(y2+h2/2)
        #cntre coordinate of the line connection both points
        cx=int((cx1+cx2)/2)
        cy=int((cy1+cy2)/2)
        #Drawing the line
        cv2.line(img,(cx1,cy1),(cx2,cy2),(255,0,0),2)
        #Drawing the point (red)
        cv2.circle(img,(cx,cy),2,(0,0,255),2)
        if (pinchFlag==1):
            pinchFlag=0
            mouse.release(Button.left)
        mouseLoc=(int(sx-(cx*sx/camx)),int(cy*sy/camy))
        mouse.position=mouseLoc
        while mouse.position!=mouseLoc:
            pass

    elif(len(conts)==1):
        x, y, w, h = cv2.boundingRect(conts[0])
        if (pinchFlag==0):
            pinchFlag=1
            mouse.press(Button.left)
        # drawing the rectangle
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cx = int(x + w / 2)
        cy = int(y + h / 2)
        r=int((w+h)/4)
        cv2.circle(img,(cx,cy),r,(0, 0, 255), 2)

        mouse.press(Button.left)
        mouseLoc = (int(sx - (cx * sx / camx)), int(cy * sy / camy))
        mouse.position = mouseLoc
        while mouse.position != mouseLoc:
            pass


    #cv2.imshow("maskClose", maskClose)
    #cv2.imshow("maskOpen", maskOpen)
    #cv2.imshow("mask", mask)
    cv2.imshow("cam", img)
    cv2.waitKey(5)