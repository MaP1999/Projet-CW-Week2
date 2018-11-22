import cv2
import numpy as np
from pynput.mouse import Button, Controller
import wx
import Reconnaissance_de_couleur as rdc

mouse=Controller()
app=wx.App(False)
(sx,sy)=wx.GetDisplaySize()
(camx,camy)=(320,240)


##On définit les limites inf et sup d'accéptation pour le vert en HSV

#Il faut d'abord importer le code pyhton contenu dans le fichier reconnaissance_de_couleur !!!
lc1,hc1=rdc.regarde_la_couleur()
lc2,hc2=rdc.regarde_la_couleur()

lowerBound1 = np.array(lc1)
upperBound1 = np.array(hc1)
lowerBound2 = np.array(lc2)
upperBound2 = np.array(hc2)

cam = cv2.VideoCapture(0)
cam.set(3,camx)
cam.set(4,camy)
kernelOpen = np.ones((5, 5))
kernelClose = np.ones((20, 20))

pinchFlag=0

while True:
    ret, img = cam.read()
    #On lit la webcam(l'image à chaque tour est dans img)
    img = cv2.resize(img, (340, 220))
    #On donne une taille imposée au fenêtre

    #On créé maintenant les différent mask pour l'image (un mask est une autre image (de meme dimension) avec du blanc
    #là où la couleur est détéctée et du noir sur le reste)
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    #on convertit l'image de RGB en HSV

    # On créé maintenant les différent mask pour l'image (un mask est une autre image (de meme dimension) avec du blanc
    # là où la couleur est détéctée et du noir sur le reste)

    mask = cv2.inRange(imgHSV, lowerBound1, upperBound1)
    #Premier mask qui détécte "betement" le vert
    mask2 = cv2.inRange(imgHSV,lowerBound2,upperBound2)

    maskOpen = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernelOpen)
    # maskOpen est le premier mask sur lequel on a retiré le bruit (càd les petits point random)
    maskOpen2 = cv2.morphologyEx(mask2, cv2.MORPH_OPEN, kernelOpen)

    maskClose = cv2.morphologyEx(maskOpen, cv2.MORPH_CLOSE, kernelClose)
    # maskClose c'est maskOpen sur lequel les objets sont "remplis" (càd lorsqu'un objet à du bruit à l'intérieur (des
    # points où du vert n'est pas détécté à tord) les bruits sont dégagés)
    maskClose2 = cv2.morphologyEx(maskOpen2, cv2.MORPH_CLOSE,kernelClose)

    maskFinal = maskClose
    _,conts,h = cv2.findContours(maskFinal.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    #conts c'est la liste des points du contour de chaque objet vert donc len(conts) c'est le lombre d'objets détéctés)
    maskFinal2 = maskClose2
    _, conts2,_ = cv2.findContours(maskFinal2.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)


    if(len(conts)==2):
        draw_2cont(img,conts,2)
        if (pinchFlag==1):
            pinchFlag=0
            mouse.release(Button.left)
        mouseLoc=(int(sx-(cx*sx/camx)),int(cy*sy/camy))
        mouse.position=mouseLoc
        while mouse.position!=mouseLoc:
            pass

        if (len(conts2)==1):
            mouse.click(Button.left,2)


    elif(len(conts)==1):
        if(pinchFlag==0):
            pinchFlag=1
            mouse.press(Button.left)
        draw_2cont(img,conts,1)

        mouseLoc = (int(sx - (cx * sx / camx)), int(cy * sy / camy))
        mouse.position = mouseLoc
        while mouse.position != mouseLoc:
            pass


    #cv2.imshow("maskClose", maskClose)
    #cv2.imshow("maskOpen", maskOpen)
    #cv2.imshow("mask", mask)
    cv2.imshow("cam", img)
    cv2.waitKey(5)

