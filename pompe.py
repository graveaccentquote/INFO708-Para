# -*- coding: utf-8 -*-

from multiprocessing import Process

from time import sleep

def pompe(activ_pompe, desactiv_pompe, waterpump_channel, etat, sleepTime):
    
    while activ_pompe.empty() and desactiv_pompe.empty():
        sleep(sleepTime)
        
    if not activ_pompe.empty():
        activ_pompe.get()
        waterpump_channel.put(True)
        proc = Process(target=pompe,
                       args=(activ_pompe,
                             desactiv_pompe,
                             waterpump_channel,
                             True,
                             sleepTime,))
        
    elif not desactiv_pompe.empty():
        desactiv_pompe.get()
        waterpump_channel.put(False)
        proc = Process(target=pompe,
                       args=(activ_pompe,
                             desactiv_pompe,
                             waterpump_channel,
                             False,
                             sleepTime,))
    proc.start()
        
        
        

