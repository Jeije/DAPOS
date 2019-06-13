'''Importing Required Modules'''
import numpy as np
import pandas as pd
import os
import datetime as dt

'''Finds Solar and Geo-Magnetic Indices for Desired Date from Processed Solar and AP txt files'''

class Indexer(object):

    def __init__(self, date: dt.datetime):
        '''Class Indexer'''
        '''INPUT 1: Date at which required Solar and AP Indices must be evaluated
        Date is a datetime class such that date = dt.datetime(2010,1,20,12,30,0) corresponds
        to 2010/01/20 - 12:30:00'''

        '''To return indices call function .return_indices'''
        '''OUT 1: Solar & AP Indices in the form: [F107,F107A,AP_Daily,AP1,AP2,AP3,AP4,APAVG1,APAVG2]'''

        '''Verification: Check Output of Class Indexer against Matlab Add-On: 
        https://nl.mathworks.com/matlabcentral/fileexchange/35054-f10-7-solar-flux-ap-indices'''
        
        self.__date = date

        self.__AP_filepath = \
            '\\'.join(os.path.dirname(os.path.abspath(__file__)).split('\\')[:-4]) \
            + '\\data\\nrlmsise00_dataprocessed\\nrlmsise00_AP_processed.txt'
        self.__F107_filepath = \
            '\\'.join(os.path.dirname(os.path.abspath(__file__)).split('\\')[:-4]) \
            + '\\data\\nrlmsise00_dataprocessed\\nrlmsise00_f107datapros.txt'

        self.__apdf = self.__loadcsv(self.__AP_filepath)
        self.__f107df = self.__loadcsv(self.__F107_filepath)

        self.__aplastdf = self.__valuefinderap(self.__apdf, self.__date.year, self.__date.month, self.__date.day)
        self.return_datalst()
        self.__f107df = self.__valuefindersolar(self.__f107df, self.__date.year, self.__date.month, self.__date.day - 1)

        self.__f107 = self.__interpl(np.array(self.__f107df['F107']),24*60*60,60*60*self.__date.hour+
                                     60*self.__date.minute+self.__date.second)
        self.__f107a = self.__interpl(np.array(self.__f107df['F107A']),24*60*60,60*60*self.__date.hour+
                                      60*self.__date.minute+self.__date.second)

        dt3h = int((60*60*self.__date.hour+60*self.__date.minute+self.__date.second)/(3*60*60))
        
        self.__ap_daily = float(self.__aplastdf['ap_daily'])
        self.__ap1 = float(self.__aplastdf['ap'+str(20+dt3h)])
        self.__ap2 = float(self.__aplastdf['ap'+str(19+dt3h)])
        self.__ap3 = float(self.__aplastdf['ap'+str(18+dt3h)])
        self.__ap4 = float(self.__aplastdf['ap'+str(17+dt3h)])
        self.__apavg1 = np.mean(self.__aplastdf.to_numpy()[0][11+dt3h:18+dt3h])
        self.__apavg2 = np.mean(self.__aplastdf.to_numpy()[0][3+dt3h:10+dt3h])

    def return_datalst(self):
        return self.__aplastdf.to_numpy()

    def return_indices(self):
        return [self.__date.isoformat(' '),self.__f107,self.__f107a,self.__ap_daily,self.__ap1,self.__ap2,
                         self.__ap3,self.__ap4,self.__apavg1,self.__apavg2]

    def __loadcsv(self, filepath: str):
        return pd.read_csv(filepath)

    def __valuefindersolar(self, dataframe: pd.DataFrame, year:int, month:int, day:int):
        indices1 = dataframe[dataframe.date == dt.date(year,month,day).isoformat()]
        indices2 = dataframe[dataframe.date == dt.date(year,month,day+1).isoformat()]
        return pd.concat([indices1,indices2])

    def __valuefinderap(self, dataframe: pd.DataFrame, year:int, month:int, day:int):
        return dataframe[dataframe.date == dt.date(year,month,day).isoformat()]

    def __interpl(self, data:np.array, dt:int, sec:int):
        return data[0]+sec*(data[1]-data[0])/dt

if __name__ == "__main__":
    '''Check Indices for 2013/02/03 - 23:00:00'''
    date = dt.datetime(2013,2,10,15,0,0)

    '''Useful Values for Code Verification against Matlab Script'''
    doy = (date-dt.datetime(date.year,1,1,date.hour,date.minute,date.second)).days+1
    ut = date.hour*60*60+date.minute*60+date.second

    '''Return Indices for Requested Date'''
    a = Indexer(date).return_indices()

