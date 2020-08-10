import pandas as pd
import glob
from src.Validator import file_name_contains_a_valid_date, df_contains_correct_columns


def load_data(start_date: str, end_date: str, folder_path: str) -> pd.DataFrame:
    if start_date == "" and end_date == "":
        df = load_data_for_all_time(folder_path)
    elif start_date != "" and end_date == "":
        df = load_data_from_date(folder_path, start_date)
    else:
        df = load_data_between_dates(folder_path, start_date, end_date)
    return df


def load_data_for_all_time(folder_path: str) -> pd.DataFrame:
    # Assumption: all valid file names should be of form "weather.yyyymm01.csv"

    all_files = glob.glob(folder_path + "/weather.*.csv")
    full_df = None
    for filename in all_files:
        if file_name_contains_a_valid_date(filename):
            df = pd.read_csv(filename, index_col=None, header=0)
            full_df = pd.concat([full_df, df]) if df_contains_correct_columns(df) else full_df
    return full_df


def load_data_from_date(folder_path: str, start_date: str) -> pd.DataFrame:
    raise NotImplementedError


def load_data_between_dates(folder_path: str, start_date: str, end_date: str) -> pd.DataFrame:
    raise NotImplementedError






