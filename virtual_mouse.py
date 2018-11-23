import cv2
import numpy as np
from pynput.mouse import Button, Controller
import wx
import Reconnaissance_de_couleur as rdc
import draw_cont as draw

#Description: Controler la souris du Rasberry avec la reconnaissance de un ou deux curseur: la création d'une souris virtuelle
#in: /
#out:/

##VARIABLE GLOBALE NECESSAIRE

mouse=Controller()
app=wx.App(False)
(sx,sy)=wx.GetDisplaySize()
(camx,camy)=(320,240)

couleur="vert"
#variable qui choisit entre calibration et couleur vert de base
if couleur=="vert":
    lowerBound = np.array([33, 100, 40])
    upperBound = np.array([102, 255, 255])
elif couleur=="calib":
    lc1,hc1=rdc.regarde_la_couleur()
    lowerBound = np.array(lc1)
    upperBound = np.array(hc1)
#On définit les limites inf et sup d'accéptation pour la couleur en HSV

cam = cv2.VideoCapture(0)
cam.set(3,camx)
cam.set(4,camy)
kernelOpen = np.ones((5, 5))
kernelClose = np.ones((20, 20))

pinchFlag=0
#variable pour garder clic gauche enfoncer

while True:

    ##PROPRIETE DE LA RECONNAISSANCE DE COULEUR

    ret, img = cam.read()
    #On lit la webcam (l'image à chaque tour est dans img)
    img = cv2.resize(img, (340, 220))
    #On donne une taille imposée aux fenêtres

    #On crée maintenant les différents mask pour l'image (un mask est une autre image (de même dimension) avec du blanc
    #là où la couleur est détéctée et du noir sur le reste)
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    #on convertit l'image de RGB en HSV

    # On crée maintenant les différents mask pour l'image (un mask est une autre image (de même dimension) avec du blanc
    # là où la couleur est détéctée et du noir sur le reste)

    mask = cv2.inRange(imgHSV, lowerBound, upperBound)
    #Premier mask qui détécte "bêtement" le vert
    maskOpen = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernelOpen)
    # maskOpen est le premier mask sur lequel on a retiré le bruit (càd les petits points random)
    maskClose = cv2.morphologyEx(maskOpen, cv2.MORPH_CLOSE, kernelClose)
    # maskClose c'est maskOpen sur lequel les objets sont "remplis" (càd lorsqu'un objet à du bruit à l'intérieur

    maskFinal = maskClose
    _,conts,h = cv2.findContours(maskFinal.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    #conts c'est la liste des points du contour de chaque objet vert donc len(conts) c'est le lombre d'objets détéctés)


    ##SI ON A DEUX CURSEURS => DEPLACEMENT DE LA SOURIS AU CENTRE


    if(len(conts)==2):
        #deux curseurs
        cx,cy = draw.drawcont(img,conts)
        #dessine les contours

        if(pinchFlag==1):
            pinchFlag=0
            mouse.release(Button.left)
        #garde le clic gauche enfoncé

        mouseLoc=(int(sx-(cx*sx/camx)),int(cy*sy/camy))
        mouse.position=mouseLoc

        while mouse.position!=mouseLoc:
            pass

    ##SI ON A UN CURSEUR => CLIC GAUCHE ENFONCE

    elif(len(conts)==1):
        #un curseur
        if (pinchFlag==0):
            pinchFlag=1
            mouse.press(Button.left)
        #stop le clic gauche

        cx,cy = draw.drawcont(img,conts)
        mouseLoc = (int(sx - (cx * sx / camx)), int(cy * sy / camy))
        mouse.position = mouseLoc
        while mouse.position != mouseLoc:
            pass
        #place la souris
    cv2.imshow("cam", img)

    if cv2.waitKey(100) ==27:
        cv2.destroyAllWindows()
        break





