import cv2 as cv
import numpy as np
import time as tm



def regarde_la_couleur():
    #On va regarder la couleur que l'on veut utiliser pour controller la souris
        
    cam= cv.VideoCapture(0)
    #On met dans cam la direction de la webcam
    
    while True:
        _,img=cam.read()
        #On lit la webcam (l'image à chaque tour est dans img)
        
        img=cv.resize(img,(340,220))
        #On donne une taille imposé au fenêtre
    
        cv.imshow("cam",img)
        #Montre ce qu'il y a dans img (càd l'image de la webcam) avec les rectangles dessus
        
        if cv.waitKey(1) == 27:
            #Il suffit de faire echap pour fermer les fenetres
            cv.destroyAllWindows()
            break
    
    H=[]
    S=[]
    V=[]
    #On créé des listes vides pour mettre les différentes valeurs HSV prises par la caméra
    
    for i in range (0,20):
        tm.sleep(0.1)
        #On va regarder toutes les 0.1 seconde pendant 2 secondes la couleur du pixel au centre de l'image que la webcam capte
        
        _,img=cam.read()
        #On lit la webcam (l'image à chaque tour est dans img)
        
        img=cv.resize(img,(340,220))
        #On donne une taille imposé à l'image
        
        imgHSV= cv.cvtColor(img,cv.COLOR_BGR2HSV)
        #on convertit l'image de RGB en HSV
        
        A=np.array(imgHSV, dtype=int)
        #on convertit en l image en tableau numpy
        
        couleur=A[110][170]
        #on prend le pixel du milieu
        
        H.append(couleur[0])
        S.append(couleur[1])
        V.append(couleur[2])
        #on fait des listes des valeurs possibles de H,S et V
         
    hmin=int(min(H)*0.7)
    smin=int(min(S)*0.7)
    vmin=int(min(V)*0.7)
    hmax=min(360,int(max(H)*1.3))
    smax=min(255,int(max(S)*1.3))
    vmax=min(255,int(max(V)*1.3))
    #on regarde les minimums et les maximums des listes H,S et V et on prend 10% de marges (pour les maximum on bornes évidements pas les valeurs maximales pouvant être prises)
    
    lowerBound=[hmin,smin,vmin]
    higherBound=[hmax,smax,vmax]
    
    return (lowerBound,higherBound)



