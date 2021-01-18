# -*- coding: utf-8 -*-

from multiprocessing import Process

def detectionGasBas(niveau_CO,
                    niveau_CH4,
                    alerte_gas_bas,
                    seuil_CO,
                    seuil_CH4):
        
    msg_CO = niveau_CO.get()
    msg_CH4 = niveau_CH4.get()
    
    if msg_CO <= seuil_CO and msg_CH4 <= seuil_CH4:
        alerte_gas_bas.put("alert")
    else:
        proc = Process(target=detectionGasBas,
                              args=(niveau_CO,
                                    niveau_CH4,
                                    alerte_gas_bas,
                                    seuil_CO,
                                    seuil_CH4,))
        
        proc.start()
    
