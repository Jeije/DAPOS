import pandas as pd

from data_process import ApDataPros
from data_extract import ApDataImport

def extractdata(filepath: str = r'C:\Users\mauro\OneDrive\AE Bachelor - TU Delft\Year 3\DSE - Local\DAPOS_Main\src\atmos\nlrmsise00_data\AP_Indices'):
    DI = ApDataImport(filepath)
    data = DI.return_data()
    years = DI.return_yealst()
    return data,years

def returnap(data:list,years:list):
    return ApDataPros(data,years)

def df(ap:list):
    df = pd.DataFrame(ap)
    df.columns = ['date','ap_daily','ap1','ap2','ap3','ap4','apavg1','apavg2']
    return df

def save_csv(dataframe: pd.DataFrame, filepath: str = r"C:\Users\mauro\OneDrive\AE Bachelor - TU Delft\Year 3\DSE - Local\DAPOS_Main\src\atmos\nlrmsise00_data\nlrmsise00_AP_processed.txt"):
    dataframe.to_csv(filepath)

if __name__ == "__main__":
    data,years = extractdata()
    ap = returnap(data,years)
    b = ap.return_aplst(44,10)
    aplst = ap.return_apdata()
    apdf = df(aplst)
    save_csv(apdf)
