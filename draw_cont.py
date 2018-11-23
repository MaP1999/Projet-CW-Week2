import cv2
#Description: dessine les contours des curseurs et lorsqu'il y en a deux, une ligne rejoignant les deux avec un point au centre
#in: -img: flux de la vidéo
#    -conts: les curseurs
#out: cx,cy si 1 curseur = son centre
#           si 2 curseur = milieu des deux
def drawcont(img,conts):
    x=len(conts)
    if  x==1:
        x, y, w, h = cv2.boundingRect(conts[0])
        # dessine le rectangle
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cx = int(x + w / 2)
        cy = int(y + h / 2)
        r=int((w+h)/4)
        cv2.circle(img,(cx,cy),r,(0, 0, 255), 2)
        return cx,cy
        #renvoie le centre du curceur

    elif x==2:
        x1,y1,w1,h1=cv2.boundingRect(conts[0])
        x2, y2, w2, h2 = cv2.boundingRect(conts[1])
        # renvoie, pour le plus petit rectangle "non penché" contenant tous les points des deux rectangles détectés,
        # les coordonnées du coin inférieur gauche (x,y) et le couple (w,h) tel que (x+w,y+h) soit les coordonnées du coin
        # supérieur droit
        cv2.rectangle(img, (x1, y1), (x1 + w1, y1 + h1), (255, 0, 0), 2)
        cv2.rectangle(img, (x2, y2), (x2 + w2, y2 + h2), (255, 0, 0), 2)
        #Dessine les deux rectangles de couleur (0,0,255)

        # renvoie, pour le plus petit rectangle "non penché" contenant tous les points des deux rectangles détectés,
        # les cordonnées du coin inférieur gauche (x,y) et le couple (w,h) tel que (x+w,y+h) représente les coordonnées du coin
        # supérieur droit

        cx1=int(x1+w1/2)
        cy1=int(y1+h1/2)
            #
        cx2=int(x2+w2/2)
        cy2=int(y2+h2/2)

        cx=int((cx1+cx2)/2)
        cy=int((cy1+cy2)/2)
        #Dessine la ligne
        cv2.line(img,(cx1,cy1),(cx2,cy2),(255,0,0),2)
        #Dessine le point (rouge)
        cv2.circle(img,(cx,cy),2,(0,0,255),2
                   )
        return cx,cy
        #milieu des deux curseurs

