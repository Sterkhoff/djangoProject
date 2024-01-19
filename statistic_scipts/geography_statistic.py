import io
import json
from datetime import datetime
import pandas as pd
import requests
from djangoProject import models


names_list = ['backend', 'бэкэнд', 'бэкенд', 'бекенд', 'бекэнд', 'back end',
              'бэк энд', 'бэк енд', 'django', 'flask', 'laravel', 'yii', 'symfony']

currency_codes = {
    "EUR": "R01239",
    "USD": "R01235",
    "BYR": "R01090",
    "KZT": "R01335",
    "UAH": "R01720",
    "AZN": "R01020A",
    "KGS": "R01370",
    "UZS": "R01717",
    "GEL": "R01210"
}

currency_dict = json.load(open("currency_values.json", "r"))

def get_currency_column(currency_code, year, month):
    response = (requests.get
                (f"http://www.cbr.ru/scripts/XML_dynamic.asp?date_req1=01/{month}/{year}&date_req2=28/{month}/{year}"
                 f"&VAL_NM_RQ={currency_code}"))
    text = io.StringIO(response.text)
    new_df = pd.read_xml(text)
    new_df = new_df.set_index('Date')
    value = str(new_df['Value'].iloc[0]).replace(',', '.')
    return str(float(value) / float(new_df['Nominal'].iloc[0]))

def find_salary(row):
    multiplier = '1'
    year = row['published_at'][:4]
    month = row['published_at'][5:7]
    currency = row['salary_currency']
    if str(currency) == 'nan':
        currency = 'RUR'
    if currency != 'RUR':
        if f"{month}.{year}" in currency_dict[currency].keys():
            multiplier = currency_dict[currency][f"{month}.{year}"]
        else:
            try:
                multiplier = get_currency_column(currency_codes[currency], year, month)
            except:
                return 0
    if str((row['salary_to'])) != 'nan' and str((row['salary_from'])) != 'nan':
        return float(((row['salary_from']) + (row['salary_to']))) / 2 * float(multiplier)
    elif str((row['salary_from'])) != 'nan':
        return float(row['salary_from']) * float(multiplier)
    elif str((row['salary_to'])) != 'nan':
        return float(row['salary_to']) * float(multiplier)
    else:
        return 0


def refactor_df(pd_reader: pd.DataFrame):
    pd_reader['mid_salary'] = (pd_reader.apply(find_salary, axis=1))
    return pd_reader


def create_cities_statistic_dataframes(pd_reader: pd.DataFrame):
    cities_dataframe = pd_reader.groupby(["area_name"]).agg({
        "mid_salary": "sum",
        "name": "count"
    }).reset_index()
    cities_dataframe.rename(columns={'mid_salary': 'sum_salary', "name": "count"},
                           inplace=True)
    cities_dataframe['mid_salary_of_city'] = (cities_dataframe
                                             .apply(lambda row: round(float(row['sum_salary'])
                                                                    / float(row['count'])), axis=1))
    cities_dataframe['part_of_vacancies'] = (cities_dataframe
                                             .apply(lambda row: float('{:.4f}'
                                                                      .format(float(row['count'])
                                                                              / len(pd_reader))) * 100, axis=1))

    return cities_dataframe[cities_dataframe['part_of_vacancies'] >= 1].reset_index()

def fill_all_cities_stat():
    csv = 'C:\\Users\\maksi\\Документы\\GitHub\\djangoProject\\statistic_scipts\\vacancies.csv'
    pd_reader = pd.read_csv(csv)
    pd_reader = refactor_df(pd_reader)
    cities_stat = create_cities_statistic_dataframes(pd_reader)[['area_name', 'mid_salary_of_city', 'part_of_vacancies']]
    for index, row in cities_stat.iterrows():
        models.AllCitiesStat.objects.create(city=row['area_name'], salary=row['mid_salary_of_city'], percent=row['part_of_vacancies'])


def fill_cities_stat_only_with_name():
    csv = 'C:\\Users\\maksi\\Документы\\GitHub\\djangoProject\\statistic_scipts\\my_vacancies.csv'
    pd_reader = pd.read_csv(csv)
    pd_reader = refactor_df(pd_reader)
    cities_stat = create_cities_statistic_dataframes(pd_reader)[['area_name', 'mid_salary_of_city', 'part_of_vacancies']]
    for index, row in cities_stat.iterrows():
        models.CitiesStatWithName.objects.create(city=row['area_name'], salary=row['mid_salary_of_city'], percent=row['part_of_vacancies'])

