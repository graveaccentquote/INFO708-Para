# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 09:15:22 2020

@author: C Ost
"""

from multiprocessing import Process, Queue, Pipe
from SystemSimulation import *
from testing import *

if __name__ == '__main__':
    info('main line')
    
    ###Hello world
    # p = Process(target=f, args=('world',))
    # p.start()
    # p.join()
    
    ### Queue
    # q = Queue()
    # p = Process(target=f2, args=(q,))
    # p.start()
    # print (q.get())
    # p.join()

    ### Pipe
    # parent_conn, child_conn = Pipe()
    # p = Process(target=f3, args=(child_conn,))
    # p.start()
    # parent_conn.send("toto")
    # #print (parent_conn.recv()) 
    # p.join()

    sim = SystemSimultion(0, 0, 0, 0, 0)

    for i in range(1,50):
        print(i)
        sim.update()
        sim.debug()