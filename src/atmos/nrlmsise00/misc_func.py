from calendar import monthrange
import numpy as np

def monthtodoy(year:int,month:int,day:int):
    tot_days=0
    for x in range(1,month):
        nb_days = monthrange(year, x)[1]
        tot_days+=nb_days
    return tot_days+day

if __name__ == '__main__':
    print('test')