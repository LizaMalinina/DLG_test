import pandas as pd
from datetime import datetime
from typing import List

RAW_DATA_COLUMNS: List[str] = ['ForecastSiteCode', 'ObservationTime', 'ObservationDate', 'WindDirection', 'WindSpeed',
                               'WindGust', 'Visibility', 'ScreenTemperature', 'Pressure', 'SignificantWeatherCode',
                               'SiteName', 'Latitude', 'Longitude', 'Region', 'Country']


def df_contains_correct_columns(df: pd.DataFrame) -> bool:
    return set(df) == set(RAW_DATA_COLUMNS)


def file_name_contains_a_valid_date(filename: str) -> bool:
    try:
        date = datetime.strptime(filename.split('.')[-2], '%Y%m%d')
        if date.day != 1:
            raise ValueError
        return True
    except ValueError:
        print(f'An exception occured when reading the file {filename}, '
              f'filename must be of type "weather.yyyymm01.csv"')
        return False


def validate_data_quality(df: pd.DataFrame) -> pd.DataFrame:
    # Assumption: temperature should never be higher than 50 degrees Celsius or below -50 degrees Celsius
    return df[df['ScreenTemperature'].between(-50, 50)]