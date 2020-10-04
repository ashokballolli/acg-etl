from etl.extract import extract_covid_data
from etl.load import load_to_dwh
from etl.transform import transform
import os
import sys
import yaml
import utils.db_utils as db_utils
import psycopg2
from utils.sns_util import notify_etl_status

CONFIG_FILE = os.path.join(sys.path[0], 'resources/config.yml')


def load_data(event, context):
    try:
        data = yaml.load(open(CONFIG_FILE), Loader=yaml.BaseLoader)['data']
        url_covid_nyt_data = data['url_covid_nyt_data']
        url_covid_jh_data = data['url_covid_jh_data']
        dwh_conn = db_utils.get_dwh_conn('dwh')

    except (Exception, psycopg2.Error) as error:
        notify_etl_status(False, str(error))

    df_nyt_data, df_jh_data = extract_covid_data(url_covid_nyt_data, url_covid_jh_data)
    df_transformed = transform(df_nyt_data, df_jh_data)
    load_to_dwh(df_transformed, dwh_conn)


load_data("", "")
