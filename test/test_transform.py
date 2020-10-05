import unittest

import pandas

from etl.extract import extract_covid_data
from etl.transform import to_date_object, filter, transform
import os
import sys


class TestTransform(unittest.TestCase):

    def setUp(self):
        self._test_covid_nyt_data = os.path.join(sys.path[0], 'testdata/nyt_data.csv')
        self._test_covid_jh_data = os.path.join(sys.path[0], 'testdata/jh_data.csv')
        self._df_nyt_data, self._df_jh_data = extract_covid_data(self._test_covid_nyt_data, self._test_covid_jh_data)

    def test_filter_for_country_US(self):
        df_filtered = filter(self._df_jh_data)
        exp_shape = (257, 3)
        self.assertTupleEqual(df_filtered.shape, exp_shape)

    def test_to_date_object(self):
        self.assertEqual(type(self._df_nyt_data['date']), pandas.core.series.Series)
        df_date_object = to_date_object(self._df_nyt_data)
        self.assertEqual(type(df_date_object.index), pandas.core.indexes.datetimes.DatetimeIndex)

    def test_transform(self):
        df_transformed = transform(self._df_nyt_data, self._df_jh_data)
        exp_shape = (253, 4)
        self.assertTupleEqual(df_transformed.shape, exp_shape)
        exp_columns = list(['date', 'cases', 'deaths', 'recovered'])
        self.assertListEqual(list(df_transformed.columns), exp_columns)

if __name__ == '__main__':
    unittest.main()
