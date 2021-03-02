#On importe les modules nécessaires

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation



# Constantes

L = 1           #Longueur de la corde         
c = 1           #Célérité de l'onde
y_zero_n = 1    #Amplitude initiale
modes_list = [1, 2, 3, 5, 7, 10, 15]    #Liste des modes propres
amplitudes_list = [0.2, 0.2, 0.2, 0.2, 0.2 ,0.2, 0.2]     #Liste des amplitudes associées à chaque mode
t_0 = 0         #Instant initial pour l'animation
time_factor = 0.005
coef_amortissement = 0


#Création figure

fig, ax = plt.subplots()
graphe, = plt.plot([], [])

x = np.linspace(0, 1, 1000)



#Calcul des modes propres

def modepropre(t, mode):
    y = np.exp(-coef_amortissement*t) * y_zero_n * np.sin((mode*np.pi)/L*c*t) * np.sin((mode*np.pi)/L*x)
    return y


def modepropre_somme(t):
    #Calcule et renvoie la somme des modes propres de la liste modes_list
    #Returns: list
    
    y_sum = modepropre(t, 0)
    for n in range(len(modes_list)):
        y_sum += modepropre(t, modes_list[n]) * amplitudes_list[n]
    return y_sum
    
    
    
#Animation

def init():
    #Limites des axes
    ax.set_xlim(0, 1)
    ax.set_ylim(-2, 2)
    
    #Initialisation de l'animation à l'instant t_0
    y = modepropre_somme(t_0)
    graphe.set_data(x, y)
    return graphe


def animate(i):
    
    y = modepropre_somme(t_0 + time_factor*i)
    graphe.set_data(x, y)
    return graphe
    

#Voir la documentation de matplotlib.animation pour plus d'info sur la fonction animation
ani = animation.FuncAnimation(fig, animate, init_func=init, frames=1000, blit=False, interval=40)      
ani.save(mode_.mp4', fps = 60)
plt.close()
