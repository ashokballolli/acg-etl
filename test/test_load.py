import unittest
import datetime
from etl.extract import extract_covid_data
import os
import sys
import testing.postgresql
import psycopg2
from etl.load import load_to_dwh, is_it_first_run, load_incremental
from etl.transform import transform
import utils.db_utils as db_utils
import pandas as pd


class TestLoad(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self._test_covid_nyt_data = os.path.join(sys.path[0], 'testdata/nyt_data.csv')
        self._test_covid_jh_data = os.path.join(sys.path[0], 'testdata/jh_data.csv')

        df_nyt_data, df_jh_data = extract_covid_data(self._test_covid_nyt_data, self._test_covid_jh_data)
        self._df_transformed = transform(df_nyt_data, df_jh_data)

        self.postgresql = testing.postgresql.Postgresql()
        self.conn = psycopg2.connect(**self.postgresql.dsn())
        cursor = self.conn.cursor()
        cursor.execute("CREATE SCHEMA covid")
        cursor.close()
        self.conn.commit()

    def test_10_is_it_first_run(self):
        actual = is_it_first_run(self.conn)
        self.assertTrue(actual)

    def test_20_load_to_dwh(self):
        load_to_dwh(self._df_transformed, self.conn)
        df_result = db_utils.get_dwh_result_as_df(self.conn,
                                                  "select * from covid.daily_stats ds  order by ds.rep_date desc", "")
        exp_shape = (253, 4)
        exp_recent_record = list([datetime.date(2020, 9, 30), 7262695, 206852, 2840688])
        exp_columns = list(['rep_date', 'cases', 'deaths', 'recovered'])
        self.assertTupleEqual(df_result.shape, exp_shape)
        self.assertListEqual(list(df_result.columns), exp_columns)
        self.assertListEqual(list(df_result.iloc[0]), exp_recent_record)

    def test_30_load_to_dwh(self):
        load_to_dwh(self._df_transformed, self.conn)
        df_result = db_utils.get_dwh_result_as_df(self.conn,
                                                  "select * from covid.daily_stats ds  order by ds.rep_date desc", "")
        exp_shape = (253, 4)
        exp_recent_record = list([datetime.date(2020, 9, 30), 7262695, 206852, 2840688])
        exp_columns = list(['rep_date', 'cases', 'deaths', 'recovered'])
        self.assertTupleEqual(df_result.shape, exp_shape)
        self.assertListEqual(list(df_result.columns), exp_columns)
        self.assertListEqual(list(df_result.iloc[0]), exp_recent_record)

    def test_31_load_to_dwh_error(self):
        dummy_conn = psycopg2.connect(**self.postgresql.dsn())
        dummy_conn.close()
        with self.assertRaises(psycopg2.Error):
            load_to_dwh(self._df_transformed, dummy_conn)

    def test_32_load_to_dwh_empty_dataframe(self):
        column_names = ['date', 'cases', 'deaths', 'recovered']
        df_empty = pd.DataFrame(columns=column_names)
        load_to_dwh(df_empty, self.conn)
        df_result = db_utils.get_dwh_result_as_df(self.conn,
                                                  "select * from covid.daily_stats ds  order by ds.rep_date desc", "")
        exp_shape = (253, 4)
        exp_recent_record = list([datetime.date(2020, 9, 30), 7262695, 206852, 2840688])
        self.assertTupleEqual(df_result.shape, exp_shape)
        self.assertListEqual(list(df_result.iloc[0]), exp_recent_record)

    def test_33_load_to_dwh_should_return_0_if_no_new_records(self):
        df_size = load_to_dwh(self._df_transformed, self.conn)
        self.assertEqual(df_size, 0)

    def test_34_load_to_dwh_duplicate_insert(self):
        df_result = db_utils.get_dwh_result_as_df(self.conn,
                                                  "select * from covid.daily_stats ds  order by ds.rep_date desc", "")
        exp_shape = (253, 4)
        exp_recent_record = list([datetime.date(2020, 9, 30), 7262695, 206852, 2840688])
        self.assertListEqual(list(df_result.iloc[0]), exp_recent_record)
        self.assertTupleEqual(df_result.shape, exp_shape)

        load_to_dwh(self._df_transformed, self.conn)

        df_result = db_utils.get_dwh_result_as_df(self.conn,
                                                  "select * from covid.daily_stats ds  order by ds.rep_date desc", "")
        exp_shape = (253, 4)
        exp_recent_record = list([datetime.date(2020, 9, 30), 7262695, 206852, 2840688])
        self.assertTupleEqual(df_result.shape, exp_shape)
        self.assertListEqual(list(df_result.iloc[0]), exp_recent_record)

    def test_40_load_incremental(self):
        test_covid_nyt_data_latest = os.path.join(sys.path[0], 'testdata/nyt_data_latest.csv')

        df_nyt_data, df_jh_data = extract_covid_data(test_covid_nyt_data_latest, self._test_covid_jh_data)
        df_transformed_latest = transform(df_nyt_data, df_jh_data)

        load_to_dwh(df_transformed_latest, self.conn)
        df_result = db_utils.get_dwh_result_as_df(self.conn,
                                                  "select * from covid.daily_stats ds  order by ds.rep_date desc", "")

        exp_shape = (257, 4)
        exp_recent_record = list([datetime.date(2020, 10, 4), 7444705, 209603, 2911699])
        exp_columns = list(['rep_date', 'cases', 'deaths', 'recovered'])
        self.assertTupleEqual(df_result.shape, exp_shape)
        self.assertListEqual(list(df_result.columns), exp_columns)
        self.assertListEqual(list(df_result.iloc[0]), exp_recent_record)

    def test_41_load_incremental_should_return_0_if_no_new_records(self):
        test_covid_nyt_data_latest = os.path.join(sys.path[0], 'testdata/nyt_data_latest.csv')

        df_nyt_data, df_jh_data = extract_covid_data(test_covid_nyt_data_latest, self._test_covid_jh_data)
        df_transformed_latest = transform(df_nyt_data, df_jh_data)

        df_size = load_incremental(df_transformed_latest, self.conn)
        self.assertEqual(df_size, 0)

    def test_42_load_incremental_duplicate_insert(self):
        df_result = db_utils.get_dwh_result_as_df(self.conn,
                                                  "select * from covid.daily_stats ds  order by ds.rep_date desc", "")

        exp_shape = (257, 4)
        exp_recent_record = list([datetime.date(2020, 10, 4), 7444705, 209603, 2911699])
        self.assertTupleEqual(df_result.shape, exp_shape)
        self.assertListEqual(list(df_result.iloc[0]), exp_recent_record)

        test_covid_nyt_data_latest = os.path.join(sys.path[0], 'testdata/nyt_data_latest.csv')

        df_nyt_data, df_jh_data = extract_covid_data(test_covid_nyt_data_latest, self._test_covid_jh_data)
        df_transformed_latest = transform(df_nyt_data, df_jh_data)

        load_to_dwh(df_transformed_latest, self.conn)
        df_result = db_utils.get_dwh_result_as_df(self.conn,
                                                  "select * from covid.daily_stats ds  order by ds.rep_date desc", "")

        exp_shape = (257, 4)
        exp_recent_record = list([datetime.date(2020, 10, 4), 7444705, 209603, 2911699])
        self.assertTupleEqual(df_result.shape, exp_shape)
        self.assertListEqual(list(df_result.iloc[0]), exp_recent_record)

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()
        cls.postgresql.stop()


if __name__ == '__main__':
    unittest.main()
