# coding: utf8

from Simulation.Voiture import Voiture
from pylab import *
from matplotlib import animation
from datetime import *
import pickle
import os


class Route(object):

    def __init__(self, longueur, vitesse_limite, delta):
        """
        Initialisation de la classe Voiture
        :param longueur: longueur de la route en mètres
        :param vitesse_limite: vitesse maximale autorisée sur la route en mètres par seconde
        :param delta: pas de temps d'intégration de la simulation
        """
        self.longueur = longueur
        self.vitesse_limite = vitesse_limite
        self.delta = delta
        self.temps_total = 0
        self.indice = 0

        self.voitures_valides = [] # Liste contenant les voitures valides uniquement
        self.voitures = [] # Liste contenant toutes les voitures
        self.N_tot = 0 # Nombre de voitures total sur la route
        self.N = 0 # Nombre de voitures valides sur la route

        """ Tableau de données """
        self.flux = []
        self.densite = []
        self.flux_total = []
        self.densite_totale = []

        # Permet de ne pas enregistrer (et donc calculer) les flux et/ou densités sur la route
        self.flux_active = True
        self.densite_active = True

        self.pas = 50  # Pas de distance pour le calcul du flux et de la densité

        """
        Liste contenant les données relatives aux sections de la route,
        selon le format suivant: [position_debut, longueur, vitesse_limite, temps_securite]
        """
        self.sections = []

    def preparation(self, espacement, vitesse):
        """
        Permet d'initialiser toutes les valeurs de la classe Route à leur valeur par defaut,
        et lance la génération du trafic routier initial (t=0)
        :param espacement: distance entre deux voitures (float)
        :param vitesse: vitesse initiale des voitures (float)
        """
        self.voitures_valides = []
        self.voitures = []
        self.N_tot = 0
        self.N = 0
        self.flux = []
        self.densite = []
        self.flux_total = []
        self.densite_totale = []
        self.flux_active = True
        self.densite_active = True
        self.temps_total = 0

        self.generer_trafic(espacement, vitesse)

    def ajouter_section(self, longueur, vitesse_limite, temps_securite, indice=0):
        """
        Ajoute une section à la liste des sections dèjà existantes
        :param longueur: longueur en mètre
        :param vitesse_limite: vitesse maximale autorisée sur la route en mètres par seconde
        :param temps_securite: temps de sécurité avec la voiture de devant
        :param indice: emplacement de la section dans la route, par défaut au début de la route
        """
        self.sections.insert(indice, [0, longueur, vitesse_limite, temps_securite])
        self.organisation_sections()

    def affichage_section(self):
        """
        Affichage des sections sous forme de tableau avec alignement automatique
        """
        S = ["Numéro", "Position", "Longueur", "Vitesse maximale", "Temps de sécurité"]

        # Affichage de la liste S avec alignement
        ligne = " "
        for s in S:
            ligne += s + " | "
        print(ligne)

        # Affichage des sections avec alignement
        n = 0
        for section in self.sections:
            l = (len(S[0]) + 2 - len(str(n)))/2
            if int(l) == l:
                l = int(l)
                ligne = " " * l + str(n) + " " * l + "|"
            else:
                l = int(l)
                ligne = " " * l + str(n) + " " * (l+1) + "|"
            n += 1
            i = 1
            for a in section:
                s = S[i]
                i += 1
                l = (len(s) + 2 - len(str(a)))/2
                if int(l) == l:
                    l = int(l)
                    ligne += " " * l + str(a) + " " * l + "|"
                else:
                    l = int(l)
                    ligne += " " * l + str(a) + " " * (l+1) + "|"

            print(ligne)

    def organisation_sections(self):
        """
        Réorganisation des sections en ajustant leur position de départ
        """
        self.longueur = self.sections[0][1]  # Longueur de la route
        if len(self.sections) > 1:  # Il faut au moins 2 sections
            for i in range(1, len(self.sections)):
                # Ajuste le début des sections selon: position en i = position en i-1 + longueur de i-1
                self.sections[i][0] = self.sections[i-1][0] + self.sections[i-1][1]
                self.longueur += self.sections[i][1]  # Mise à jour de la longueur de la route

    def numero_section(self, position):
        """
        Renvoie l'indice de la section traversée par la voiture pour une position donnée à l'intérieur de la route
        """
        if position <= self.longueur:  # On vérifie que la voiture est dans la route
            for section in self.sections:
                position -= section[1]
                if position <= 0:  # La voiture se situe alors dans la section
                    return self.sections.index(section)
        else:
            return 0

    def desactiver_flux(self):
        if self.temps_total == 0:  # Uniquement au début de la simulation
            self.flux_active = False

    def desactiver_densite(self):
        if self.temps_total == 0:  # Uniquement au début de la simulation
            self.densite_active = False

    def generer_trafic(self, distance, vitesse):
        """
        Génération du trafic routier initial
        :param distance: distance entre deux voitures (float)
        :param vitesse: vitesse initiale des voitures (float)
        """
        p = self.longueur
        while p >= 0:
            section = self.numero_section(p)
            self.ajouter_voiture(p, self.sections[section][2])
            p -= distance

    def update(self, delta, temps_total, indice):
        """
        Mise à jour de la route et de chaque voiture
        :param delta: pas de temps d'intégration de la simulation
        :param temps_total: temps total de la simulation
        :param indice: nombre de tours dans la boucle effectués
        """

        self.temps_total = temps_total # Sauvegarde du temps total de simulation
        self.indice = indice

        for voiture in self.voitures_valides:
            if voiture.valide:
                i = self.voitures_valides.index(voiture)
                if i != self.N-1: # Si la voiture n'est pas la première
                    voiture_devant = self.voitures_valides[i+1]
                else: # Si c'est la première voiture
                    if self.N >= 2: # S'il y a plus de 2 voitures alors la voiture de devant est la première
                        voiture_devant = self.voitures_valides[0]
                    else:
                        voiture_devant = None
                indice_section = self.numero_section(voiture.position)
                # Mise à jour de la voiture
                voiture.update(
                    temps_total,
                    delta,
                    indice,
                    voiture_devant,
                    self.longueur,
                    self.sections[indice_section][3],  # temps de sécurité
                    self.sections[indice_section][2]  # vitesse limite
                )

        # On retire les voitures invalides de la simulation
        for voiture in self.voitures_valides:
            if not voiture.valide:
                self.retirer_voiture(voiture)

        # Mise à jour du flux
        if self.flux_active:
            F = []
            for k in range(0, self.longueur, self.pas):  # On découpe la route en intervalle de longueur 'self.pas'
                v_totale = 0
                for voiture in self.voitures_valides:
                    if voiture.position <= k + self.pas and voiture.position >= k:
                        v_totale += voiture.vitesse
                F.append(v_totale / self.pas)

            self.flux.append([
                temps_total,
                F
            ])

        v = 0
        for voiture in self.voitures_valides:
            v += voiture.vitesse
        self.flux_total.append([
            temps_total,
            v / self.longueur
        ])

        # Mise à jour de la densité
        if self.densite_active:
            D = []
            for k in range(0, self.longueur, self.pas):
                N_totale = 0
                for voiture in self.voitures_valides:
                    if voiture.position <= k + self.pas and voiture.position >= k:
                        N_totale += 1
                D.append(N_totale / self.pas)

            self.densite.append([
                temps_total,
                D
            ])

        self.densite_totale.append([
            temps_total,
            self.N / self.longueur
        ])

    def ajouter_voiture(self, position, vitesse, index=0):
        """
        Ajoute une voiture dans la simulation
        :param position: position initiale en mètres
        :param vitesse: vitesse initiale en mètres par seconde
        :param index: emplacement de la voiture sur la route, par défaut derrière toutes les autres
        """
        voiture = Voiture(position, vitesse, self.delta, self.temps_total, self.indice)
        self.voitures_valides.insert(index, voiture)
        self.voitures.append(voiture)
        self.N += 1
        self.N_tot += 1

    def retirer_voiture(self, voiture):
        """
        Retire une voiture de la simulation
        :param voiture: objet Voiture à retirer
        """
        self.voitures_valides.remove(voiture)
        self.N -= 1

    """
    Début des fonctions pour l'affichage de graphiques,
    liste des graphiques disponibles:
        - flux en fonction de la position et du temps
        - densité en fonction de la position et du temps
        - flux en fonction de la densité (permet de générer la courbe caractéristique des différents régimes de trafic)
        - positions, vitesses, accélérations en fonction du temps pour un certain nombre de voitures
        - distance entre deux voitures en fonction du temps (permet de vérifier le respect des distances de sécurité)
        - animation qui permet d'observer la simulation une fois finie
    """

    def afficher_flux(self):
        Z = []
        X = []
        Y = [k for k in range(0, self.longueur + self.pas, self.pas)]
        for d in self.flux:
            X.append(d[0])
            Z.append(d[1])

        m = np.matrix(Z)

        pcolor(np.array(X), np.array(Y), np.array(m.T), cmap="afmhot")
        ylim(0, self.longueur)
        xlim(0, self.temps_total)
        show()

    def afficher_densite(self):
        Z = []
        X = []
        Y = [k for k in range(0, self.longueur + self.pas, self.pas)]
        for d in self.densite:
            X.append(d[0])
            Z.append(d[1])

        m = np.matrix(Z)

        pcolor(np.array(X), np.array(Y), np.array(m.T), cmap="afmhot")
        ylim(0, self.longueur)
        xlim(0, self.temps_total)
        show()

    def afficher_flux_densite(self):
        X = []
        Y = []

        for d in self.flux_total:
            Y.append(d[1])
        for d in self.densite_totale:
            X.append(d[1])

        hist2d(np.array(X), np.array(Y), cmap="afmhot", bins=60)
        # plot(X, Y, 'bo')
        xlim(0, max(X)*1.2)
        ylim(0, max(Y)*1.2)
        show()

    def afficher_position(self, indice):
        try:
            voiture = self.voitures[indice]
        except:
            print("Erreur ! Impossible de récupérer la voiture d'indice " + str(indice))
            return None
        X, Y = voiture.obtenir_positions()
        plot(Y, X)

    def afficher_vitesse(self, indice):
        try:
            voiture = self.voitures[indice]
        except:
            print("Erreur ! Impossible de récupérer la voiture d'indice " + str(indice))
            return None
        X, Y = voiture.obtenir_vitesses()
        plot(X, Y)

    def afficher_acceleration(self, indice):
        try:
            voiture = self.voitures[indice]
        except:
            print("Erreur ! Impossible de récupérer la voiture d'indice " + str(indice))
            return None
        X, Y = voiture.obtenir_acceleration()
        plot(X, Y)

    def afficher_distance(self, i1, i2):
        try:
            voiture1 = self.voitures[i1]
            voiture2 = self.voitures[i2]
        except:
            print("Erreur ! Impossible de récupérer les voitures d'indices " + str(i1) + " et " + str(i2))
            return None
        X, Y1 = voiture1.obtenir_positions()
        X, Y2 = voiture2.obtenir_positions()
        Y = []
        D = []
        for i in range(len(Y1)):
            Y.append(Y2[i] - Y1[i])
            D.append(self.distance_securite)
        plot(X, Y, label="Distance entre les voitures " + str(i1) + " et " + str(i2))

    def afficher(self, xmin, xmax, ymin, ymax):
        xlim(xmin, xmax)
        ylim(ymin, ymax)
        legend(loc="best")
        show()

    def analyse_voitures(self, nombre=-1):
        if nombre <= 0:
            nombre = self.N_tot
        print("Analyse des positions...")
        for i in range(nombre):
            self.afficher_position(i)
        self.afficher(0, self.longueur, 0, self.temps_total)

        print("Analyse des vitesses...")
        for i in range(nombre):
            self.afficher_vitesse(i)
        self.afficher(0, self.temps_total, 0, 40)

        print("Analyse des accélérations...")
        for i in range(nombre):
            self.afficher_acceleration(i)
        self.afficher(0, self.temps_total, -30, 30)

    def analyse_trafic(self):
        print("Analyse du flux...")
        if self.flux_active:
            self.afficher_flux()

        print("Analyse de la densité...")
        if self.densite_active:
            self.afficher_densite()

        print("Génération de la courbe flux-densité...")
        self.afficher_flux_densite()

    def animation(self):

        positions = []
        for voiture in self.voitures:
            positions.append(voiture.obtenir_positions(temps=False))

        fig = figure()
        data, = plot([], [], 'bo')
        xlim(0, self.longueur)
        ylim(0, 1)
        N = round(self.temps_total / self.delta)

        def update(k):
            X = []
            Y = []
            for voiture in positions:
                try:
                    i = voiture[0].index(k)
                    position = voiture[1][i]
                    X.append(position)
                    Y.append(0.5)
                except:
                    pass
            data.set_data(X, Y)
            title("Temps : " + str(round(self.delta * k)) + "s")
            return data

        animation.FuncAnimation(fig, update, frames=N, interval=self.delta/1000, repeat=False)
        legend()
        show()

    def sauvegarde(self):
        """
        Permet de sauvegarder dans un fichier les données de la simulation dans le dossier 'Données',
        dans le but de les afficher simultanément via le fichier 'Analyse.py'
        """
        d = datetime.now()
        nom_fichier = str(d.day) + "-" + str(d.month) + "-" + str(d.year) + "_" + str(d.hour) + str(d.minute) + str(d.second) + str(d.microsecond)
        print("Sauvegarde dans le fichier : Données/" + nom_fichier)

        with open(os.getcwd() + "/Données/" + nom_fichier, 'wb') as fichier:
            p = pickle.Pickler(fichier)
            """ Enregistrement des données de la simualation """
            # Paramètres de la simulation
            p.dump([
                self.temps_total,
                self.delta,
                self.longueur
            ])

            p.dump(self.flux_total)
            p.dump(self.densite_totale)
