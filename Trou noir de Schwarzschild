#Importation des modules

import matplotlib.pyplot as plt
from scipy.integrate import odeint
import numpy as np
import matplotlib.animation as animation


nbGeodesigue = 60


#Création de la figure

fig = plt.figure()
ax = plt.axes(xlim = (-1.5,1.5), ylim = (-1,1))
line, = plt.plot([],[])
lines = []

for index in range(nbGeodesigue+1):
    lobj = ax.plot([],[])[0]
    lines.append(lobj)

def trou_noir(M):
    c = 1                      #vitesse de la lumière
    G = 1                      #constante gravitation universelle
    #M = 0.05                  #masse trou noir
    rs = (2*G*M)/(c**2)        #rayon Schwarzschild
    xnew = []                  #listes des listes des coordonnées des géodésiques
    ynew = []
    
    for a in range(nbGeodesigue):
        h0 = 5.125 - 0.18*a             #hauteur initiale
        d0 = 2                          #distance de référence
        phi0 = np.arctan(h0/d0)         #angle initial
        d = h0/(np.sin(phi0))           #distance au trou noir                  
        alpha = phi0                    #l'angle alpha pour la direction initiale du rayon
        
        if h0 > 0:
            phi = np.linspace(phi0,8*np.pi,1500)
        else:
            phi = np.linspace(phi0,phi0-8*np.pi,1500)
        
        def fonction(U,phi):       #définition de l'équa diff sous forme u'' = f(u,u')
            (u, du) = U
            return (du, 1.5 * rs * u**2 - u)
        
        U, dU = odeint(fonction, [1/d, 1/(d*np.tan(alpha))], phi).T 
        #résolution équa diff avec 2 conditions initiales u(0) et u'(0) en fonction de phi 
        
        U[U == 0] = 1     #Pour éviter les divisions par 0 dans le changement de variable de Binet
        R = 1/U
        
        u, v = R*np.cos(phi), R*np.sin(phi)
        
        condition = True
        xnew1 = []
        ynew1 = []

        for i in range(1500):
            a, b = u[i], v[i]
            if M == 0:
                xnew1.append(a)
                ynew1.append(b)
            if a<3 and a>-3 and b<3 and b>-3 and a**2 + b**2 > rs**2 and M!=0 and condition == True:
                xnew1.append(a)
                ynew1.append(b)
            else:
                condition = False
        
        #Cette boucle 'for' sert à ne plus considérer les géodésiques dès qu'elles sortent de l'écran
        #(limites en x et y fixées à -3 et 3) ou passent l'horizon des évènements du trou noir (sont à
        #l'intérieur du disque de rayon rs) pour éviter tous problèmes liés à la résolution de l'équation
        #différentielle 
        
        xnew.append(xnew1)
        ynew.append(ynew1)
    
    
    #Pour dessiner le cercle qui symbolise l'horizon des évènements du trou noir
    
    t = np.linspace(0, 2*np.pi, 100)
    m = rs*np.cos(t)
    n = rs*np.sin(t)
    xnew.append(m)
    ynew.append(n)
    return xnew, ynew
    
    

#Animation

def init():
    xnew2,ynew2 = trou_noir(0)    #On commence avec une masse nulle
    for k, line in enumerate(lines):
        line.set_data(xnew2[k],ynew2[k])
        print(line)
    print(lines)
    return lines


def animate(i):
    xnew2,ynew2 = trou_noir(0.00025*i)
    for k,line in enumerate(lines):
        line.set_data(xnew2[k],ynew2[k])
    return lines


ani = animation.FuncAnimation(fig, animate, init_func=init, frames=500, blit=True, interval=40)      
ani.save('black_hole_3.mp4' , fps = 30)
plt.show()
