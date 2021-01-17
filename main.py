# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 09:15:22 2020

@author: C Ost
"""

from multiprocessing import Process, Queue
from SystemSimulation import startSimulation
#from testing import *

if __name__ == '__main__':
    #queues
    CH4_sensor_channel_out = Queue()
    CO_sensor_channel_out = Queue()
    H2O_sensor_channel_out = Queue()
    waterpump_channel_in = Queue()
    gasfan_channel_in = Queue()
    
  
    simProcess = Process(target=startSimulation,
                         args=(CH4_sensor_channel_out,
                                 CO_sensor_channel_out,
                                 H2O_sensor_channel_out,
                                 waterpump_channel_in,
                                 gasfan_channel_in,
                                 20))
    
    
    simProcess.start()