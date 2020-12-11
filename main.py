# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 09:15:22 2020

@author: C Ost
"""

from multiprocessing import Process, Queue, Pipe
import os

def f(name):
    info('process')
    print ('hello', name)
    
def f2(arg):
    arg.put("This message brought to you by a queue ")
    
def f3(arg):
    #arg.send("This message brought to you via a 2-way pipe")
    print(arg.recv())
    arg.close()

def system_simulation(CH4_channel_out, CO_channel_out, H20_channel_out, waterpump_channel_in, fan_channel_in) :
    #TODO
    print()
    
    
def info(title):
    print (title)
    print ('module name:', __name__)
    if hasattr(os, 'getppid'):  # only available on Unix
        print ('parent process:', os.getppid())
    print ('process id:', os.getpid())

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
    parent_conn, child_conn = Pipe()
    p = Process(target=f3, args=(child_conn,))
    p.start()
    parent_conn.send("toto")
    #print (parent_conn.recv()) 
    p.join()