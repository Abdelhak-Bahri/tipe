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
p0 = 1/100
f = 1/500
a0 = random()
a1 = random()*1.5
a2 = random()*2
a3 = random()*2.8
def alea(x):
    return p0 * abs(1 + a0*sin(2*pi*f*x) + a1*sin(4*pi*f*x) + a2*sin(8*f*x) + a3*sin(16*f*x))


# Paramètres pour le feux rouges
position = 1000
p = 0.07
def feux_rouges(x):
    if x <= position:
        return p
    else:
        return 0

# Paramètres pour la répartition constante
p = 0.02
def constante(x):
    return p

s = Simulation.Simulation(250, 1/20.0)
s.route.ajouter_section(1000, 25)

s.route.ajout_indices_analyse([0])

resultat = s.initialisation(alea, affichage=True)
if resultat:
    # s.analyse = True
    s.route.desactiver_flux_densite()
    s.route.boucle = True
    s.sauvegarde = False
    s.animation = True

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