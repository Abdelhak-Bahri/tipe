# coding: utf8

from Route import *

class Simulation(object):

    def __init__(self):
        self.temps = 5*60.0 # Durée de la simulation en secondes
        self.delta = 1/5.0 # Intervalle de temps entre chaque calcul
        self.route = Route(3000, 36, self.delta)

    def initialisation(self, espacement, vitesse):
        self.route.initialisation(espacement, vitesse)

    def lancer(self):
        temps_total = 0
        p = 0 # Avancement de la simulation
        i = 0
        indice = 0 # Nombre de tours dans la boucle

        while temps_total <= self.temps: # Boucle principale du programme
            self.route.update(self.delta, temps_total, indice)
            indice += 1
            temps_total += self.delta
            i += self.delta / self.temps
            if i >= 0.01:
                p += 0.01
                i -= 0.01
                print("Avancement de la simulation : " + str(round(p*100)) + "%")
        print("Fin de la simulation")

        """ Lancement des analyses """
        # self.route.analyse_voitures(nombre=1)
        # self.route.animation()
        # self.route.analyse_trafic()
        """ Fin des analyses """

        # Sauvegarde des données
        self.route.sauvegarde()

        print("Arrêt de la simulation")

s = Simulation()

for p in range(10, 1500, 50):
    # a = 36/(1000 - 100)
    # v = a * p + (36 - a*(1000 + 100))/2
    # print(p, v)
    s.initialisation(p, 0)
    s.lancer()