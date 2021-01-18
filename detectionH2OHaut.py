# -*- coding: utf-8 -*-

from multiprocessing import Process

def detectionH2OHaut(niveau_H2O,
                     alerte_H2O_haut,
                     seuil_H2O_haut,
                     ):

    msg = niveau_H2O.get()
    if msg >= seuil_H2O_haut:
        alerte_H2O_haut.put("alert")
    else:
        proc = Process(target=detectionH2OHaut,
                       args=(niveau_H2O,
                             alerte_H2O_haut,
                             seuil_H2O_haut,))
        proc.start()
    
