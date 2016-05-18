# coding: utf8

from Simulation import Simulation
from math import exp, pi, sin
import cProfile
from random import random

# Paramètres de la gaussienne
sigma = 100
mu = 500
A = 30
cste = 0.005
def gaussienne(x):
    return exp(-(x-mu)**2/(2*sigma**2))/(sigma*2*pi) * A + cste

# Paramètres de la réparition aléatoire
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
p = 1/200
def constante(x):
    return p

s = Simulation.Simulation(300, 1/20.0)
s.route.ajouter_section(1000, 25)

s.route.ajout_indices_analyse([0, 5])

resultat = s.initialisation(gaussienne, affichage=False)
if resultat:
    # s.analyse = True
    # s.route.desactiver_flux_densite()
    s.route.boucle = True
    s.sauvegarde = False
    # s.animation = True

    # cProfile.run('s.lancer()')
    s.lancer()

# for l in range(50, 100, 5):
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