# -*- coding: utf-8 -*-

from multiprocessing import Process

from detectionH2OHaut import detectionH2OHaut
from detectionH2OBas import detectionH2OBas
from detectionGasBas import detectionGasBas

def commande(niveau_H2O,
             niveau_CO,
             niveau_CH4,
             alerte_H2O_haut,
             alerte_H2O_bas,
             alerte_gas_bas,
             seuil_H2O_haut,
             seuil_H2O_bas,
             seuil_CO,
             seuil_CH4,
             activ_pompe,
             desactiv_pompe,
             activ_ventil,
             desactiv_ventil):
    
    D_H2O_haut_proc = Process(target=detectionH2OHaut,
                              args=(niveau_H2O,
                                    alerte_H2O_haut,
                                    seuil_H2O_haut,))
    
    aux_Proc = Process(target=aux,
                       args=(alerte_gas_bas,
                             activ_pompe,
                             niveau_H2O, 
                             alerte_H2O_bas,
                             seuil_H2O_bas,))
    
    stopPump_proc = Process(target=stopPump,
                            args=(niveau_H2O,
                                  niveau_CO,
                                  niveau_CH4,
                                  alerte_H2O_haut,
                                  alerte_H2O_bas,
                                  alerte_gas_bas,
                                  seuil_H2O_haut,
                                  seuil_H2O_bas,
                                  seuil_CO,
                                  seuil_CH4,
                                  activ_pompe,
                                  desactiv_pompe,
                                  activ_ventil,
                                  desactiv_ventil,))
    
    D_H2O_haut_proc.start()
    stopPump_proc.start()
    
    alerte_H2O_haut.get()
    msg_CO = niveau_CO.get()
    msg_CH4 = niveau_CH4.get()
    if (msg_CO > seuil_CO) or (msg_CH4 > seuil_CH4):
        aux_Proc.start()
        activ_ventil.put("alert")   
        detectionGasBas(niveau_CO,
                        niveau_CH4,
                        alerte_gas_bas,
                        seuil_CO,
                        seuil_CH4)
    else:
        activ_pompe.put("alert")
        detectionH2OBas(niveau_H2O,
                        alerte_H2O_bas,
                        seuil_H2O_bas)
        
  
def aux(alerte_gas_bas,
        activ_pompe,
        niveau_H2O,
        alerte_H2O_bas,
        seuil_H2O_bas):
    alerte_gas_bas.get()
    activ_pompe.put("alert")
    detectionH2OBas(niveau_H2O,
                    alerte_H2O_bas,
                    seuil_H2O_bas)
    
def stopPump(niveau_H2O,
             niveau_CO,
             niveau_CH4,
             alerte_H2O_haut,
             alerte_H2O_bas,
             alerte_gas_bas,
             seuil_H2O_haut,
             seuil_H2O_bas,
             seuil_CO,
             seuil_CH4,
             activ_pompe,
             desactiv_pompe,
             activ_ventil,
             desactiv_ventil):
        
    alerte_H2O_bas.get()
    desactiv_pompe.put("alert")
    desactiv_ventil.put("alert")
    
    proc = Process(target=commande,
                   args=(niveau_H2O,
                         niveau_CO,
                         niveau_CH4,
                         alerte_H2O_haut,
                         alerte_H2O_bas,
                         alerte_gas_bas,
                         seuil_H2O_haut,
                         seuil_H2O_bas,
                         seuil_CO,
                         seuil_CH4,
                         activ_pompe,
                         desactiv_pompe,
                         activ_ventil,
                         desactiv_ventil,))
    
    proc.start()


    
    

