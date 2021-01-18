# -*- coding: utf-8 -*-
import numpy.random

from time import sleep

from colorama import init, Fore, Back, Style

def startSimulation(CH4_sensor_channel,
                    CO_sensor_channel,
                    H2O_sensor_channel,
                    waterpump_channel,
                    gasfan_channel,
                    timeout):
    
    sim = SystemSimultion(CH4_sensor_channel,
                          CO_sensor_channel,
                          H2O_sensor_channel,
                          waterpump_channel,
                          gasfan_channel)
    
    init() #for colorama
    
    for i in range(0, timeout):
        print("Iteration "+ str(i))
        sim.update()
        sleep(0.25)
        
class SystemSimultion(object):

    #simulation variables
    AVERAGE_H2O_DECREASE = 4.0
    AVERAGE_H2O_INCREASE = 3.0
    H2O_STD = 0.5
    AVERAGE_GAS_DECREASE = 2.0
    AVERAGE_GAS_INCREASE = 1.0
    GAS_STD = 0.33
    
    def __init__(self,
                 CH4_sensor_channel,
                 CO_sensor_channel,
                 H2O_sensor_channel,
                 waterpump_channel,
                 gasfan_channel):
        self.H2O_level = float(0)
        self.CH4_level = float(0)
        self.CO_level = float(0)
        self.waterPumpRunning = False
        self.gasFanRunning = False

        self.CH4_sensor_channel = CH4_sensor_channel
        self.CO_sensor_channel = CO_sensor_channel
        self.H2O_sensor_channel = H2O_sensor_channel
        self.waterpump_channel = waterpump_channel
        self.gasfan_channel = gasfan_channel

    def update(self):
        #send updated values to other processes
        self.sendH2OValue()
        self.sendCOValue()
        self.sendCH4Value()
        
        #receive messages
        self.recvFanValue()
        self.recvPumpValue()
        
        #update internal values and print
        self.debug()
        self.updateInternalValues()

    def updateInternalValues(self):
        #water update
        if not(self.waterPumpRunning):
            self.H2O_level += numpy.random.normal(self.AVERAGE_H2O_INCREASE, self.H2O_STD)
        else:
            self.H2O_level -= numpy.random.normal(self.AVERAGE_H2O_DECREASE, self.H2O_STD) 
            
        #gas update
        if not(self.gasFanRunning):
            self.CH4_level += numpy.random.normal(self.AVERAGE_GAS_INCREASE, self.GAS_STD)
            self.CO_level  += numpy.random.normal(self.AVERAGE_GAS_INCREASE, self.GAS_STD) 
        else:
            self.CH4_level -= numpy.random.normal(self.AVERAGE_GAS_DECREASE, self.GAS_STD)
            self.CO_level  -= numpy.random.normal(self.AVERAGE_GAS_DECREASE, self.GAS_STD)
            
            
        self.H2O_level = max(0, self.H2O_level)
        self.CH4_level = max(0, self.CH4_level)
        self.CO_level = max(0, self.CO_level)


    def debug(self):
        #watch out with console prints and parallel processes, might lead to 
        #access conflicts
        #in this application, only SystemSimulation prints stuff in the console
        
        if self.waterPumpRunning:
            print(Fore.RED + Back.LIGHTBLACK_EX, end='')
        if self.gasFanRunning:
            print(Back.BLACK, end='')
        
        print("#################################################")
        print("Pump running : "+str(self.waterPumpRunning))
        print("Fan running : "+str(self.gasFanRunning))
        print("WATER level : "+str(self.H2O_level))
        print("CO level : "+str(self.CO_level))
        print("CH4 level : "+str(self.CH4_level))
        print(Style.RESET_ALL, end='')   
        
        
        
    def sendH2OValue(self):
        self.H2O_sensor_channel.put(self.H2O_level)
    
    def sendCH4Value(self):
        if not self.CH4_sensor_channel.empty():
            self.CH4_sensor_channel.get()
        self.CH4_sensor_channel.put(self.CH4_level)
    
    def sendCOValue(self):
        if not self.CO_sensor_channel.empty():
            self.CO_sensor_channel.get()
        self.CO_sensor_channel.put(self.CO_level)
        
    def recvFanValue(self):
        if not self.gasfan_channel.empty():
            msg = self.gasfan_channel.get()
            self.gasFanRunning = msg
        
    def recvPumpValue(self):
        if not self.waterpump_channel.empty():
            msg = self.waterpump_channel.get()
            self.waterPumpRunning = msg;
    
    