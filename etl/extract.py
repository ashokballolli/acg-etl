import pandas as pd
from utils.sns_util import notify_etl_status


def extract_covid_data(url_covid_nyt_data, url_covid_jh_data):
    try:
        df_nyt_data = pd.read_csv(url_covid_nyt_data)
        df_jh_data = pd.read_csv(url_covid_jh_data, usecols=['Date', 'Country/Region', 'Recovered'])
        return df_nyt_data, df_jh_data
    except (Exception) as error:
        notify_etl_status(False, str(error))
