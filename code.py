# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 18:16:28 2018

@author: Nasreddine
"""
import matplotlib.pyplot as plt
from scipy import ndimage
from skimage import io
import numpy as np
from skimage import morphology

plt.close('all')
img = io.imread("capture.png")
img = img[:,:,0]
img_copie=np.copy(img)

##############################################################
""" Seuillage Otsu """
taille=img.shape
nbLigne=taille[0]
nbColonne=taille[1]
nbTotal=nbLigne*nbColonne
### Variance Totale
VarTotale = np.var(img)
### Histogramme
H=ndimage.histogram(img, 0, 255, 256)
varIntra = []
for seuil in range(1,256):    
    ## Variance fond
    m1 = 0
    nb1 = 0
    var1 = 0
    for i in range(0,seuil):
        m1 += H[i]*i
        nb1 += H[i]
    m1 /= nb1
    for j in range(0,seuil):
        var1 += (H[j]*(j-m1)**2)
    var1 /= nb1
    ## Variance objet
    m2 = 0
    nb2 = 0
    var2 = 0
    for k in range(seuil,256):
        m2 += H[k]*k
        nb2 += H[k]
    m2 /= nb2
    for l in range(seuil,256):
        var2 += (H[l]*(l-m2)**2)
    var2 /= nb2
    ## Variance intra    
    varIntra.append((var1*nb1/nbTotal)+(var2*nb2/nbTotal))
     
Seuil = varIntra.index(min(varIntra))
### Binarisation:
for i in range (nbLigne):
    for j in range (nbColonne):
        if (img[i,j]<Seuil):
            img[i,j] = 0
        else:
            img[i,j] = 255

##############################################################
""" Calcul de la projections verticale pour définir les lignes """
p=np.sum(img,1)

max_p= max(p)
indice_lignes = []
for i in range(len(p)):
    if (p[i] != max(p) & p[i-1] == max(p)):
        indice_lignes.append(i-1)
    if (p[i-1] < max(p) & p[i] == max(p)):
        indice_lignes.append(i)
## indice_lignes contient le début et la fin de chaque ligne de sorte :
        ## indice_lignes[0] : est le début de la ligne
        ## indice_lignes[1] : est la fin de la ligne

#Ceci est pour le test      
#img [indice_lignes] = 0


""" Calcul des projections horizontales pour chaque ligne """
ligne = []
for i in range(int(len(indice_lignes))):
    pp=0
    if (i%2 == 0):
        tmp = np.copy (img[indice_lignes[i]:indice_lignes[i+1],:])
        pp=np.sum(img[indice_lignes[i]:indice_lignes[i+1],:],0)
        ligne.append(pp)

""" Découpage des mots au sein de chaque ligne """
## Je considère qu'un espace correpond au moins à 3 pixels blancs
indices_mots=[]
for i in range (len(ligne)):
    tmp = []
    for j in range (len(ligne[i])):
        if ligne[i][j] < max(ligne[i]) & ligne[i][j-1] == max(ligne[i]) & ligne[i][j-2] == max(ligne[i]) & ligne[i][j-3] == max(ligne[i]) :
            tmp.append(j-1)
        elif (j+3 <= len(ligne[i])):
            if ligne[i][j] < max(ligne[i]) & ligne[i][j+1] == max(ligne[i]) & ligne[i][j+2] == max(ligne[i]) & ligne[i][j+3] == max(ligne[i]):
                tmp.append(j+1)
    indices_mots.append(tmp)

""" affichage du découpage """
gray = np.copy(img)
cpt = 0
plt.figure()
for j in range (len(indice_lignes)):
    if j%2 == 0:
        a = np.copy(gray[indice_lignes[j]:indice_lignes[j+1],:])
        a[:,indices_mots[cpt]] = 0
        cpt += 1
        plt.subplot(len(ligne),1,cpt)
        plt.imshow(a, cmap = plt.get_cmap('gray'))

##############################################################

mots = []
cpt = -1
for i in range (0,int(len(indice_lignes))):
    if i%2 == 0 :
        cpt += 1
        Nombre2mot = int(len(indices_mots[cpt]))
        for j in range (0,Nombre2mot):
            if j%2==0:
                tmp = []
                a=indice_lignes[i]
                b=indice_lignes[i+1]
                c=indices_mots[cpt][j]
                d=indices_mots[cpt][j+1]
                mot=np.copy(img[a:b,c:d])
                plt.figure()
                plt.imshow(mot,cmap = plt.get_cmap('gray'))
                tmp = [mot]+[a]+[b]+[c]+[d]
                mots.append(tmp)
                break
            
                
plt.imshow(mots[15][0],cmap = plt.get_cmap('gray'))

def similarite (a,b):
    A=plt.hist(a)
    B=plt.hist(b)
    if A/B > 0.8:
        return 1
    else:
        return 0
    
a = morphology.label(mots[15][0])
b = morphology.label(mots[11][0])
plt.figure()
plt.show(mots[0][0])
