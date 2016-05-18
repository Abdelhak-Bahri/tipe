# coding: utf8

from Simulation.Route import Route
from time import clock


class Simulation(object):

    """
    Présentation de la classe Simulation:
    Cette classe permet la gestion globale de la simulation: initialisation, mise à jour de la route et du temps
    """

    def __init__(self, temps, delta):
        """
        Initialisation de la classe Simulation
        :param temps: durée de la simulation en secondes
        :param delta: pas de temps de la simulation
        """
        self.temps = temps
        self.delta = delta
        self.route = Route(self.delta)
        self.analyse = False  # Permet de ne pas afficher les graphiques et de sauvegarder automatiquement
        self.sauvegarde = True  # Permet de ne pas effectuer de sauvegarde de la simulation
        self.animation = False  # Permet de créer un fichier vidéo de la simulation dans le dossier 'Animation/'

    def initialisation(self, fonction, affichage=True):
        """
        Lance l'initialisation de la route
        :param fonction: fonction python qui donne la densité du trafic en fonction de la position x
        :param affichage: booléen qui permet d'afficher et de confirmer la génération du trafic
        """
        return self.route.preparation(fonction, affichage)

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
        t_debut = clock()
        if len(self.route.sections) == 0:  # Vérifie s'il y a au minimum une section dans la route
            print("Il faut au moins une section !")
            return None

        temps_total = 0
        p = 0  # Avancement de la simulation entre 0 et 1
        i = 0  # Sert à incrémenter la variable 'p'
        indice = 0  # Nombre de tours dans la boucle effectués

        while temps_total <= self.temps:  # Boucle principale du programme
            self.route.update(self.delta, temps_total, indice)
            indice += 1
            temps_total += self.delta  # Mise à jour du temps
            i += self.delta / self.temps
            if i >= 0.1:  # On affiche l'avancement 'p'
                p += 0.1
                i -= 0.1
                print("Avancement de la simulation : " + str(round(p*100)) + "% (" + str(round(temps_total)) + "s de " + str(self.temps) + "s).")
        print("Fin de la simulation")
        print("Simulation réalisée en ", round(clock() - t_debut, 2), "secondes")

        if not self.analyse:
            """ Début des analyses """
            rep = input("Analyse de la simulation ? (o/n)")
            while rep == "o":
                self.route.analyse_voitures()
                self.route.analyse_trafic()
                rep = input("Analyse de la simulation ? (o/n)")
            """ Fin des analyses """

            """ Sauvegarde de l'animation """
            if self.animation:
                print("Génération de l'animation...")
                self.route.animation()

            """ Sauvegarde des données """
            if self.sauvegarde:
                rep = input("Sauvegarde ? (o/n)")
                if rep == "o":
                    self.route.sauvegarde()
        else:
            self.route.sauvegarde()

        print("Arrêt de la simulation")
