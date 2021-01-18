# -*- coding: utf-8 -*-

from multiprocessing import Process

from time import sleep

def ventilateur(activ_ventil, desactiv_ventil, gasfan_channel, etat, sleepTime):
    
    while activ_ventil.empty() and desactiv_ventil.empty():
        sleep(sleepTime)
    
    if not activ_ventil.empty():
        activ_ventil.get()
        gasfan_channel.put(True)
        proc = Process(target=ventilateur,
                       args=(activ_ventil,
                             desactiv_ventil,
                             gasfan_channel,
                             True,
                             sleepTime,))
        
    elif not desactiv_ventil.empty():
        desactiv_ventil.get()
        gasfan_channel.put(False)
        proc = Process(target=ventilateur,
                       args=(activ_ventil,
                             desactiv_ventil,
                             gasfan_channel,
                             False,
                             sleepTime,))
    proc.start()
        
        
        

