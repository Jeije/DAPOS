'''Importing Requiered Modules from Folder'''
from src.atmos.nrlmsise00.ap_process.data_process import ApDataPros
from src.atmos.nrlmsise00.ap_process.data_extract import ApDataImport

'''Importing Requierd Modules'''
import pandas as pd
import os

def extractdata(filepath: str = r'\\'.join(os.getcwd().split('\\')[:-4]) + '\\data\\nrlmsise00_data\\AP_Indices'):
    '''Function extractdata'''
    '''PARAM 1: Filepath of unprocessed ap data'''

    DI = ApDataImport(filepath)
    data = DI.return_data()
    years = DI.return_yealst()
    return data,years

def return_ap(data:list,years:list):
    '''Function return_ap'''
    '''PARAM 1: Processed AP data'''
    '''PARAM 2: Year list of all processed data'''

    return ApDataPros(data,years)

def df(ap:list):
    '''Function df'''
    '''Defines Columns of AP Processed DataFrame'''
    '''PARAM 1: Processed AP data'''
    '''PARAM 2: Year list of all processed data'''

    df = pd.DataFrame(ap)
    #df.columns = ['date','ap_daily','ap1','ap2','ap3','ap4','apavg1','apavg2']
    return df

def save_csv(dataframe: pd.DataFrame, filepath: str = r'\\'.join(os.getcwd().split('\\')[:-4]) + '\\data\\nrlmsise00_dataprocessed\\nlrmsise00_AP_processed.txt'):
    '''Function save_csv'''
    '''PARAM 1: Pandas DataFrame containing processed AP data'''
    '''PARAM 2: Filepath to save processed AP data'''

    dataframe.to_csv(filepath)

if __name__ == "__main__":
    data,years = extractdata()
    ap = return_ap(data,years)
    aplst = ap.return_apdata()
    apdf = df(aplst)
    save_csv(apdf)
