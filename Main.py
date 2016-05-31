# coding: utf8

from Simulation import Simulation
from math import exp, pi, sin
import cProfile
from random import random

# Paramètres de la gaussienne
sigma = 100
mu = 700
A = 30
cste = 0.01
def gaussienne(x):
    return exp(-(x-mu)**2/(2*sigma**2))/(sigma*2*pi) * A + cste

# Paramètres de la répartition aléatoire
l = 1000
nb = int(random())*20 + 30
f0 = 1/(2*l)
f, a, phi = [f0], [1], [0]
for k in range(1, nb):
   f.append((k+1) * f0)
   a.append(random()*((k+1)//2)/5)
   phi.append(random()*2*pi)

def alea(x):
   return 0.008*abs(sum((a[i]*sin(2*pi*f[i]*x + phi[i]) for i in range(0, nb))))

# Paramètres pour le feux rouges
position = 1000
p = 0.07
def feux_rouges(x):
    if x <= position:
        return p
    else:
        return 0

# Paramètres pour la répartition constante
p = 0.2
def constante(x):
    return p

s = Simulation.Simulation(3000, 1/20.0)
s.route.ajouter_section(1400, 25)

s.route.ajout_indices_analyse([0])

resultat = s.initialisation(gaussienne, affichage=True)
if resultat:
    # s.analyse = True
    s.route.desactiver_flux_densite()
    s.route.boucle = True
    s.sauvegarde = False
    # s.animation = True

    # cProfile.run('s.lancer()')
    s.lancer()

# for l in range(4, 20, 1):
#     s = Simulation.Simulation(300, 1/20.0)
#     s.route.ajouter_section(1000, 25)
#
#     def constante(x):
#         return 1/l
#
#     s.initialisation(constante, affichage=False)
#     s.analyse = True
#     s.route.boucle = True
#     s.lancer()

# for l in range(20, 250, 5):
#     s = Simulation.Simulation(150, 1/20.0)
#     s.route.ajouter_section(1000, 25)
#
#     def constante(x):
#         return 1/l
#
#     s.initialisation(constante, affichage=False)
#     s.analyse = True
#     s.route.boucle = True
#     s.lancer()