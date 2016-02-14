# coding: utf8

from pylab import *

"""
Présentation du modèle :
L'objectif de ce modèle est de déterminer l'accélération du véhicule en fonction des différents paramètres
qui lui sont accessibles: sa vitesse, la vitesse de la voiture de devant et la distance la séparant à cette dernière.

"""


class Modele(object):

    def __init__(self, a_max):
        """
        Initialisation des paramètres du modèle
        :param a_max: accélération maximale de la voiture
        """
        self.a_max = a_max

    def calcul_acceleration(self, v_j, v_i, distance, vitesse_limite, temps_securite, longueur):
        """
        :param v_j: la vitesse de la voiture de devant
        :param v_i: la vitesse de la voiture
        :param distance: la distance entre la voiture et celle de devant
        :param vitesse_limite: vitesse_maximale autorisée sur la section de route
        :param temps_securite: temps de sécurité à respecter
        :param longueur: longueur du véhicule
        :return: L'accélération du véhicule
        """
        delta_v = v_j - v_i  # Vitesse relative
        distance_securite = temps_securite * v_i + longueur  # Distance à respecter avec le véhicule de devant
        delta_x = distance_securite - distance
        v_j += 0.00001
        v_i += 0.00001
        vitesse_limite += 0.00001

        if delta_x < 0:
            vitesse_desiree = vitesse_limite
        else:
            vitesse_desiree = v_j
        if vitesse_desiree > vitesse_limite:
            vitesse_desiree = vitesse_limite
        n = self.a_max / vitesse_desiree

        return - n * v_i + n * v_j + (self.a_max - n * v_j) * (1 - exp(-delta_v/vitesse_limite)*exp(delta_x/longueur))
