from src.orbit.OrbitPosCalc import OrbitGroundTrack
from src.atmos.nrlmsise00.IndexReturn import Indexer
from src.atmos.nrlmsise00.denscalc import nlrmsise00

import matplotlib.pyplot as plt
import numpy as np

class OrbitAtmosCalc(object):
    def __init__(self, dt:int=300,year:int=2002, month:int=10, day:int=15 ,sec:int=300, h:float=200,doy = False):

        self.__indices = Indexer(year,month,day,sec).return_indices()

        if doy == True:
            self.__indices = Indexer(year,month,0,sec,doy=True).return_indices()

        self.__pos = OrbitGroundTrack(dt,np.array([6371000+h*1000,0.0,94.3,180,0,0])).return_df()

        self.__inputs = np.zeros([dt,13])
        self.__vals = np.zeros([dt,11])
        self.__pros = np.zeros([3,11])

        self.atmoscalc(dt,year,month,day,sec,self.__indices,self.__pos)
        self.avgcalc(self.__vals)


    def return_vals(self):
        return self.__vals

    def return_inputs(self):
        return self.__inputs

    def return_pros(self):
        return self.__pros

    def return_simon(self):
        for i in range(len(np.array(self.__pos['Lat [deg]']))):
            print(self.__vals[i][5],np.array(self.__pos['Lat [deg]'])[i],np.array(self.__pos['Lat [deg]'])[i])

    def atmoscalc(self,dt,year,month,day,sec,indices:np.array,pos:np.array):
        for i in range(dt):
            env = nlrmsise00(year,month,day,sec+np.array(pos['Time [s]'])[i],np.array(pos['Height [km]'])[i],np.array(pos['Lat [deg]'])[i],
                             np.array(pos['Lat [deg]'])[i],indices)
            self.__inputs[i][0]=year
            self.__inputs[i][1]=month
            self.__inputs[i][2]=day
            self.__inputs[i][3]=sec+np.array(pos['Time [s]'])[i]
            self.__inputs[i][4:13]=indices

            self.__vals[i][0:9]=env.d
            self.__vals[i][9:11]=env.t

    def avgcalc(self,vals:np.array):
        row_num = vals.shape[1]
        for i in range(row_num):
            avg = np.average(vals[:,i])
            min = np.amin(vals[:,i])
            max = np.amax(vals[:,i])
            self.__pros[:,i]=np.array([avg,min,max])

if __name__ == "__main__":
    a = OrbitAtmosCalc()
    b = a.return_vals()
    c = a.return_inputs()
    d = a.return_pros()
    e = a.return_simon()