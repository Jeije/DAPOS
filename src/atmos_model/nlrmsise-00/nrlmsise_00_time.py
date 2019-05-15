from calendar import monthrange
import numpy as np

def monthtodoy(year:int,month:int,day:int):
    tot_days=0
    for x in range(1,month):
        nb_days = monthrange(year, x)[1]
        tot_days+=nb_days
    return tot_days+day

def lin_spline(xy1:np.array,xy2:np.array,doy:int,ut:int):
    dt = 24*60*60*(xy2[0]-xy1[0])
    df107 = (xy2[1]-xy1[1])/dt
    f107 = xy1[1]+df107*(((doy-xy1[0])*24*60*60)+ut)
    return f107

def lin_splinelst(xy1:np.array,xy2:np.array):
    print(xy2[0])
    if (int(xy2[0])-int(xy1[0])) > 1:
        dt = 24 * 60 * 60 * (xy2[0] - xy1[0])
        df107 = (xy2[1] - xy1[1]) / dt
        f107_lst = []
        doy_range = xy2[0]-xy1[0]
        for x in range(1,doy_range):
            f107 = xy1[1] + df107 * x*(24 * 60 * 60)
            f107_lst.append(f107)
        return np.array(f107_lst)
    else:
        print('Invalid Input')
        return


# def f107a(f07_lst:np.array):
#     for x in f07_lst:



if __name__ == '__main__':
    xy1 = np.array([189,100])
    xy2 = np.array([194,200])
    a = lin_splinelst(xy1,xy2)
    print(a)