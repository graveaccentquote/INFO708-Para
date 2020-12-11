import numpy.random

class SystemSimultion(object):

    #static variables
    AVERAGE_H2O_DECREASE = float(5)
    AVERAGE_H2O_INCREASE = float(2)
    H2O_STD = float(1)
    AVERAGE_GAS_DECREASE = float(5)
    AVERAGE_GAS_INCREASE = float(2)
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


    def debug(self):
        print("WATER level : "+str(self.H2O_level)+"\n")
        print("CO level : "+str(self.CO_level)+"\n")
        print("CH4 level : "+str(self.CH4_level)+"\n")
            


def system_simulation(CH4_channel_out, CO_channel_out, H20_channel_out, waterpump_channel_in, fan_channel_in) :
    
    print()
    