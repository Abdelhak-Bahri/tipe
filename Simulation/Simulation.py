# coding: utf8

from Simulation.Route import Route


class Simulation(object):

    def __init__(self, temps, delta):
        """
        Initialisation de la classe Simulation
        :param temps: durée de la simulation en secondes
        :param delta: pas de temps de la simulation
        :return:
        """
        self.temps = temps
        self.delta = delta
        self.route = Route(3000, 36, self.delta)
        self.analyse = False  # Permet de ne pas afficher les graphiques et de sauvegarder automatiquement

    def initialisation(self, espacement):
        """
        Lance l'initialisation de la route
        :param espacement: distance entre deux voitures (float)
        """
        self.route.preparation(espacement)

    def parametres(self, flux, densite):
        """
        Permet de désactiver l'enregistrement du flux ou/et de la densité dans la simulation
        :param flux: booléen
        :param densite: booléen
        """
        if not flux:
            self.route.desactiver_flux()
        if not densite:
            self.route.desactiver_densite()

    def lancer(self):
        """
        Début de la simulation
        """

        if len(self.route.sections) == 0:  # Vérifie s'il y a au minimum une section dans la route
            print("Il faut au moins une section !")
            return None

        temps_total = 0
        p = 0  # Avancement de la simulation entre 0 et 1
        i = 0  # Sert à incrémenter la variable 'p'
        indice = 0  # Nombre de tours dans la boucle effectués

        while temps_total <= self.temps: # Boucle principale du programme
            self.route.update(self.delta, temps_total, indice)
            indice += 1
            temps_total += self.delta # Mise à jour du temps
            i += self.delta / self.temps
            if i >= 0.01: # On affiche l'avancement 'p'
                p += 0.01
                i -= 0.01
                print("Avancement de la simulation : " + str(round(p*100)) + "% (" + str(round(temps_total)) + "s de " + str(self.temps) + "s).")
        print("Fin de la simulation")

        if not self.analyse:
            """ Début des analyses """
            rep = input("Analyse de la simulation ? (o/n)")
            while rep == "o":
                self.route.analyse_voitures(nombre=1)
                self.route.animation()
                # self.route.analyse_trafic()
                rep = input("Analyse de la simulation ? (o/n)")
            """ Fin des analyses """

            """ Sauvegarde des données """
            rep = input("Sauvegarde ? (o/n)")
            if rep == "o":
                self.route.sauvegarde()
        else:
            self.route.sauvegarde()

        print("Arrêt de la simulation")
