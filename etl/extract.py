import pandas as pd
import os
import sys
import yaml
from utils.sns_util import notify_etl_status

CONFIG_FILE = os.path.join(sys.path[0], './resources/config.yml')


def extract_covid_data():
    try:
        data = yaml.load(open(CONFIG_FILE), Loader=yaml.BaseLoader)['data']

        df_nyt_data = pd.read_csv(data['url_covid_nyt_data'])
        df_jh_data = pd.read_csv(data['url_covid_jh_data'], usecols=['Date', 'Country/Region', 'Recovered'])
        return df_nyt_data, df_jh_data
    except (Exception) as error:
        notify_etl_status(False, str(error))