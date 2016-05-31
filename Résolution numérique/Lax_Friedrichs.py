# coding: utf8

import numpy as np
import pylab as plt
from matplotlib import animation

"""
Résolution numérique de l'équation aux dérivées partielles:
    du/dt + df(u)/dx = 0
    u(x,0) = u0(x)
"""

# Paramètres de la simulation numérique
xmax = 500
tmax = 20
Vmax = 25
Pmax = 0.25

# Pas d'intégration
Dt = 0.005
Dx = 0.005

# Nombre de points de calcul
Nx = int(xmax // Dx) + 1
Nt = int(tmax // Dt) + 1

# def f(u):
#     """ Fonction f(u) de l'équation différentielle """
#     return u**2/2

def f(u):
    """ Fonction f(u) de l'équation différentielle """
    if u < 0.01:
        return 24*u
    else:
        return Pmax - u

def initialisation():
    """ Renvoie u0 la condition initiale du problème """
    t = gaussienne()
    # return 1-2*t/Pmax
    return t

def bord(T, t):
    """ Conditions aux bords pour x=0 et x=xmax au temps d'intégration t """
    T[0, t] = 1
    T[-1, t] = 1
    return T


# Création de différentes fonctions u0 initales
def choc():
    """ Répartition constante égale à 1 puis nulle """
    t = np.zeros(Nx)
    for x in range(0, Nx//2):
        t[x] = 1
    return t

sigma = 50
mu = 250
A = 40

def gaussienne():
    """ Répartition gaussienne """
    return np.array([np.exp(-(x*Dx-mu)**2/(2*sigma**2))/(sigma*2*np.pi) * A + 0.1 for x in range(0, Nx)])


# Fonctions permettant l'affichage des résultats et leur sauvegarde
def afficher(T):
    """ Affichage simple de u(x, t) au temps t en fonction de x """
    X = np.arange(0, Nx) * Dx
    plt.plot(T, X)
    plt.show()

def afficher_2D(T):
    """ Affichage d'un graphique 2D permettant de visualiser l'évolution de u(x,t) en fonction du temps """
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    plt.imshow(T, origin='lower', interpolation='nearest', cmap=plt.cm.afmhot, aspect='auto', extent=[0, tmax, 0, xmax])
    plt.colorbar()
    plt.xlabel("Temps (s)")
    plt.ylabel("Position x (m)")
    plt.show()

def resolution():
    T = np.zeros((Nx, Nt))
    u0 = initialisation()

    T[:,0] = u0

    for t in range(0, Nt-1):
        T = bord(T, t+1)
        for x in range(1, Nx-1):
            T[x, t+1] = 0.5*(T[x+1, t] + T[x-1, t]) - Dt*(f(T[x+1, t]) - f(T[x-1, t]))/(2*Dx)

    # T = Pmax*(1 - T)/2

    afficher_2D(T)

resolution()


# sigma = 50
# mu = 250
# A = 40
# cste = 0.1
# def f(x):
#     return np.exp(-(x-mu)**2/(2*sigma**2))/(sigma*2*np.pi) * A + cste
#
# X = [x*Dx for x in range(0, Nx)]
# Y = [f(x) for x in X]
#
# plt.plot(X, Y)
# plt.xlim(0, xmax)
# # plt.ylim(0, 0.25)
# plt.show()