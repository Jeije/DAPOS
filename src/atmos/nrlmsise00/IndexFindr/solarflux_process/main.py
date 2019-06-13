'''Importing Required Modules from Folder'''
from src.atmos.nrlmsise00.IndexFindr.solarflux_process.data_fill import NanFiller
from src.atmos.nrlmsise00.IndexFindr.solarflux_process.data_extract import DataImport
from src.atmos.nrlmsise00.IndexFindr.solarflux_process.f107a import f107a_calc

'''Importing Requiered Modules'''
import pandas as pd
import os

'''Extracts Data from Unprocessed Solar Flux txt and saves the Processed Solar Flux Indices at desired filepath'''

def extract_all_data(filepath: str = r'\\'.join(os.getcwd().split('\\')[:-4]) + '\\data\\nrlmsise00_data\\SolarFlux_Indices\\nlrmsise00_f107data.txt') -> pd.DataFrame:

    '''Function extract_all_data'''
    '''PARAM 1: Filepath of unprocessed solar flux data'''

    DI = DataImport(filepath)
    NF = NanFiller(DI.return_data())
    F107A = f107a_calc(NF.return_dataframe())

    return F107A.return_dataframe()

def save_csv(dataframe: pd.DataFrame, filepath: str = r'\\'.join(os.getcwd().split('\\')[:-4]) + '\\data\\nrlmsise00_dataprocessed\\nlrmsise00_f107datapros.txt'):
    '''Function save_csv'''
    '''PARAM 1: Pandas DataFrame containing processed solar flux data'''
    '''PARAM 2: Filepath to save processed solar flux data'''

    dataframe.to_csv(filepath)

if __name__ == "__main__":
    Dataframe = extract_all_data()
    save_csv(Dataframe)
