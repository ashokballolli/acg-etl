from etl.extract import extract_covid_data
from etl.load import load_to_dwh
from etl.transform import transform


def load_data(event, context):
    df_nyt_data, df_jh_data = extract_covid_data()
    df_transformed = transform(df_nyt_data, df_jh_data)
    load_to_dwh(df_transformed)


load_data("", "")