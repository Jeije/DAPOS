import pandas as pd
import numpy as np
import os
from nrlmsise_00_time import monthtodoy, lin_splinelst, lin_spline

def new_data(data, dr_new:str):
    with open(dr_new, 'w') as f:
        for x in data:
            f.write(x)

def find_nan(f107_lst:np.array):
    nan_lst = []
    idx = 0
    size = len(f107_lst)
    while True:
        x = f107_lst[idx]
        if 'NaN' in x:
            idx_s = int(idx)
            idx_e = idx_s+1
            while True:
                if 'NaN' in f107_lst[idx_e]:
                    idx_e+=1
                else:
                    break
            nan_lst.append([idx_s,idx_e,f107_lst[idx_s-1],f107_lst[idx_e]])
            idx=idx_e+1
        elif idx+1 >= size:
            break
        else:
            idx+=1
            continue
    return np.array(nan_lst)

def repl_nan(nan_lst:np.array, doy_lst:np.array,f107_lst:np.array):
    idx = 0
    if doy_lst.size != f107_lst.size:
        return print('Incompatible Table Sizes')
    for x in nan_lst:
        if (x[1]-[0]) > 1:
            if x[0] != 0 and x[1] != doy_lst.size:
                xy1 = np.array([doy_lst[x[0]-1],int(f107_lst[x[0]-1] if '\n' not in f107_lst[x[0]-1] else f107_lst[x[0]-1][:-2])])
                xy2 = np.array([doy_lst[x[1]],int(f107_lst[x[1]] if '\n' not in f107_lst[x[1]] else f107_lst[x[1]][:-2])])
                lst = lin_splinelst(xy1,xy2)
                for x in range(lst):
                    f107_lst[idx+x]=lst[x]
    return f107_lst

def data_clean(dr:str,dr_new:str):
    year_lst = []
    doy_lst = []
    f107_lst = []
    with open(dr,'r') as f:
        data = f.readlines()
        data[-1] = data[-1]+'\n'
        idx = 0
        for x in data:
            if len(x) > 12 and x[12] == ' ':
                new = x[:8] + x[9:]
                data[idx] = new
            if len(x) > 12 and x[14] == ' ':
                new = x[:8]+'    NaN\n'
                data[idx] = new
            elif len(x) != 18:
                new = x[:8]+'    NaN\n'
                data[idx] = new
            idx += 1
        for x in data:
            x = x.split('    ')
            year = x[0][:4]
            doy = monthtodoy(int(year),int(x[0][4:6]),int(x[0][6:8]))
            f107 = x[1]
            year_lst.append(int(year))
            doy_lst.append(int(doy))
            f107_lst.append(f107)

            #new_data(data, dr_new)
        return np.array(year_lst),np.array(doy_lst),np.array(f107_lst)

if __name__ == '__main__':
    dr = r'C:\Users\mauro\OneDrive\AE Bachelor - TU Delft\Year 3\DSE - Local\DAPOS_Main'
    dr_old = dr+r'\src\atmos_model\nlrmsise-00_data\nlrmsise-00_f107data.txt'
    dr_new = dr+r'\src\atmos_model\nlrmsise-00_data\nlrmsise-00_f107dataclean.txt'
    a,b,c = data_clean(dr_old,dr_new)
    lst = find_nan(c)
    print(lst)
    ans = repl_nan(lst,b,c)


