# -*- coding: utf-8 -*-

from multiprocessing import Process

def detectionH2OBas(niveau_H2O,
                     alerte_H2O_bas,
                     seuil_H2O_bas):
          
    msg = niveau_H2O.get()
    if msg <= seuil_H2O_bas:
        alerte_H2O_bas.put("alert")
    else:
        proc = Process(target=detectionH2OBas,
                              args=(niveau_H2O,
                                    alerte_H2O_bas,
                                    seuil_H2O_bas,))
        
        proc.start()
    
