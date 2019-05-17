import numpy as np
import pandas as pd


class NanFiller(object):

    def __init__(self, dataframe: pd.DataFrame):

        self.__df = dataframe

        self.__datecol = self.__df['Date']
        self.__SI_col = np.array(self.__df['Solar Index'])

        self.__nanlist = []
        self.__search_nan()
        self.__backfill()

        self.__interp = self.__find_interp_boundaries()
        self.__fillnan()
        self.__df['F107'] = self.__SI_col
        self.__dropsolarindx()

    def return_dataframe(self):
        return self.__df

    def return_data(self):
        return self.__SI_col

    def return_nanlist(self):
        return self.__nanlist

    def __row_isna_check(self, row):
        return pd.isna(row[1]['Solar Index'])

    def __search_nan(self):

        self.__nanlist = list(np.argwhere(np.isnan(self.__SI_col)))

    def __dropsolarindx(self):
        return self.__df.drop('Solar Index', axis=1, inplace=True)

    def __backfill(self):

        fill = 260.4
        for i in range(44):
            self.__SI_col[i] = fill
            self.__nanlist.pop(0)

    def __find_interp_boundaries(self):

        def ordercheck(lst, idx):
            return lst[idx] == (lst[idx+1] - 1)

        ranges = []

        first = None
        last = None

        size = len(self.__nanlist)

        for idx, i in enumerate(np.array(self.__nanlist[:-1], dtype=int)):

            if first is None and last is None:

                first = int(i)
                last = int(i)

            if ordercheck(self.__nanlist, idx):
                last = int(self.__nanlist[idx+1])

            else:
                ranges.append([first, last])
                first = None
                last = None

        ranges.append([23741, 23741]) # Sorry for shitty code

        return ranges

    @staticmethod
    def __setup_line(xrange, yrange):

        return lambda x: (yrange[1] - yrange[0])/(xrange[1]-xrange[0])*(x - xrange[0]) + yrange[0]



    def __fillnan(self):

        for xrange in self.__interp:
            x0 = xrange[0]-1
            x1 = xrange[1]+1

            y0 = self.__SI_col[x0]
            y1 = self.__SI_col[x1]

            line = self.__setup_line((x0, x1), (y0, y1))

            for x in range(x0, x1+1):
                y_i = line(x)

                self.__SI_col[x] = y_i


