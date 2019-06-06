from src.atmos.nrlmsise00.misc_func import monthtodoy

import numpy as np
import pandas as pd

#This class returns the solar and geomagnetic indices at any given day

class Indexer(object):

    def __init__(self, year: int = 1994, month: int = 1, day: int = 10, sec: int = 0, doy = False):
        self.__AP_filepath = r'C:\Users\mauro\OneDrive\AE Bachelor - TU Delft\Year 3\DSE - Local\DAPOS_Main\src\atmos\nlrmsise00_data\nlrmsise00_AP_processed.txt'
        self.__F107_filepath = r'C:\Users\mauro\OneDrive\AE Bachelor - TU Delft\Year 3\DSE - Local\DAPOS_Main\src\atmos\nlrmsise00_data\nlrmsise00_f107datapros.txt'

        self.__apdf = self.__loadcsv(self.__AP_filepath)
        self.__f107df = self.__loadcsv(self.__F107_filepath)

        if doy == False:
            self.__doy = self.__monthtodoy(year,month,day)
        elif doy == True:
            self.__doy = month
        else:
            print('Invalid Inputs')
            print('Inputs: Year, Month, Day, sec')
            exit(0)


        self.__aplastdf = self.__valuefinder(self.__apdf, year, self.__doy)
        self.__f107df = self.__valuefinder(self.__f107df, year, self.__doy - 1)

        self.__f107 = self.__interpl(np.array(self.__f107df['F107']),24*60*60,sec)
        self.__f107a = self.__interpl(np.array(self.__f107df['F107A']), 24 * 60 * 60, sec)
        self.__ap_daily = np.array(self.__aplastdf['ap_daily'])[0]
        self.__ap1 = np.array(self.__aplastdf['ap1'])[0]
        self.__ap2 = np.array(self.__aplastdf['ap2'])[0]
        self.__ap3 = np.array(self.__aplastdf['ap3'])[0]
        self.__ap4 = np.array(self.__aplastdf['ap4'])[0]
        self.__apavg1 = np.array(self.__aplastdf['apavg1'])[0]
        self.__apavg2 = np.array(self.__aplastdf['apavg2'])[0]


    def return_indices(self):
        return np.array([self.__f107,self.__f107a,self.__ap_daily,self.__ap1,self.__ap2,self.__ap3,self.__ap4,self.__apavg1,self.__apavg2])

    def __monthtodoy(self,year:int, month:int, day:int):
        return monthtodoy(year,month,day)

    def __loadcsv(self, filepath: str):
        return pd.read_csv(filepath)

    def __valuefinder(self, dataframe: pd.DataFrame, year:int, doy:int):
        indices1 = dataframe[dataframe.date == int(str(year)+str(doy))]
        indices2 = dataframe[dataframe.date == int(str(year)+str(doy+1))]
        indices = pd.concat([indices1,indices2])
        return indices

    def __interpl(self, data:np.array, dt:int, sec:int):
        return data[0]+sec*(data[1]-data[0])/dt


if __name__ == "__main__":
    a = Indexer().return_indices()

