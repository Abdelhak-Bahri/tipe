# coding: utf8

from Modele import Modele


class Voiture(object):

    def __init__(self, position, vitesse, delta, temps_total, indice):
        """
        Initialisation de la classe Voituresimulation
        :param position: position initiale en mètres
        :param vitesse: vitesse initiale en mètres par seconde
        :param delta: pas de temps de la simulation
        :param temps_total: temps total de la simulation
        :param indice: nombre de tours dans la boucle effectués
        """

        self.donnees = []  # Tableau contenant les données enregistrées lors de la simulation
        self.position = position
        self.position_totale = position  # Position sur la route sans le retour à l'origine lors d'une boucle
        self.vitesse = vitesse
        self.longueur = 4  # Longueur en mètre de la voiture
        self.a_max = 20  # Accélération maximale en m/s²
        self.a_min = 20  # Décélération maximale en m/s²
        self.valide = True  # Booléen pour savoir si la voiture doit être prise en compte dans la simulation
        self.temps_reaction = 2  # Temps de réaction commun aux conducteurs en secondes
        # Création du modèle pour la gestion de l'accélération
        self.modele = Modele(self.a_max, self.a_min, self.temps_reaction, self.longueur)

        # Création de données pour les positions et les vitesses pour le temps de réaction
        indice_decalage = round(self.temps_reaction / delta)
        for i in range(indice_decalage):
            self.donnees.append([
                temps_total + delta * i - delta * indice_decalage,
                [
                    self.position,
                    self.position_totale,
                    self.vitesse,
                    0
                ],
                indice + i - indice_decalage
            ])

    def update(self, temps_total, delta, indice, voiture_devant, longueur, vitesse_limite, boucle=True):
        """
        Mise à jour de la voiture
        :param temps_total: temps total de la simulation
        :param delta: pas de temps d'intégration
        :param indice: nombre de tours dans la boucle effectués
        :param voiture_devant: objet Voiture, voiture qui la précède
        :param longueur: longueur de la route
        :param vitesse_limite: vitesse maximale autorisée sur la section
        :param boucle: booleén qui indique si la route boucle sur elle même
        """

        if self.position >= longueur:
            if boucle:
                self.position -= longueur
            else:
                self.valide = False
                return None

        # Influence de la voiture de devant
        if voiture_devant is not None:
            """ Intégration du temps de réaction """
            # L'indice de décalage représente le décalage dans la prise d'information du conducteur
            # Ainsi, on récupère les données de la voiture de devant en prenant en compte ce décalage
            indice_decalage = indice - round(self.temps_reaction / delta)

            # Récupération des données de la voiture de devant
            v = voiture_devant.obtenir_vitesse(indice_decalage)
            d = voiture_devant.obtenir_position_totale(indice_decalage)
            # nombre_boucle_voiture_devant = voiture_devant.obtenir_nombre_boucle()

            # Distance relative
            if d <= self.position_totale:
                distance = longueur + d - self.position_totale
            else:
                distance = d - self.position_totale

            if distance <= 0:  # erreur liée au temps de réaction ou à un dépassement non souhaité dans la simulation
                distance = 0

        else:
            distance = 1000000
            v = 100000

        # Calcul de l'accélération appliquée par le conducteur
        a = self.modele.calcul_acceleration(v, self.vitesse, distance, vitesse_limite)

        # On limite l'accélération
        a = min(a, self.a_max)
        a = max(a, -self.a_min)

        # Intégration d'Euler
        self.vitesse += a * delta
        if self.vitesse < 0:  # Impossible de reculer
            self.vitesse = 0
        self.position += self.vitesse * delta

        # Enregistrement des données
        self.donnees.append([
            temps_total,
            [
                self.position,
                self.position_totale,
                self.vitesse,
                a
            ],
            indice
        ])

    def obtenir_positions(self, temps=True):
        """
        :param temps: booléen qui permet de choisir entre temps ou indice
        :return: une liste contenant les positions de la voiture en fonction du temps ou de l'indice
        """
        if temps:
            t = []
            r = []
            for d in self.donnees:
                t.append(d[0])
                r.append(d[1][0])
            return t, r
        else:
            i = []
            r = []
            for d in self.donnees:
                i.append(d[2])
                r.append(d[1][0])
            return i, r

    def obtenir_vitesse(self, i):
        """
        :param i: indice
        :return: la vitesse de la voiture à l'indice i
        """
        for d in self.donnees:
            if d[2] == i:
                return d[1][2]
        return None

    def obtenir_position(self, i):
        """
        :param i: indice
        :return: la position de la voiture à l'indice i
        """
        for d in self.donnees:
            if d[2] == i:
                return d[1][0]
        return None

    def obtenir_position_totale(self, i):
        """
        :param i: indice
        :return: la position de la voiture à l'indice i
        """
        for d in self.donnees:
            if d[2] == i:
                return d[1][1]
        return None

    def obtenir_vitesses(self):
        """
        :return: une liste contenant les vitesses de la voiture en fonction du temps
        """
        t = []
        r = []
        for d in self.donnees:
            t.append(d[0])
            r.append(d[1][2])
        return t, r

    def obtenir_acceleration(self):
        """
        :return: une liste contenant les accélérations de la voiture en fonction du temps
        """
        t = []
        r = []
        for d in self.donnees:
            t.append(d[0])
            r.append(d[1][3])
        return t, r
