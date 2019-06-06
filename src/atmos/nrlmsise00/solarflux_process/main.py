from data_fill import NanFiller
from data_extract import DataImport
from f107a import f107a_calc
import pandas as pd


def extract_all_data(filepath: str = r"C:\Users\mauro\OneDrive\AE Bachelor - TU Delft\Year 3\DSE - Local\DAPOS_Main\src\atmos\nlrmsise00_data\SolarFlux_Indices\nlrmsise00_f107data.txt") -> pd.DataFrame:

    DI = DataImport(filepath)
    NF = NanFiller(DI.return_data())
    F107A = f107a_calc(NF.return_dataframe())

    return F107A.return_dataframe()

def save_csv(dataframe: pd.DataFrame, filepath: str = r"C:\Users\mauro\OneDrive\AE Bachelor - TU Delft\Year 3\DSE - Local\DAPOS_Main\src\atmos\nlrmsise00_data\nlrmsise00_f107datapros.txt"):
    dataframe.to_csv(filepath)

if __name__ == "__main__":
    Dataframe = extract_all_data()
    save_csv(Dataframe)

