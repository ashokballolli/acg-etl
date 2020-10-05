import os
import sys
import psycopg2
import utils.db_utils as db_utils
from utils.log_utils import setup_logging
from utils.sns_util import notify_etl_status

CONFIG_FILE = os.path.join(sys.path[0], './resources/config.yml')
setup_logging(CONFIG_FILE)


def load_all(df_transformed, dwh_conn):
    dwh_columns = ['rep_date', 'cases', 'deaths', 'recovered']
    df_size = df_transformed.shape[0]
    try:
        db_utils.insert_data_into_dwh_table(dwh_conn, 'covid', 'daily_stats', dwh_columns, df_transformed, 'dwh')
    except (Exception, psycopg2.Error) as error:
        raise error

    return df_size


def is_it_first_run(dwh_conn):
    query = "SELECT to_regclass('covid.daily_stats')"
    try:
        query_results = db_utils.executeQuery(dwh_conn, query, 'dwh')
    except (Exception, psycopg2.Error) as error:
        raise error
    return True if query_results[0][0] == None else False


def create_table(dwh_conn):
    query = """CREATE TABLE IF NOT EXISTS covid.daily_stats (rep_date date PRIMARY KEY, cases integer, deaths integer, recovered integer)"""
    try:
        db_utils.create_table(dwh_conn, query, 'dwh')
    except (Exception, psycopg2.Error) as error:
        raise error


def load_incremental(df_transformed, dwh_conn):
    query = """SELECT max(rep_date) from covid.daily_stats"""
    try:
        query_results = db_utils.executeQuery(dwh_conn, query, 'dwh')
        max_report_date_dwh = query_results[0][0]
        diff_data = df_transformed.loc[(df_transformed['date'] > str(max_report_date_dwh))]
        df_size = diff_data.shape[0]
        dwh_columns = ['rep_date', 'cases', 'deaths', 'recovered']
        db_utils.insert_data_into_dwh_table(dwh_conn, 'covid', 'daily_stats', dwh_columns, diff_data, 'dwh')
    except (Exception, psycopg2.Error) as error:
        raise error
    return df_size


def load_to_dwh(df_transformed, dwh_conn):
    try:
        if is_it_first_run(dwh_conn):
            create_table(dwh_conn)
            df_size = load_all(df_transformed, dwh_conn)
        else:
            df_size = load_incremental(df_transformed, dwh_conn)

        if df_size:
            notify_etl_status(True, df_size)

        return df_size
    except (Exception, psycopg2.Error) as error:
        notify_etl_status(False, str(error))
        raise error
