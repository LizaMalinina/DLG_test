from unittest import TestCase
from Validator import *


class TestDfContainsCorrectColumns(TestCase):
    def test_df_contains_more_columns_returns_false(self):
        columns: List[str] = ['ForecastSiteCode', 'ObservationTime', 'ObservationDate', 'WindDirection', 'WindSpeed',
                              'WindGust', 'Visibility', 'ScreenTemperature', 'Pressure', 'SignificantWeatherCode',
                              'SiteName', 'Latitude', 'Longitude', 'Region', 'Country', 'extra_column']
        self.assertFalse(df_contains_correct_columns(pd.DataFrame(columns=columns)))

    def test_df_contains_less_columns_returns_false(self):
        columns: List[str] = ['ForecastSiteCode', 'ObservationTime', 'ObservationDate', 'WindDirection', 'WindSpeed',
                              'WindGust', 'Visibility', 'ScreenTemperature', 'Pressure', 'SignificantWeatherCode',
                              'SiteName', 'Latitude', 'Longitude', 'Region']
        self.assertFalse(df_contains_correct_columns(pd.DataFrame(columns=columns)))

    def test_df_contains_wrong_columns_returns_false(self):
        columns: List[str] = ['ForecastSiteCode', 'ObservationTime', 'ObservationDate', 'WindDirection', 'WindSpeed',
                              'WindGust', 'Visibility', 'ScreenTemperature', 'Pressure', 'SignificantWeatherCode',
                              'SiteName', 'Latitude', 'Longitude', 'Region', 'Country123']
        self.assertFalse(df_contains_correct_columns(pd.DataFrame(columns=columns)))

    def test_df_contains_correct_columns_returns_true(self):
        columns: List[str] = ['ForecastSiteCode', 'ObservationTime', 'ObservationDate', 'WindDirection', 'WindSpeed',
                              'WindGust', 'Visibility', 'ScreenTemperature', 'Pressure', 'SignificantWeatherCode',
                              'SiteName', 'Latitude', 'Longitude', 'Region', 'Country']
        self.assertTrue(df_contains_correct_columns(pd.DataFrame(columns=columns)))


class TestFileNameContainsAValidDate(TestCase):
    def test_contains_a_valid_date_before_last_dot(self):
        filename = '...20200801.csv'
        self.assertTrue(file_name_contains_a_valid_date(filename))

    def test_contains_a_valid_date_before_last_dot_but_not_first_day_of_month(self):
        filename = '...20200802.csv'
        self.assertFalse(file_name_contains_a_valid_date(filename))

    def test_contains_an_invalid_date_before_last_dot(self):
        filename = '...abcd.csv'
        self.assertFalse(file_name_contains_a_valid_date(filename))


class TestValidateDataQuality(TestCase):
    def test_data_with_temperature_above_50_is_ignored(self):
        df = pd.DataFrame({'ScreenTemperature': [51]})
        self.assertTrue(validate_data_quality(df).empty)

    def test_data_with_temperature_below_minus_50_is_ignored(self):
        df = pd.DataFrame({'ScreenTemperature': [-51]})
        self.assertTrue(validate_data_quality(df).empty)

    def test_data_with_normal_temperature_is_kept(self):
        df = pd.DataFrame({'ScreenTemperature': [15]})
        self.assertEqual(1, len(validate_data_quality(df)))
