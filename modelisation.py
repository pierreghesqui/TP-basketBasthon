import cv2
from vecteur import Vecteur
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

class Modelisation:
    def __init__(self):
        print("Veuillez Patientez quelques instants...")
        self.ecranLargeur = 1920
        self.ecranHauteur = 1080
        self.listImages = []
        self.imageEnCours = 0
        self.image = cv2.imread("frame0.png")
        self.nbLignes = self.image.shape[0]
        self.nbColonnes = self.image.shape[1]
        self.pixelSize = 0.00876  #metre par pixel
        self.ratioFenetre = self.nbColonnes/self.nbLignes
        self.nbImages = 39
        self.positions = []
        self.vitesses = []

    def stockeInfo(self, position, vitesse,F):
        self.image = cv2.imread(
            'frame'+str(self.imageEnCours)+'.png')
        
        
        cv2.putText(self.image, "IMAGE "+str(self.imageEnCours), (30, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.25, (255, 255, 255), 2, cv2.LINE_AA)
        
        if vitesse.x !=0 and vitesse.y!=0:
            start_point = self.metersToPixel(position)
            start_point = Vecteur(start_point.x, self.nbLignes-start_point.y)
            
            end_point = position+vitesse/10
            end_point = self.metersToPixel(end_point)
            end_point = Vecteur(end_point.x, self.nbLignes-end_point.y)
            color = (0, 255, 0) #BGR
            thickness = 5
            cv2.arrowedLine(self.image, (start_point.x,start_point.y), (end_point.x,end_point.y),
                                         color, thickness)
            cv2.putText(self.image, "v ", (end_point.x-10,end_point.y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.25, color, 2, cv2.LINE_AA)
            cv2.arrowedLine(self.image, (end_point.x-10,end_point.y-35), (end_point.x+10,end_point.y-35),
                                         color, 2)
        if  F.y!=0 : #self.imageEnCours == 3 and
            end_point = position+F/10
            end_point = self.metersToPixel(end_point)
            end_point = Vecteur(end_point.x, self.nbLignes-end_point.y)
            colorForce = (0, 0, 255) #BGR
            cv2.arrowedLine(self.image, (start_point.x,start_point.y), (end_point.x,end_point.y),
                                         colorForce, thickness)
            cv2.putText(self.image, "F ", (end_point.x+20,end_point.y-20),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.25, colorForce, 2, cv2.LINE_AA)
            cv2.arrowedLine(self.image, (end_point.x+20,end_point.y-50), (end_point.x+50,end_point.y-50),
                                         colorForce, 2)
        self.dessineCroix(position)
        self.listImages.append(np.copy(self.image))
        self.imageEnCours = self.imageEnCours +1
    
    def anima(self):
        print("Votre modélisation va bientôt apparaître ...")
        fig = plt.figure()
        nbImages = self.imageEnCours
        listImages = self.listImages
        im = plt.imshow(listImages[0],animated=True)
        def updatefig(i):   
            im.set_array(listImages[i])
            return im,
        anim = animation.FuncAnimation(fig, updatefig ,frames=nbImages, interval=50,repeat=True)
        return anim
        #writervideo = animation.PillowWriter(fps=60)
        #anim.save('increasingStraightLine.gif', writer=writervideo)
        
    def metersToPixel(self, lc):
        pix = lc/self.pixelSize
        pix = Vecteur(int(pix.x), int(pix.y))
        return pix

    def pixelToMeters(self, pix):
        lc = pix*self.pixelSize
        return lc

    def dessineCroix(self, position):
        pix = self.metersToPixel(position)
        pix = Vecteur(pix.x, self.nbLignes-pix.y)
        tailleCroix = 8
        color = (255, 255, 255)
        cv2.line(self.image, (pix.x-tailleCroix, pix.y-tailleCroix),
                 (pix.x+tailleCroix, pix.y+tailleCroix), color, 2)
        cv2.line(self.image, (pix.x+tailleCroix, pix.y-tailleCroix),
                 (pix.x-tailleCroix, pix.y+tailleCroix), color, 2)
        '''
        cv2.putText(self.image, "PREVISION", (pix.x, pix.y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.25, color, 2, cv2.LINE_AA)
        '''
    def dessineVecteur(self, vposition, vecteur, echelle=0.5):
        end_point = vposition+vecteur*echelle
        # print(position)
        vposition = self.metersToPixel(vposition)
        vposition = Vecteur(vposition.x, self.nbLignes-vposition.y)
        
        end_point = self.metersToPixel(end_point)
        end_point = Vecteur(end_point.x, self.nbLignes-end_point.y)
        
        self.image = cv2.arrowedLine(self.image, (vposition.x, vposition.y), (end_point.x,
                                     end_point.y), (255, 255, 0), 2)

  