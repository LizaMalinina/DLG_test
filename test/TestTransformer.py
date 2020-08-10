from unittest import TestCase
from Transformer import *


class TestCleanDf(TestCase):
    def test_only_correct_columns_are_returned(self):
        df = pd.DataFrame({'ForecastSiteCode': ['a'],
                           'ObservationTime': ['b'],
                           'ObservationDate': ['2020-08-05'],
                           'WindDirection': ['c'],
                           'WindSpeed': [2],
                           'ScreenTemperature': ['20'],
                           'Region': ['Region']
                           })
        expected_columns = ['ObservationDate', 'ScreenTemperature', 'Region']
        actual_columns = clean_df(df).columns
        self.assertEqual(set(expected_columns), set(actual_columns))

    def test_rows_with_empty_values_are_removed(self):
        df = pd.DataFrame({'ObservationDate': ['2020-08-05'],
                           'ScreenTemperature': [''],
                           'Region': ['Region']
                           })
        self.assertTrue(clean_df(df).empty)

    def test_rows_with_non_value_temperature_are_removed(self):
        df = pd.DataFrame({'ObservationDate': ['2020-08-05'],
                           'ScreenTemperature': ['abc'],
                           'Region': ['Region']
                           })
        self.assertTrue(clean_df(df).empty)

    def test_rows_with_invalid_date_are_removed(self):
        df = pd.DataFrame({'ObservationDate': ['abc'],
                           'ScreenTemperature': ['20'],
                           'Region': ['Region']
                           })
        self.assertTrue(clean_df(df).empty)

    def test_valid_data_remains(self):
        df = pd.DataFrame({'ObservationDate': ['2020-08-05'],
                           'ScreenTemperature': ['20'],
                           'Region': ['Region']
                           })
        self.assertEqual(1, len(clean_df(df)))


class TestGetMaxTemperaturePerRegionPerDay(TestCase):
    def test_returns_only_one_entry_per_region_per_day(self):
        df = pd.DataFrame({'ObservationDate': ['2020-08-05', '2020-08-05', '2020-08-05'],
                           'ScreenTemperature': [20, 12, 17],
                           'Region': ['Region1', 'Region1', 'Region1']
                           })
        self.assertEqual(1, len(get_max_temperature_per_region_per_day(df)))

    def test_returns_maximum_temperature_entry_per_region_per_day(self):
        df = pd.DataFrame({'ObservationDate': ['2020-08-05', '2020-08-05', '2020-08-05'],
                           'ScreenTemperature': [20, 12, 17],
                           'Region': ['Region1', 'Region1', 'Region1']
                           })
        self.assertEqual(20, get_max_temperature_per_region_per_day(df)['ScreenTemperature'].values[0])


class TestGetDataForStartEndAndTheHottestDate(TestCase):
    def test_returns_correct_start_date(self):
        df = pd.DataFrame({'ObservationDate': ['2020-08-04', '2020-08-05', '2020-08-06'],
                           'ScreenTemperature': [20, 12, 17],
                           'Region': ['Region1', 'Region2', 'Region3']
                           })
        start, _, _ = get_data_for_start_end_and_the_hottest_date(df)
        self.assertEqual('2020-08-04', start['ObservationDate'].values[0])

    def test_returns_correct_end_date(self):
        df = pd.DataFrame({'ObservationDate': ['2020-08-04', '2020-08-05', '2020-08-06'],
                           'ScreenTemperature': [20, 12, 17],
                           'Region': ['Region1', 'Region2', 'Region3']
                           })
        _, end, _ = get_data_for_start_end_and_the_hottest_date(df)
        self.assertEqual('2020-08-06', end['ObservationDate'].values[0])

    def test_returns_correct_hottest_date(self):
        df = pd.DataFrame({'ObservationDate': ['2020-08-04', '2020-08-05', '2020-08-06'],
                           'ScreenTemperature': [20, 12, 17],
                           'Region': ['Region1', 'Region2', 'Region3']
                           })
        _, _, hottest = get_data_for_start_end_and_the_hottest_date(df)
        self.assertEqual('2020-08-04', hottest['ObservationDate'].values[0])