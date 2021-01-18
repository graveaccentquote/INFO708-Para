# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 09:15:22 2020

@author: C Ost
"""

from multiprocessing import Process, Queue
from SystemSimulation import startSimulation
from ventilateur import ventilateur
from pompe import pompe
from commande import commande

if __name__ == '__main__':
    
    #seuils
    seuil_H2O_haut = 10.0
    seuil_H2O_bas = 0.0
    seuil_CO = 5.0
    seuil_CH4 = 5.0
    
    #sim variables
    max_iterations = 50    
    
    
    #queues
    waterpump_channel = Queue()
    gasfan_channel = Queue()
    activ_pompe = Queue()
    desactiv_pompe = Queue()
    activ_ventil = Queue()
    desactiv_ventil = Queue()
    
    niveau_H2O = Queue()
    niveau_CO = Queue()
    niveau_CH4 = Queue()
    alerte_H2O_haut = Queue()
    alerte_H2O_bas = Queue() 
    alerte_gas_bas = Queue()
    
  
    simProcess = Process(target=startSimulation,
                         args=(niveau_CH4,
                               niveau_CO,
                               niveau_H2O,
                               waterpump_channel,
                               gasfan_channel,
                               max_iterations))
    
    fanProcess = Process(target=ventilateur,
                         args=(activ_ventil,
                               desactiv_ventil, 
                               gasfan_channel, 
                               False, 
                               0.01,))
    
    pumpProcess = Process(target=pompe,
                          args=(activ_pompe,
                                desactiv_pompe,
                                waterpump_channel,
                                False,
                                0.01,))
    
    commandProcess = Process(target=commande,
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
    
    simProcess.start()
    fanProcess.start()
    pumpProcess.start()
    commandProcess.start()