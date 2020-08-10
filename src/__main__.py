import sys
import os
import pandas as pd
from src.Loader import load_data
from src.Saver import save_to_parquet
from src.Transformer import transform, get_data_for_start_end_and_the_hottest_date, add_year_month_day_columns_to_df

RAW_CSV_PATH: str = '../data/csv/raw'
RAW_PARQUET_PATH = '../data/parquet/raw/'
PROCESSED_PARQUET_PATH = '../data/parquet/processed/'
HELP_TEXT: str = '''
usage: python {prog_name} [start_date] [end_date]
       python {prog_name}

- Providing no dates loads data for all time
- TO BE IMPLEMENTED: Providing only start_date processes data from the specified start_date
- TO BE IMPLEMENTED: Providing 2 dates processes data for the specified date range up to but not including end_date 
'''

# TODO: implement functionality to allow 1 and 2 input dates, such that
#  Providing only start_date processes data from the specified start_date
#  Providing 2 dates processes data for the specified date range up to but not including end_date


def show_help_text() -> None:
    prog_name: bytes = os.path.realpath(__file__).split(os.sep)[-1]
    print(HELP_TEXT.format(prog_name=prog_name))


def print_result(df: pd.DataFrame) -> None:
    # Assumption: the hottest date is the date when ScreenTemperature had the highest number
    print('-' * 50)
    start, end, hottest = get_data_for_start_end_and_the_hottest_date(df)
    print(f'The hottest day between {start["ObservationDate"].values[0]} and {end["ObservationDate"].values[0]} is '
          f'{hottest["ObservationDate"].values[0]}')
    print(f'The temperature on this date was {hottest["ScreenTemperature"].values[0]} degrees Celsius')
    print(f'It happened in {hottest["Region"].values[0]} region')


def run(start_date: str, end_date: str):
    print("...Loading Data...")
    df: pd.DataFrame = load_data(start_date, end_date, RAW_CSV_PATH)

    print("...Saving Raw Data to Parquet...")
    save_to_parquet(df, RAW_PARQUET_PATH, partition_by_ymd=False)

    # Note: In a real world scenario I would divide it into multiple tasks, so that after raw data is saved to
    # parquet the next task would take raw parquet data to do all transformations with it

    print(f"...Transforming and Validating Data to {RAW_PARQUET_PATH}...")
    transformed_df: pd.DataFrame = transform(df)

    print(f"...Saving Transformed Data to {PROCESSED_PARQUET_PATH}...")
    save_to_parquet(add_year_month_day_columns_to_df(transformed_df), PROCESSED_PARQUET_PATH)

    print_result(transformed_df)


def main(args):
    start_date: str = ""
    end_date: str = ""

    if len(args) < 1 or len(args) > 3:
        show_help_text()
    else:
        if len(args) >= 2:
            start_date = args[1]
        if len(args) == 3:
            end_date = args[2]
        run(start_date, end_date)


if __name__ == '__main__':
    main(sys.argv)
