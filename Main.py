# coding: utf8

from Simulation import Simulation


s = Simulation.Simulation(60, 1/30.0)

s.route.ajouter_section(1000, 25)
s.route.affichage_section()

s.initialisation(1000)
s.lancer()

# for p in range(10, 1500, 50):
#     s.initialisation(p, 0)
#     s.lancer()
