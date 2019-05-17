import numpy as np
import pandas as pd

class f107a_calc(object):
    def __init__(self,dataframe: pd.DataFrame):

        self.__df = dataframe
        self.__f107coll = np.array(self.__df['F107'])
        self.__df['F107A'] = np.zeros((len(self.__f107coll),1))
        self.calc_f107a()

    def return_dataframe(self):
        return self.__df

    def calc_f107a(self):

        for idx in range(len(self.__f107coll)):
            sm = 0
            a  = 40
            b = 40

            if idx < 40:
                a = idx

            if len(self.__f107coll)-idx-1 < 40:
                b = len(self.__f107coll)-idx-1

            for i in range(idx-a,idx+b+1):
                sm += self.__f107coll[i]
            self.__df.loc[idx,'F107A'] = sm/(a+b+1)




