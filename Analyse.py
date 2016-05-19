# coding: utf8

import pickle
import os
from pylab import *

"""
Analyse du flux et de la densité des différentes simulations à partir des résultats stockés dans le dossier 'Données'
"""

F, D, V, S, P, H = [], [], [], [], [], []

fichiers = os.listdir(os.getcwd() + "/Données/")
l = len(fichiers)
if l > 0:
    c = 0
    for nom_fichier in fichiers:
        c += 1
        print(c/l*100, "%")
        with open(os.getcwd() + "/Données/" + nom_fichier, 'rb') as fichier:
            p = pickle.Unpickler(fichier)
            params = p.load()
            # print(params)

            # On ajoute uniquement la dernière donnée celle qui correspond à un regime stationnaire
            F.append(p.load())
            D.append(p.load())
            V.append(p.load())
            S.append(p.load())
            H.append(p.load())
            P.append(p.load())

    plot(D, F, 'bo')
    title("Diagramme fondamental")
    xlim(0, max(D) * 1.2,)
    ylim(0, max(F) * 1.2,)
    xlabel("$Density(m^-1)$")
    ylabel("$Flow(s^-1)$")
    legend()
    show()

    plot(S, V, 'bo')
    title("Diagramme fondamental")
    xlim(0, max(S) * 1.2)
    ylim(0, max(V) * 1.2)
    xlabel("$Spacing(m)$")
    ylabel("$Speed(m.s^-1)$")
    legend()
    show()

    plot(P, H, 'bo')
    title("Diagramme fondamental")
    xlim(0, 1.2)
    ylim(0, 20)
    xlabel("$Pace(s.m^-1)$")
    ylabel("$Headway(s)$")
    legend()
    show()

else:
    print("Aucune donnée à traiter !")
