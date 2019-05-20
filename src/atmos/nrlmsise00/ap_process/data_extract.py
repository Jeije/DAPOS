import pandas as pd
import numpy as np

from os import listdir
from os.path import isfile, join


class ApDataImport(object):

    def __init__(self, path: str = r'C:\Users\mauro\OneDrive\AE Bachelor - TU Delft\Year 3\DSE - Local\DAPOS_Main\src\atmos\nlrmsise00_data\AP_Indices'):

        self.__pathfile = path

        self.__yearlst = [f for f in listdir(path) if isfile(join(path, f))]
        self.__pathlst = list(self.__yearlst)

        self.__data = []

        self.__pathgenerator()
        self.__import()


    def return_data(self):
        return self.__data

    def return_yealst(self):
        return self.__yearlst


    def __pathgenerator(self):

        for idx, file in enumerate(self.__pathlst):

            self.__pathlst[idx] = self.__pathfile + f"\\{file}"


    def __import(self):

        for idx, file in enumerate(self.__pathlst):

            with open(file, 'r') as datafile:
                lines = datafile.readlines()

            self.__data.append(lines)


if __name__ == "__main__":

    DI = ApDataImport()
    a = DI.return_data()
    b = DI.return_yealst()