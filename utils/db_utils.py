# -*- coding: utf-8 -*-

import psycopg2
import pandas as pd
import numpy as np
import yaml
import psycopg2.extras as extr
import logging
import sys
import os
from os import environ
import datetime
from utils.log_utils import setup_logging

CONFIG_FILE = os.path.join(sys.path[0], './resources/config.yml')
setup_logging(CONFIG_FILE)


def nan_to_null(f,
                _NULL=psycopg2.extensions.AsIs('NULL'),
                _NaN=np.NaN,
                _Float=psycopg2.extensions.Float):
    if np.isnan(f):
        return _NULL
    else:
        return _Float(f)


psycopg2.extensions.register_adapter(float, nan_to_null)


def get_dwh_conn(DB):
    """
    1. Check for the database the user needs to connect
    2. Create the connection if not already connected
    3. return the connection to the user
    """
    if (DB == "dwh"):
        logging.debug("Establishing connection to 8pus")
        con_db = yaml.load(open(CONFIG_FILE), Loader=yaml.BaseLoader)['dwh']
    else:
        logging.debug("Database not known")
        return

    try:
        conn = None
        conn = psycopg2.connect(user=environ.get('rds_username') or con_db['username'],
                                password=environ.get('rds_password') or con_db['password'],
                                host=environ.get('rds_host') or con_db['host'],
                                port=environ.get('rds_port') or con_db['port'],
                                database=environ.get('rds_database_name') or con_db['name'])
    except (Exception, psycopg2.Error) as error:
        logging.debug("Error while connecting to PostgreSQL " + str(error))
        raise error

    finally:
        # return the connection
        if (conn):
            return (conn)


def close_dwh_conn(conn):
    try:
        if (conn):
            conn.close()
            logging.debug("Connection closed")
        else:
            logging.debug("Connection was not present with the database")
    except (Exception, psycopg2.Error) as error:
        logging.debug("Error while closing connection " + str(error))
        raise error


def get_dwh_result_as_df(conn, select_query, DB):
    """
    1. check if the connection exists, if not create one.
    2. Select the data from the table by passing the select query
    """
    if (not conn):
        conn = get_dwh_conn(DB)
    try:
        cursor = conn.cursor()
        cursor.execute(select_query)
        colnames = [desc[0] for desc in cursor.description]
        records = pd.DataFrame(cursor.fetchall(), columns=colnames)
        return records
    except (Exception, psycopg2.Error) as error:
        close_dwh_conn(conn)
        raise error


def insert_data_into_dwh_table(conn, schema, table_name, col_in_DWH, df, DB, return_id=''):
    """
    1. check if the connection exists, if not create one.
    2. Check if the dataframe has data
    3. create the insert query and pass it to query executer.
    """
    if (not conn):
        conn = get_dwh_conn(DB)
    try:
        if len(df) > 0:
            df_columns = col_in_DWH
            # create (col1,col2,...)
            columns = ",".join(df_columns)
            # create VALUES('%s', '%s",...) one '%s' per column
            values = "VALUES({})".format(",".join(["%s" for _ in df_columns]))
            # create INSERT INTO table (columns) VALUES('%s',...)
            if return_id == '':
                insert_stmt = "INSERT INTO {}.{} ({}) {}".format(schema, table_name, columns, values)
            else:
                insert_stmt = "INSERT INTO {}.{} ({}) {} returning {}".format(schema, table_name, columns, values,
                                                                              return_id)

            cur = conn.cursor()
            extr.execute_batch(cur, insert_stmt, df.values)
            if return_id != '':
                returned_col = cur.fetchone()[0]
            conn.commit()

            logging.debug(schema + "." + table_name + " was refreshed successfully!!")

            if return_id == '':
                return
            else:
                return returned_col
        else:
            logging.debug("{}.{} has no data to insert".format(schema, table_name))
            return
    except (Exception, psycopg2.Error) as error:
        logging.debug("Error while refreshing " + schema + "." + table_name + " " + str(error))
        closeDWHConn(conn)
        raise error


def truncate_dwh_table(conn, schema, table_name, DB):
    """
    1. Checks if the connection exists, if not create one.
    2. Truncates the table recieved in table_name argument
    """
    if (not conn):
        conn = get_dwh_conn(DB)
    try:
        cursor = conn.cursor()
        truncate_query = "delete from {}.{};".format(schema, table_name)
        cursor.execute(truncate_query)
        conn.commit()
        logging.debug("{}.{} Truncated".format(schema, table_name))
    except (Exception, psycopg2.Error) as error:
        logging.debug("Error while truncating table " + str(error))
        close_dwh_conn(conn)
        raise error


def executeQuery(conn, query, DB, data=None):
    """
    1. Checks if the connection exists, if not create one.
    2. Runs the query
    """

    if (not conn):
        conn = get_dwh_conn(DB)
    else:
        try:
            cursor = conn.cursor()
            if data:
                cursor.execute(query, data)
            else:
                cursor.execute(query)
            query_results = cursor.fetchall()
            conn.commit()
            return query_results
        except (Exception, psycopg2.Error) as error:
            logging.debug("Error while running query " + str(error) + "\
					{}".format(query))
            raise error


def create_table(conn, query, DB):
    """
    1. Checks if the connection exists, if not create one.
    2. Runs the query
    """

    if (not conn):
        conn = get_dwh_conn(DB)
    else:
        try:
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
        except (Exception, psycopg2.Error) as error:
            logging.debug("Error while running query " + str(error) + "\
					{}".format(query))
            raise error
