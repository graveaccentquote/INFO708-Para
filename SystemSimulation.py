import numpy.random

from colorama import init, Fore, Back, Style

def startSimulation(CH4_sensor_channel_out,
                    CO_sensor_channel_out,
                    H2O_sensor_channel_out,
                    waterpump_channel_in,
                    gasfan_channel_in,
                    timeout):
    
    sim = SystemSimultion(CH4_sensor_channel_out,
                          CO_sensor_channel_out,
                          H2O_sensor_channel_out,
                          waterpump_channel_in,
                          gasfan_channel_in)
    
    init() #for colorama
    
    for i in range(0, timeout):
        print(i)
        sim.update()
        if i == 10:
            sim.waterpump_channel_in.put(True)
        if i == 15:
            sim.gasfan_channel_in.put(True)
        if i == 17:
            sim.gasfan_channel_in.put(False)
        
class SystemSimultion(object):

    #simulation variables
    AVERAGE_H2O_DECREASE = float(5)
    AVERAGE_H2O_INCREASE = float(2)
    H2O_STD = float(1)
    AVERAGE_GAS_DECREASE = float(3)
    AVERAGE_GAS_INCREASE = float(1)
    GAS_STD = float(1)
    
    def __init__(self,
                 CH4_sensor_channel_out,
                 CO_sensor_channel_out,
                 H2O_sensor_channel_out,
                 waterpump_channel_in,
                 gasfan_channel_in):
        self.H2O_level = float(0)
        self.CH4_level = float(0)
        self.CO_level = float(0)
        self.waterPumpRunning = False
        self.gasFanRunning = False

        self.CH4_sensor_channel_out = CH4_sensor_channel_out
        self.CO_sensor_channel_out = CO_sensor_channel_out
        self.H2O_sensor_channel_out = H2O_sensor_channel_out
        self.waterpump_channel_in = waterpump_channel_in
        self.gasfan_channel_in = gasfan_channel_in

    def update(self):
        #send updated values to other processes
        self.sendH2OValue()
        self.sendCH4Value()
        self.sendCOValue()
        
        #receive messages
        self.recvFanValue()
        self.recvPumpValue()
        
        #update internal values and print
        self.updateInternalValues()
        self.debug()

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
        self.H2O_sensor_channel_out.put(self.H2O_level)
    
    def sendCH4Value(self):
        self.CH4_sensor_channel_out.put(self.CH4_level)
    
    def sendCOValue(self):
        self.CO_sensor_channel_out.put(self.CO_level)
        
    def recvFanValue(self):
        if not self.gasfan_channel_in.empty():
            msg = self.gasfan_channel_in.get()
            self.gasFanRunning = msg
        
    def recvPumpValue(self):
        if not self.waterpump_channel_in.empty():
            msg = self.waterpump_channel_in.get()
            self.waterPumpRunning = msg;
    
    