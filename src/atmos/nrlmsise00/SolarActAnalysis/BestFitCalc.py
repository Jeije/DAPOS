import numpy, scipy.optimize
import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
import statsmodels.api as sm
import statsmodels as stm
from statsmodels.tsa.seasonal import seasonal_decompose
import os

class BestFitSin(object):
    def __init__(self, idx0: int = 2000):
        self.__datafilepath = \
            '\\'.join(os.path.dirname(os.path.abspath(__file__)).split('\\')[:-4]) \
            + '\\data\\nrlmsise00_dataprocessed\\nrlmsise00_f107datapros.txt'

        self.__solardata = self.__loadcsv(self.__datafilepath)
        self.__solardata.index = pd.to_datetime(self.__solardata['date'])

        self.__f107data = self.__solardata['F107']

        self.__f107data.plot()
        print(type(self.__f107data))

        mod = sm.tsa.statespace.SARIMAX(self.__f107data, trend='c', order=(1, 1, 1))
        res = mod.fit(disp=False)
        #predict = mod.predict(self.__f107data)
        print(mod)

        model = sm.tsa.UnobservedComponents(self.__f107data,
                                            level='fixed intercept',
                                            freq_seasonal=[{'period': 395,
                                                            'harmonics': 4},
                                                           {'period': 11*365,
                                                            'harmonics': 4}])

        res_f = model.fit(disp=False)
        y_hat_avg = self.__f107data.copy()
        y_hat_avg['SARIMA'] = res_f.predict(start="2013-11-01", end="2013-12-31", dynamic=True)
        plt.plot(self.__f107data['Count'], label='Test')
        plt.plot(y_hat_avg['SARIMA'], label='SARIMA')
        plt.legend(loc='best')
        plt.show()


        # self.__residuals = pd.DataFrame(res.resid)
        # self.__residuals.plot()
        # self.__residuals.plot(kind='kde')
        #res.plot_diagnostics()
        #print(self.__residuals.describe())
        # print(res.tvalues)

        #self.__results = seasonal_decompose(self.__f107data, model='multiplicative')

        self.__decomp = seasonal_decompose(self.__f107data,freq=365*11)
        self.__decomp.plot()




    def __loadcsv(self, filepath: str):
        return pd.read_csv(filepath)

    def fit_sin(self, tt, yy):
        '''Fit sin to the input time sequence, and return fitting parameters "amp", "omega", "phase", "offset", "freq", "period" and "fitfunc"'''
        tt = numpy.array(tt,dtype=numpy.float32)
        yy = numpy.array(yy,dtype=numpy.float32)
        ff = numpy.fft.fftfreq(len(tt), (tt[1]-tt[0]))   # assume uniform spacing
        Fyy = abs(numpy.fft.fft(yy))
        guess_freq = abs(ff[numpy.argmax(Fyy[1:])+1])   # excluding the zero frequency "peak", which is related to offset
        guess_amp = numpy.std(yy) * 2.**0.5
        guess_offset = numpy.mean(yy)
        guess = numpy.array([guess_amp, 2.*numpy.pi*guess_freq, 0., guess_offset])

        def sinfunc(t, A, w, p, c):  return A * numpy.sin(w*t + p) + c
        popt, pcov = scipy.optimize.curve_fit(sinfunc, tt, yy, p0=guess)
        A, w, p, c = popt
        f = w/(2.*numpy.pi)
        fitfunc = lambda t: A * numpy.sin(w*t + p) + c
        return {"amp": A, "omega": w, "phase": p, "offset": c, "freq": f, "period": 1./f, "fitfunc": fitfunc, "maxcov": numpy.max(pcov), "rawres": (guess,popt,pcov)}

    def plotbestfit(self):
        x = numpy.linspace(0, self.__date.iloc[-1],1000)
        y = self.__bestfit['fitfunc'](x)
        plt.plot(self.__date,self.__f107)
        plt.plot(x,y)
        plt.show()

if __name__ == "__main__":
    a = BestFitSin()
    # a = numpy.array([1,2,3,4,5,6])
    # b = [numpy.sin(1),numpy.sin(2),numpy.sin(3),numpy.sin(4),numpy.sin(5),numpy.sin(6)]
    # par = fit_sin(a,b)
    # x = numpy.linspace(1,6,100)
    # c = par['amp']*numpy.sin(par['omega']*x+ par['phase']) + par['offset']

    # plt.plot(a,b)
    # plt.plot(x,c)
    # plt.show()