'''Importing Required Modules from Folder'''
from src.orbit.SatGroundTrack.GroundTrack import GroundTrackCalc
from src.atmos.nrlmsise00.IndexFindr.IndexReturn import Indexer
from src.atmos.nrlmsise00.AtmosCalc import nrl00,nrl00_cond

'''Importing Required Modules'''
import time
import os
import numpy as np
import datetime as dt
import pandas as pd
from astropy import units as u
import matplotlib.pyplot as plt


'''Class OrbitAtmosCalc1Day'''
'''Calculates the Atmospheric Conditions across 1 day '''
'''
* INPUT 1: Discretization Step per Orbit (keep above 100)
* INPUT 2: Date for which Orbits will be Calculated
* INPUT 3: Inclination of Orbit
* INPUT 4: Orbital Altitude 
* INPUT 5: Initial Latitude of Satellite
* INPUT 6: Initial Longitude of Satellite

* PARAM 1: plot, set True if orbit ground track plot is required

* OUTPUT 1: Dataframe structure containing the calculated orbit data in columns:
['time [s]','Lat [deg]','Lon [deg]','V_rel [m/s]','V [rad/s]','Azimuth [deg]'] 
for each discretization step along the requested orbit
'''

class OrbitAtmosCalc1Day(object):
    def __init__(self, t:int=400, date: dt.datetime= dt.datetime(2008, 6, 2), inc:float = 94.7 * u.deg, h:float= 206 * u.km,
                 lat0: float = 12.77*u.deg, longi0: float = -91.37*u.deg):

        self.__date = date
        self.__inc = inc.to(u.deg)
        self.__h = h.to(u.km)
        self.__lat0 = lat0.to(u.deg)
        self.__longi0 = longi0.to(u.deg)
        self.__pos = GroundTrackCalc(dt = t, inc = self.__inc, h = self.__h, lat0 = self.__lat0,
                                     longi0=self.__longi0, n=0).return_data()

        self.__vals = np.zeros([len(self.__pos),20])
        self.__pros = np.zeros([3,11])

        self.__indices = Indexer(self.__date).return_indices()[1:]

        for idx,i in enumerate(range(len(self.__pos))):
            if idx%1 == 20:
                self.__indices = Indexer(self.__date).return_indices()[1:]

            self.__data = nrl00(date=self.__date,h=self.__h ,lat = self.__pos['Lat [deg]'][i]*u.deg, lon = self.__pos['Lon [deg]'][i]*u.deg,
                                indices = self.__indices)
            self.__date = date + dt.timedelta(0, self.__pos['time [s]'][i])
            self.__vals[i][0] = self.__date.year
            self.__vals[i][1] = self.__date.month
            self.__vals[i][2] = self.__date.day
            self.__vals[i][3] = self.__date.hour
            self.__vals[i][4] = self.__date.minute
            self.__vals[i][5] = self.__date.second
            self.__vals[i][6] = self.__pos['Lat [deg]'][i]
            self.__vals[i][7] = self.__pos['Lon [deg]'][i]
            self.__vals[i][8] = self.__pos['V_rel [m/s]'][i]
            self.__vals[i][9:18]=self.__data.d
            self.__vals[i][18:20]=self.__data.t

        self.data_df()
        self.save_csv(self.__df)
        self.avgcalc()

    def return_vals(self):
        return self.__df

    def return_pros(self):
        return self.__pros

    def return_indices(self):
        return self.__indices

    def data_df(self):
        self.__df = pd.DataFrame(self.__vals)
        self.__df.columns = ['Year','Month','Day','Hour','Minute','Second','Lat','Long','V_rel',
                                 'He','O','N2','O2','Ar','Density','H','N','Anomalous Oxygen','Exospheric Temp','Temp']

    def pros_df(self):
        self.__df = pd.DataFrame(self.__pros)
        self.__df.columns = ['He','O','N2','O2','Ar','Density','H','N','Anomalous Oxygen','Exospheric Temp','Temp']

    def save_csv(self,dataframe: pd.DataFrame, filepath: str = r'\\'.join(os.getcwd().split('\\')[:-2]) +
                                                          '\\data\\atmosorbitdata\\'):
        '''Function save_csv'''
        '''PARAM 1: Pandas DataFrame containing processed AP data'''
        '''PARAM 2: Filepath to save processed AP data'''
        filepath = filepath + str(self.__inc.value) + ',' + str(self.__h.value) + ',' + str(self.__lat0.value) + ',' \
                   + str(self.__longi0.value) + ',' + str(self.__indices[0]) + ',' + str(self.__indices[1]) + ',' + \
                   str(self.__indices[2]) + '.csv'
        dataframe.to_csv(filepath)

    def avgcalc(self):
        row_num = self.__vals.shape[1]
        for i in range(9,row_num):
            avg = np.average(self.__vals[:, i])
            min = np.amin(self.__vals[:, i])
            max = np.amax(self.__vals[:, i])
            self.__pros[:, i-9] = np.array([avg, min, max])

if __name__ == "__main__":
    a = OrbitAtmosCalc1Day()
    b = a.return_vals()
    c = a.return_pros()
    d = a.return_indices()
    plt.plot(b['Hour']*60*60+b['Minute']*60+b['Second'],b['Density'], label = 'h = 206 km' + ', F10.7 =' + str(round(d[0],1))
                                                                              + ', F10.7A = ' +str(round(d[1],2))
                                                                              + ', AP Daily = ' + str(round(d[2],2)))
    plt.plot(np.average(np.array(b['Density'])))
    print(np.average(np.array(b['Density'])))
    plt.xlim(0,max(b['Hour']*60*60+b['Minute']*60+b['Second']))
    plt.xlabel('Time [s]')
    plt.ylabel('Density [kg/m^3]')
    plt.legend(loc = 'upper left')
    plt.show()
    print(time.process_time())
