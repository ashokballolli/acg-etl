import unittest
from etl.extract import extract_covid_data
import os
import sys


class TestExtract(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self._test_covid_nyt_data = os.path.join(sys.path[0], 'testdata/nyt_data.csv')
        self._test_covid_jh_data = os.path.join(sys.path[0], 'testdata/jh_data.csv')

    def test_extract_dataframe_size(self):
        df_nyt_data, df_jh_data = extract_covid_data(self._test_covid_nyt_data, self._test_covid_jh_data)
        exp_shape_nyt_data = (254, 3)
        exp_shape_jh_data = (68362, 3)
        self.assertTupleEqual(df_nyt_data.shape, exp_shape_nyt_data)
        self.assertTupleEqual(df_jh_data.shape, exp_shape_jh_data)

    def test_extract_dataframe_column_names(self):
        df_nyt_data, df_jh_data = extract_covid_data(self._test_covid_nyt_data, self._test_covid_jh_data)
        exp_columns_nyt_data = list(['date', 'cases', 'deaths'])
        exp_columns_jh_data = list(['Date', 'Country/Region', 'Recovered'])
        self.assertListEqual(list(df_nyt_data.columns), exp_columns_nyt_data)
        self.assertListEqual(list(df_jh_data.columns), exp_columns_jh_data)

    def test_extract_error_for_invalid_url(self):
        with self.assertRaises(TypeError):
            df_nyt_data, df_jh_data = extract_covid_data(self._test_covid_nyt_data, "www.column.name")
            print(df_jh_data.head())

if __name__ == '__main__':
    unittest.main()
