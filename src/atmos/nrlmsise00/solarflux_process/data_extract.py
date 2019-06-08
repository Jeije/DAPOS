import pandas as pd
import os
import datetime as dt




class DataImport(object):

    def __init__(self, datafile: str = r'\\'.join(os.getcwd().split('\\')[:-4]) + '\\data\\nrlmsise00_data\\SolarFlux_Indices\\nlrmsise00_f107data.txt'):

        self.__datafile = datafile

        self.__data = None
        self.__import()
        self.__parse()

    def return_data(self):
        return self.__data

    def __import(self):

        with open(self.__datafile, 'r') as datafile:
            lines = datafile.readlines()

        self.__data = lines

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

        dates = []
        solar_index = []

        for row in self.__data:
            length = len(row)

            date = dt.date(int(row[:8][0:4]),int(row[:8][4:6]),int(row[:8][6:8])).isoformat()

            dates.append(date)

            if length == 9 or ' .' in row:
                solar_index.append(None)

            else:
                solar_index.append(float(self.__stringsplitter(row)))

        data = {
            'date': dates,
            'Solar Index': solar_index
        }
        self.__data = pd.DataFrame.from_dict(data)



if __name__ == "__main__":

    DI = DataImport()

    a = DI.return_data()