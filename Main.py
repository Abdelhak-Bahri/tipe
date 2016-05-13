# coding: utf8

from Simulation import Simulation
from math import exp, pi
import cProfile

# Paramètres de la gaussienne
sigma = 100
mu = 500
A = 30
cste = 0.01
def gaussienne(x):
    return exp(-(x-mu)**2/(2*sigma**2))/(sigma*2*pi) * A + cste

# Paramètres pour le feux rouges
position = 1000
p = 0.07
def feux_rouges(x):
    if x <= position:
        return p
    else:
        return 0

# Paramètres pour la répartition constante
p = 0.006
def constante(x):
    return p

s = Simulation.Simulation(60, 1/20.0)
s.route.ajouter_section(1000, 25)

# s.route.ajout_indices_analyse([0, 1])

resultat = s.initialisation(gaussienne, affichage=True)
if resultat:
    # s.analyse = True
    s.route.desactiver_flux_densite()
    s.route.boucle = True
    s.sauvegarde = False
    s.animation = True

    # cProfile.run('s.lancer()')
    s.lancer()
