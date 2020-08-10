import pandas as pd
from src.Validator import validate_data_quality


def transform(df: pd.DataFrame) -> pd.DataFrame:
    cleaned_df = clean_df(df)
    validated_df = validate_data_quality(cleaned_df)
    return get_max_temperature_per_region_per_day(validated_df)


def clean_df(df: pd.DataFrame) -> pd.DataFrame:
    cleaned_df = df[['ObservationDate', 'ScreenTemperature', 'Region']]
    cleaned_df = cleaned_df[cleaned_df.notnull()]
    cleaned_df['ObservationDate'] = pd.to_datetime(cleaned_df['ObservationDate'], errors='coerce').dt.date
    cleaned_df['ScreenTemperature'] = pd.to_numeric(cleaned_df['ScreenTemperature'], errors='coerce')
    return cleaned_df.dropna()


def get_max_temperature_per_region_per_day(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby(['ObservationDate', 'Region']).max('ScreenTemperature').reset_index()


def get_data_for_start_end_and_the_hottest_date(df: pd.DataFrame):
    return df[df['ObservationDate'] == min(df['ObservationDate'])], \
           df[df['ObservationDate'] == max(df['ObservationDate'])], \
           df[df['ScreenTemperature'] == max(df['ScreenTemperature'])]


def add_year_month_day_columns_to_df(df: pd.DataFrame) -> pd.DataFrame:
    df['year'] = pd.DatetimeIndex(df['ObservationDate']).year
    df['month'] = pd.DatetimeIndex(df['ObservationDate']).month
    df['day'] = pd.DatetimeIndex(df['ObservationDate']).day
    return df
