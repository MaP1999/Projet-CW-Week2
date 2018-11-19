import cv2
import numpy as np

lowerBound=np.array([33,80,40])
upperBound=np.array([102,255,255])

cam= cv2.VideoCapture(0)
kernelOpen=np.ones((5,5))
kernelClose=np.ones((20,20))

font = cv2.FONT_HERSHEY_SIMPLEX

while True:
    ret, img=cam.read()
    img=cv2.resize(img,(340,220))
    
    #convert BGR to HSV
    imgHSV= cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    
    # create the Mask
    mask=cv2.inRange(imgHSV,lowerBound,upperBound)
    #un mask est une autre image (de meme dimension) avec du blanc la ou la couleur est détéctée et du noir sur le reste
    
    #morphology
    maskOpen=cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernelOpen)
    maskClose=cv2.morphologyEx(maskOpen,cv2.MORPH_CLOSE,kernelClose)
    # maskopen c'est le premier mask sur lequel on a retiré le bruit (et il y a un parametre kernelOpen que je comprend pas...)
    # On réitère avec maskOpen pour obtenir maskClose (et il y a encore un parametre que je ne comprend pas : KernelClose. Il faudrait essayer de les enlever)
    maskFinal=maskClose
    (_,conts,_)=cv2.findContours(maskFinal.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    #conts c'est la liste des lites des point du contour de chaque objet vert objet vert (donc len(conts) c'est le lombre d'objets détéctés))
    #la fct cv2.findContours renvoie 3 éléments, mais on ne veut que le deuxième, donc les autres on les dégages (dans les underscore)

    for i in range(len(conts)):
        x,y,w,h=cv2.boundingRect(conts[i])
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255), 2)
        cv2.putText(img, str(i+1),(x,y+h),font,2,(0,255,255),1,cv2.LINE_AA)
    cv2.imshow("maskClose",maskClose)
    cv2.imshow("maskOpen",maskOpen)
    cv2.imshow("mask",mask)
    cv2.imshow("cam",img)
    if cv2.waitKey(1) == 27:
        cv2.destroyAllWindows()
        break
    

 