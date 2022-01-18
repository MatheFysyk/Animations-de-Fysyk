#Importation des modules nécessaires

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.integrate import odeint


#Constantes

G = 1
m_1 = 1
m_2 = 50


#Conditions initiales

x_10, y_10, x_20, y_20 = -4, 0, 2, 0
dx_10, dy_10, dx_20, dy_20 = 2, 2, 0, 0

t0 = 0
tf = 5

nb_pts = 1000

#etat = 550


#Définition des limites de la figure

x_min = -16
x_max = 16
y_min = -10
y_max = 10


#Création figure


fig, ax = plt.subplots()

#Mettre des # si on veut que python adapte la taille de la figure dans la vidéo
ax.set_xlim([-x_min, x_max])
ax.set_ylim([-y_min, y_max])
ax.set_aspect(1)

astre_1 = plt.Circle((x_10, y_10), 0.1, color='Black', zorder=5)
astre_2 = plt.Circle((x_20, y_20), 0.1, color='Black', zorder=5)


#Résolution de l'équation du mvt

t = np.linspace(t0, tf, nb_pts)

def eq_2_corps(M, t):
    x1, y1, dx1, dy1, x2, y2, dx2, dy2 = M
    d12 = ((x1 - x2)**2 + (y1 - y2)**2)**(1/2)
    dM = (dx1, dy1, -G*m_2*(x1 - x2)/d12**3, -G*m_2*(y1 - y2)/d12**3, dx2, dy2, -G*m_1*(x2 - x1)/d12**3, -G*m_1*(y2 - y1)/d12**3)
    return dM

sol = odeint(eq_2_corps, [x_10, y_10, dx_10, dy_10, x_20, y_20, dx_20, dy_20], t)

x_1f, y_1f, x_2f, y_2f = sol[:,0], sol[:,1], sol[:,4], sol[:,5]


#Enlever les # si on veut tracer les courbes solutions

#plt.plot(x_1f, y_1f, color='Blue')
#plt.plot(x_2f, y_2f, color='Blue')

astre_1.center = x_1f[etat], y_1f[etat]
astre_2.center = x_2f[etat], y_2f[etat]

ax.add_patch(astre_1)
ax.add_patch(astre_2)

plt.show()


#Animation

def init():
    astre_1.center = x_10, y_10
    astre_2.center = x_20, y_20
    ax.add_patch(astre_1)
    ax.add_patch(astre_2)
    return astre_1, astre_2

def animate(i):
    astre_1.center = x_1f[i], y_1f[i]
    astre_2.center = x_2f[i], y_2f[i]
    ax.add_patch(astre_1)
    ax.add_patch(astre_2)
    return astre_1, astre_2

ani = animation.FuncAnimation(fig, animate, init_func=init, frames=nb_pts, blit=False, interval=40)
ani.save('Probleme_2_corps.mp4', fps=60)
plt.show()
