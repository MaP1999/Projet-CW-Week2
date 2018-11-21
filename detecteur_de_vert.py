import cv2 as cv
import numpy as np

lowerBound=np.array([33,80,40])
upperBound=np.array([102,255,255])
#On définit les limites inf et sup d'accéptation pour le vert en HSV

cam= cv.VideoCapture(0)
#On met dans cam la direction de la webcam

kernelOpen=np.ones((5,5))
kernelClose=np.ones((20,20))

font = cv.FONT_HERSHEY_SIMPLEX

while True:
    _,img=cam.read()
    #On lit la webcam (l'image à chaque tour est dans img)
    img=cv.resize(img,(340,220))
    #On donne une taille imposé au fenêtre
    
    imgHSV= cv.cvtColor(img,cv.COLOR_BGR2HSV)
    #on convertit l'image de RGB en HSV
    
    #On créé maintenant les différent mask pour l'image (un mask est une autre image (de meme dimension) avec du blanc la ou la couleur est détéctée et du noir sur le reste)
    mask=cv.inRange(imgHSV,lowerBound,upperBound)
    #Premier mask qui détécte "betement" le vert

    maskOpen=cv.morphologyEx(mask,cv.MORPH_OPEN,kernelOpen)
    # maskOpen est le premier mask sur lequel on a retiré le bruit (càd les petits point random)
    
    maskClose=cv.morphologyEx(maskOpen,cv.MORPH_CLOSE,kernelClose)
    # maskClose c'est maskOpen sur lequel les objets sont "remplis" (càd lorsqu'un objet à du bruit à l'intérieur (des points où du vert n'est pas détécté à tord) les bruits sont dégagés)
    
    maskFinal=maskClose
    
    (_,conts,_)=cv.findContours(maskFinal.copy(),cv.RETR_EXTERNAL,cv.CHAIN_APPROX_NONE)
    #conts c'est la liste des lites des point du contour de chaque objet vert objet vert (donc len(conts) c'est le lombre d'objets détéctés))
    #la fct cv2.findContours renvoie 3 éléments, mais on ne veut que le deuxième, donc les autres on les dégages (dans les underscores)

    for i in range(len(conts)):
        #pour chaque objet vert
        x,y,w,h=cv.boundingRect(conts[i])
        #renvoie, pour le plus petit rectangle "non penché" contenant tous les points de conts[i], les cordonnées du coins inférieur gauche (x,y) et le couple (w,h) tel que (x+w,y+h) soit les cordonnées du coin supérieur droit
        
        cv.rectangle(img,(x,y),(x+w,y+h),(0,0,255), 2)
        #Dessine le dit rectangle dans la couleur (0,0,255)
        
        cv.putText(img, str(i+1),(x,y+h),font,2,(0,0,0),1,cv.LINE_AA)
        #Numérotes les objets verts dans la couleur (0,0,0)
    
    cv.imshow("mask",mask)
    #montre le mask mask (celui sans corréction)    
    cv.imshow("maskOpen",maskOpen)
    #montre le mask maskOpen   
    cv.imshow("maskClose",maskClose)
    #montre le mask maskClose
    cv.imshow("cam",img)
    #Montre ce qu'il y a dans img (càd l'image de la webcam) avec les rectangles dessus
    
    if cv.waitKey(1) == 27:
        #Il suffit de faire echap pour fermer les fenetres
        cv.destroyAllWindows()
        break
        
#Corrigé et commenté par Marvin
    

 