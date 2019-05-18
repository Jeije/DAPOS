import pandas as pd
import  numpy as np

from os import listdir
from os.path import isfile, join


class DataImport(object):

    def __init__(self, path: str = r'C:\Users\mauro\OneDrive\AE Bachelor - TU Delft\Year 3\DSE - Local\DAPOS_Main\src\atmos\nlrmsise-00_data\AP_Indices'):

        self.__pathfile = path

        self.__yearlst = [f for f in listdir(path) if isfile(join(path, f))]
        self.__pathlst = list(self.__yearlst)

        self.__data = []
        self.__apdata= []

        self.__pathgenerator()

        self.__genapdata()

        self.__import()

        self.__apdaily()

        print(self.__apdata)



        #self.__parse()

    def return_data(self):
        return self.__data

    def return_apdata(self):
        return self.__apdata

    def __pathgenerator(self):

        for idx, file in enumerate(self.__pathlst):
            self.__pathlst[idx] = self.__pathfile + f"\\{file}"

    def __import(self):

        for idx, file in enumerate(self.__pathlst):

            with open(file, 'r') as datafile:
                lines = datafile.readlines()
            self.__data.append(lines)

    def __genapdata(self):
        for idx1,i in enumerate(self.__yearlst):
            self.__apdata.append([self.__yearlst[idx1],0])

    def __apdaily(self):

        for idx1,i in enumerate(self.__data):
            apdata = []

            for idx2, x in enumerate(i):

                if x[56] == ' ' and x[57] == ' ' and int(x[58]) == int:
                    apdaily = int(x[58:59]+x[60:62]) / 1000

                elif x[56] == ' ' and int(x[57]) == int:
                    apdaily = int(x[57:59]+x[60:62]) / 1000

                else:
                    apdaily = int(x[56:59]+x[60:62]) / 1000

                apdata.append(apdaily)
            self.__apdata[idx1][1] = apdata



    @staticmethod
    def __stringsplitter(string: str):

        result = ''
        for char in string[8:]:
            if char == " " or char == '\n':
                continue
            else:
                result += char

        return result

    def __parse(self):

        size = len(self.__data)

        dates = []
        solar_index = []

        for row in self.__data:
            length = len(row)
            dates.append(row[:8])

            if length == 9 or ' .' in row:
                solar_index.append(None)

            else:
                solar_index.append(float(self.__stringsplitter(row)))

        data = {
            'Date': dates,
            'Solar Index': solar_index
        }
        self.__data = pd.DataFrame.from_dict(data)
        # self.__data.set_index([i for i in range(size)])



if __name__ == "__main__":

    DI = DataImport()

    a = DI.return_data()
    b =DI.return_apdata()