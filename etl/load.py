import os
import sys

from utils.db_utils import db_utils
from utils.log_utils import setup_logging

CONFIG_FILE = os.path.join(sys.path[0], '../resources/config.yml')
setup_logging(CONFIG_FILE)


def load_all(dfFinal, db_obj, dwh_conn):
    dwh_columns = ['rep_date', 'cases', 'deaths', 'recovered']
    db_obj.insert_data_into_dwh_table(dwh_conn, 'covid', 'daily_stats', dwh_columns, dfFinal, 'dwh')


def is_it_first_run(db_obj, dwh_conn):
    query = "SELECT to_regclass('covid.daily_stats')"
    query_results = db_obj.executeQuery(dwh_conn, query, 'dwh')
    return True if query_results[0][0] == None else False


def create_table(db_obj, dwh_conn):
    query = """CREATE TABLE covid.daily_stats (rep_date date PRIMARY KEY, cases integer, deaths integer, recovered integer)"""
    db_obj.create_table(dwh_conn, query, 'dwh')


def load_incremental(df_transformed, db_obj, dwh_conn):
    query = """SELECT max(rep_date) from covid.daily_stats"""
    query_results = db_obj.executeQuery(dwh_conn, query, 'dwh')
    max_report_date_dwh = query_results[0][0]
    diff_data = df_transformed.loc[(df_transformed['date'] > str(max_report_date_dwh))]
    print(diff_data.head())
    dwh_columns = ['rep_date', 'cases', 'deaths', 'recovered']
    db_obj.insert_data_into_dwh_table(dwh_conn, 'covid', 'daily_stats', dwh_columns, diff_data, 'dwh')


def load_to_dwh(df_transformed):
    db_obj = db_utils(CONFIG_FILE)
    dwh_conn = db_obj.get_dwh_conn('dwh')

    if is_it_first_run(db_obj, dwh_conn):
        create_table(db_obj, dwh_conn)
        load_all(df_transformed, db_obj, dwh_conn)
    else:
        load_incremental(df_transformed, db_obj, dwh_conn)