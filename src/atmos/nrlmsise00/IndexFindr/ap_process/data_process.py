import datetime as dt

class ApDataPros(object):

    def __init__(self, data: list, yearlst: list):

        self.__data = data
        self.__yearlst = yearlst

        self.__apdata= []

        self.__apdaily()

        # self.__apappend()

    def return_apdata(self):
        return self.__apdata


    def return_aprow(self,idx1:int,idx2:int):
        return self.__aprow(idx1,idx2)

    def return_aplst(self,idx1:int,idx2:int):
        return self.__appros(self.return_aprow(idx1,idx2))

    def return_ap(self,idx1:int,idx2:int):
        return self.__apcalc(self.return_aplst(idx1,idx2))


    def __apdaily(self):

        for idx1, i in enumerate(self.__data):

            for idx2, x in enumerate(i):

                if x[56] == ' ' and x[57] == ' ' and type(int(x[58])) == int:
                    apdaily = int(x[58:59] + x[60:62]) / 1000

                elif x[56] == ' ' and type(int(x[57])) == int:
                    apdaily = int(x[57:59] + x[60:62]) / 1000

                else:
                    apdaily = int(x[56:59] + x[60:62]) / 1000

                ap = [(dt.date(int(self.__yearlst[idx1]),1,1)+dt.timedelta(idx2)).isoformat(), apdaily] + self.return_ap(idx1,idx2+1)
                self.__apdata.append(ap)



    def __aprow(self,idx1:int,idx2:int):
        aplastraw = []
        p = 4

        if idx2 < 4:

            if idx1 == 0:
                while p:
                    if idx2-p<0:
                        aplastraw.append([self.__data[idx1][0]])
                        p = p - 1
                    else:
                        aplastraw.append([self.__data[idx1][idx2-p]])
                        p = p - 1
                return aplastraw

            while p:
                if idx2-p < 0:
                    aplastraw.append([self.__data[idx1-1][idx2-p]])
                    p = p - 1
                else:
                    aplastraw.append([self.__data[idx1][idx2-p]])
                    p = p - 1
        else:
            while p:
                aplastraw.append([self.__data[idx1][idx2-p]])
                p=p-1
        return aplastraw


    def __appros(self,aplastraw:list):
        ap = []

        for s in aplastraw:

            for i in s:
                pos = [32,35,38,41,44,47,50,53]

                for x in pos:

                    if i[x] == ' ' and i[x+1] == ' ':
                        ap.append(0)

                    if i[x] == ' ' and type(int(i[x+1])) == int:
                        ap.append(int(i[x+1]))

                    else:
                        ap.append(int(i[x]+i[x+1]))
        return ap


    def __apcalc(self,ap:list):
        return ap[5:32]

