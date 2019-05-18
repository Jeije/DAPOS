import pandas as pd


class DataImport(object):

    def __init__(self, datafile: str = r'C:\Users\mauro\OneDrive\AE Bachelor - TU Delft\Year 3\DSE - Local\DAPOS_Main\src\atmos_model\nlrmsise-00_data\nlrmsise-00_f107data.txt'):

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