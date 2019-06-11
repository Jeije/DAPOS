'''Importing Atmospheric Model from Folder'''
from src.atmos.nrlmsise00.model.nrlmsise_00 import nrlmsise_flags,nrlmsise_input,nrlmsise_output,ap_array,gtd7
from src.atmos.nrlmsise00.IndexFindr.IndexReturn import Indexer

'''Importing Required Modules'''
import time
import datetime as dt
from astropy import units as u

'''Calculate Atmsopheric conditions for given Inputs using NRLMSISE00 Atmospheric Model'''

'''
* INPUT 1: Date at which required output will be calculates
* Date is a datetime class such that date = dt.datetime(2010,1,20,12,30,0) corresponds
* to 2010/01/20 - 12:30:00
* INPUT 2: Height use *u.meters to indicate meters or u.km to indicate kilometers
* INPUT 3: Latitude use *u.deg to indicate degrees or u.rad to indicate radians
* INPUT 4: Longitude use *u.deg to indicate degrees or u.rad to indicate radians
* INPUT 5: NP Array Containing Solar Flux and AP Inidices
[F107,F107A,AP_DAILY,AP1,AP2,AP3,AP4,APAVG1,APAVG2]
'''

'''
* FLAGS:
aph=
True - AP array given in Input 5 is used
False - indicates that the AP Daily is used instead of AP Array to determine atmospheric Conditions, input 5 must
now be in the form [F107,F107A,AP_DAILY]
'''

'''
 *   OUTPUT VARIABLES:
 *      d[0] - HE NUMBER DENSITY(N/M-3)
 *      d[1] - O NUMBER DENSITY(N/M-3)
 *      d[2] - N2 NUMBER DENSITY(M-3)
 *      d[3] - O2 NUMBER DENSITY(M-3)
 *      d[4] - AR NUMBER DENSITY(M-3)                       
 *      d[5] - TOTAL MASS DENSITY(KG/M-3)
 *      d[6] - H NUMBER DENSITY(M-3)
 *      d[7] - N NUMBER DENSITY(M-3)
 *      d[8] - Anomalous oxygen NUMBER DENSITY(M-3)
 *      t[0] - EXOSPHERIC TEMPERATURE (K)
 *      t[1] - TEMPERATURE AT ALT (K)
 '''

def nrl00(date: dt.datetime=dt.datetime(2010,10,10,12,30,0), h: float = 190000*u.meter, lat: float=-70*u.deg,
               lon: float=100*u.deg, indices: list=[60,60,1,0,0,0,0,0,0], aph = True):
    '''Defining Outputs, Flag & Inputs of NLRMSISE00 Class'''
    output = [nrlmsise_output() for _ in range(2)]
    Input = [nrlmsise_input() for _ in range(2)]
    flags = nrlmsise_flags()

    '''Defining Flags'''
    '''If you want answers in g/cm^3 set flags.switches[0]=0'''
    for i in range(24):
        flags.switches[i]=1
    #flags.switches[0] = 0

    '''Creating AP Array'''
    '''
     * Array containing the following magnetic values:
     *   0 : daily AP
     *   1 : 3 hr AP index for current time
     *   2 : 3 hr AP index for 3 hrs before current time
     *   3 : 3 hr AP index for 6 hrs before current time
     *   4 : 3 hr AP index for 9 hrs before current time
     *   5 : Average of eight 3 hr AP indicies from 12 to 33 hrs 
     *           prior to current time
     *   6 : Average of eight 3 hr AP indicies from 36 to 57 hrs 
     *           prior to current time
    '''
    if aph == True:
         flags.switches[9] = -1
         aph = ap_array()
         for i in range(7):
             aph.a[i] = indices[i+2]


    '''Defining Inputs of Atmospheric Model and Converting Units if Necessary'''

    Input[1].doy = (date - dt.datetime(date.year, 1, 1, date.hour, date.minute, date.second)).days + 1
    Input[1].year = date.year  # /* without effect */
    Input[1].sec = date.hour * 60 * 60 + date.minute * 60 + date.second
    Input[1].alt = h.to(u.km).value
    Input[1].g_lat = lat.to(u.deg).value
    Input[1].g_long = lon.to(u.deg).value

    Input[1].f107 = indices[0]
    Input[1].f107A = indices[1]
    Input[1].ap = indices[2]
    Input[1].ap_a = aph

    '''Runs NLRMSISE00 Class'''
    gtd7(Input[1], flags, output[1])

    return output[1]

'''Calculate Atmsopheric conditions for given Date & Position using NRLMSISE00 Atmospheric Model'''

'''
* INPUT 1: Date at which required output will be calculates
* Date is a datetime class such that date = dt.datetime(2010,1,20,12,30,0) corresponds
* to 2010/01/20 - 12:30:00
* INPUT 2: Height use *u.meters to indicate meters or u.km to indicate kilometers
* INPUT 3: Latitude use *u.deg to indicate degrees or u.rad to indicate radians
* INPUT 4: Longitude use *u.deg to indicate degrees or u.rad to indicate radians
Note: the Solar Flux and AP Indices are calculated for the given date
'''

'''
 *   OUTPUT VARIABLES{Tuple}:
 * [0]
 *      d[0] - HE NUMBER DENSITY(N/M-3)
 *      d[1] - O NUMBER DENSITY(N/M-3)
 *      d[2] - N2 NUMBER DENSITY(M-3)
 *      d[3] - O2 NUMBER DENSITY(M-3)
 *      d[4] - AR NUMBER DENSITY(M-3)                       
 *      d[5] - TOTAL MASS DENSITY(KG/M-3)
 *      d[6] - H NUMBER DENSITY(M-3)
 *      d[7] - N NUMBER DENSITY(M-3)
 *      d[8] - Anomalous oxygen NUMBER DENSITY(M-3)
 *      t[0] - EXOSPHERIC TEMPERATURE (K)
 *      t[1] - TEMPERATURE AT ALT (K)
 * [1]
 * List Containing Solar FLux anc AP Indices
 '''

def nrl00_2(date: dt.datetime=dt.datetime(2010,10,10,12,30,0), h: float = 190000*u.meter, lat: float=-70*u.deg,
               lon: float=100*u.deg):
    return nrl00(date,h,lat,lon,Indexer(date).return_indices()[1::],aph=True),Indexer(date).return_indices()[1::]

'''Calculate High, Avg and Low Atmospheric Conditions for Date & Position using NRLMSISE00 Atmospheric Model'''

'''
* INPUT 1: Date at which required output will be calculates
* Date is a datetime class such that date = dt.datetime(2010,1,20,12,30,0) corresponds
* to 2010/01/20 - 12:30:00
* INPUT 2: Height use *u.meters to indicate meters or u.km to indicate kilometers
* INPUT 3: Latitude use *u.deg to indicate degrees or u.rad to indicate radians
* INPUT 4: Longitude use *u.deg to indicate degrees or u.rad to indicate radians
Note: the Solar Flux and AP Indices are calculated for the given date
'''

'''
 *   OUTPUT VARIABLES:
 *      d[0] - HE NUMBER DENSITY(N/M-3)
 *      d[1] - O NUMBER DENSITY(N/M-3)
 *      d[2] - N2 NUMBER DENSITY(M-3)
 *      d[3] - O2 NUMBER DENSITY(M-3)
 *      d[4] - AR NUMBER DENSITY(M-3)                       
 *      d[5] - TOTAL MASS DENSITY(KG/M-3)
 *      d[6] - H NUMBER DENSITY(M-3)
 *      d[7] - N NUMBER DENSITY(M-3)
 *      d[8] - Anomalous oxygen NUMBER DENSITY(M-3)
 *      t[0] - EXOSPHERIC TEMPERATURE (K)
 *      t[1] - TEMPERATURE AT ALT (K)
 '''

def nrl00_cond(date: dt.datetime=dt.datetime(2010,10,10,12,30,0), h: float = 190000*u.meter, lat: float=-70*u.deg,
               lon: float=100*u.deg,atmos=None):
    '''Atmospheric Conditions taken from ref [51]'''
    if atmos == 'high':
        indices = [250,250,45]
    elif atmos == 'avg':
        indices = [140,140,15]
    elif atmos == 'low':
        indices = [65,65,0]
    return nrl00(date,h,lat,lon,indices,aph=False)

if __name__ == '__main__':
    #start = time.clock()
    a = nrl00(aph=True)
    b = nrl00_2()
    c = nrl00_cond(atmos='high')
    #print(time.clock() - start)

