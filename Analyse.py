# coding: utf8

import pickle
import os
from pylab import *

"""
Analyse du flux et de la densité des différentes simulations à partir des résultats stockés dans le dossier 'Données'
"""

X, Y = [], []

fichiers = os.listdir(os.getcwd() + "/Simulation/Données/")
if fichiers != []:
    for nom_fichier in fichiers:
        with open(os.getcwd() + "/Simulation/Données/" + nom_fichier, 'rb') as fichier:
            p = pickle.Unpickler(fichier)
            params = p.load()
            print(params)

            flux_total = p.load()
            densite_totale = p.load()

            # On ajoute uniquement la dernière donnée celle qui correspond à un regime stationnaire
            Y.append(flux_total[len(flux_total)-1][1])
            X.append(densite_totale[len(densite_totale)-1][1])

    hist2d(np.array(X), np.array(Y), cmap="afmhot", bins=60)
    # plot(X, Y, 'bo')
    xlim(0, max(X)*1.2)
    ylim(0, max(Y)*1.2)
    show()
else:
    print("Aucune donnée à traiter !")
