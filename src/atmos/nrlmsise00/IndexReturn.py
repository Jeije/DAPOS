from src.atmos.nrlmsise00.misc_func import monthtodoy

import numpy as np
import pandas as pd
import os
import datetime as dt

#This class returns the solar and geomagnetic indices at any given day

class Indexer(object):

    def __init__(self, date: dt.datetime):
        self.__date = date

        self.__AP_filepath = r'\\'.join(os.getcwd().split('\\')[:-3]) + '\\data\\nrlmsise00_dataprocessed\\nlrmsise00_AP_processed.txt'
        self.__F107_filepath = r'\\'.join(os.getcwd().split('\\')[:-3]) + '\\data\\nrlmsise00_dataprocessed\\nlrmsise00_f107datapros.txt'

        self.__apdf = self.__loadcsv(self.__AP_filepath)
        self.__f107df = self.__loadcsv(self.__F107_filepath)

        self.__aplastdf = self.__valuefinder(self.__apdf, self.__date.year, self.__date.month, self.__date.day)
        self.__f107df = self.__valuefinder(self.__f107df, self.__date.year, self.__date.month, self.__date.day - 1)

        self.__f107 = self.__interpl(np.array(self.__f107df['F107']),24*60*60,60*60*self.__date.hour+60*self.__date.minute+self.__date.second)
        self.__f107a = self.__interpl(np.array(self.__f107df['F107A']), 24*60*60, 60*60*self.__date.hour+60*self.__date.minute+self.__date.second)

        self.__ap_daily = np.array(self.__aplastdf['ap_daily'])[0]
        self.__ap1 = np.array(self.__aplastdf['ap1'])[0]
        self.__ap2 = np.array(self.__aplastdf['ap2'])[0]
        self.__ap3 = np.array(self.__aplastdf['ap3'])[0]
        self.__ap4 = np.array(self.__aplastdf['ap4'])[0]
        self.__apavg1 = np.array(self.__aplastdf['apavg1'])[0]
        self.__apavg2 = np.array(self.__aplastdf['apavg2'])[0]


    def return_indices(self):
        return np.array([self.__date.isoformat(' '),self.__f107,self.__f107a,self.__ap_daily,self.__ap1,self.__ap2,self.__ap3,self.__ap4,self.__apavg1,self.__apavg2])

    def __monthtodoy(self,year:int, month:int, day:int):
        return monthtodoy(year,month,day)

    def __loadcsv(self, filepath: str):
        return pd.read_csv(filepath)

    def __valuefinder(self, dataframe: pd.DataFrame, year:int, month:int, day:int):
        indices1 = dataframe[dataframe.date == dt.date(year,month,day).isoformat()]
        indices2 = dataframe[dataframe.date == dt.date(year,month,day+1).isoformat()]
        indices = pd.concat([indices1,indices2])
        print(indices)


        return indices

    def __interpl(self, data:np.array, dt:int, sec:int):
        return data[0]+sec*(data[1]-data[0])/dt


if __name__ == "__main__":
    date = dt.datetime(2013,2,3,12,0,0)
    ut = 12*60*60+0*60+0
    a = Indexer(date).return_indices()

