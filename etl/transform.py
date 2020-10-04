import pandas as pd


def transform(df_nyt_data, df_jh_data):
    try:
        df_jh_data = filter(df_jh_data)
        df_jh_data = df_jh_data.drop(columns='Country/Region')
        df_jh_data.columns = ['date', 'recovered']
        df_nyt_data = to_date_object(df_nyt_data)
        df_jh_data = to_date_object(df_jh_data)
        df_jh_data['recovered'] = df_jh_data['recovered'].astype('int64')
        df_transformed = df_nyt_data.join(df_jh_data, how='inner')
        df_transformed.reset_index(inplace=True)
    except (Exception) as error:
        raise error
    return df_transformed


def filter(dataframe):
    filter_condition = (dataframe['Country/Region'].notnull()) & (dataframe['Country/Region'] == 'US')
    return dataframe[filter_condition]


def to_date_object(dataframe):
    dataframe['date'] = pd.to_datetime(dataframe['date'], format='%Y-%m-%d')
    dataframe.set_index('date', inplace=True)
    return dataframe
