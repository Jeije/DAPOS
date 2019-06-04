from model.nrlmsise_00 import *
from misc_func import monthtodoy

import pandas as pd

AP_fiepath = r'C:\Users\mauro\OneDrive\AE Bachelor - TU Delft\Year 3\DSE - Local\DAPOS_Main\src\atmos\nlrmsise00_data\nlrmsise00_AP_processed.txt'
F107_filepath = r'C:\Users\mauro\OneDrive\AE Bachelor - TU Delft\Year 3\DSE - Local\DAPOS_Main\src\atmos\nlrmsise00_data\nlrmsise00_f107datapros.txt'

def loadcsv(filepath: str):
    return pd.read_csv(filepath)

# def getf107(year:int,doy:int):



def msise00(alt:float, year: int = 2010, month: int = 1, day: int = 1,sec: int=0):
    #Setting Up Input/Outputs
    output = [nrlmsise_output() for _ in range(2)]
    Input = [nrlmsise_input() for _ in range(2)]
    flags = nrlmsise_flags()

    #Setting Up Parameters
    #=1 for values in kg/m^3
    #=0 for values in g/cm^3
    flags.switches[0] = 1
    for i in range(1, 24):
        flags.switches[i]=1

    #Convert Date to Doy
    doy = monthtodoy(year,month,day)

    #State Inputs of NLRMSISE00
    Input[1].doy = doy
    Input[1].year = year
    Input[1].sec = sec
    Input[1].alt = alt
    Input[1].g_lat = 60
    Input[1].g_long = -70
    Input[1].lst = 16
    Input[1].f107A = 150
    Input[1].f107 = 150
    Input[1].ap = 4

    gtd7(Input[1], flags, output[1])

    return output[1].d[5]


if __name__ == "__main__":
    b = msise00(200)
    a = loadcsv(F107_filepath)

#gapminder_2002 = gapminder[gapminder.year == 2002]