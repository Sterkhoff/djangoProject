import io
import json
from datetime import datetime
import pandas as pd
import requests
from djangoProject import models
vacancies = []
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

def check(df):
    for index, row in df.iterrows():
        if row['published_at'] == 2005 and row["mid_salary"] > 1000000:
            print(row["mid_salary"], row['salary_currency'], row['salary_to'], row['salary_from'])
def change_date_on_year(pd_reader):
    date_column = pd_reader['published_at']
    new_date_column = date_column.apply(lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%S%z').year)
    pd_reader['published_at'] = new_date_column
    return pd_reader

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
    pd_reader = change_date_on_year(pd_reader)
    return pd_reader


def create_years_statistic_dataframes(pd_reader: pd.DataFrame):
    years_dataframe = pd_reader.groupby(["published_at"]).agg({
        "mid_salary": "sum",
        "name": "count"
    }).reset_index()
    years_dataframe.rename(columns={'published_at': 'year', 'mid_salary': 'sum_salary', "name": "count"},
                           inplace=True)
    years_dataframe['mid_salary_of_year'] = (years_dataframe
                                             .apply(lambda row: round(float(row['sum_salary'])
                                                                    / float(row['count'])), axis=1))
    return years_dataframe


def create_curr_dict():
    curr_dict = {}
    for month in range(1, 13):
        for year in range(3, 2024):
            date_str = f"{str(month).zfill(2)}.20{str(year).zfill(2)}"
            for key, value in curr_dict.items():
                curr_dict[key] = \
                    {date_str: get_currency_column(value, str(month).zfill(2), "20"+str(year).zfill(2))}
    with open("currency_values.json", "w") as outfile:
        outfile.write(json.dumps(curr_dict))


def fill_all_years_stat():
    csv = 'C:\\Users\\maksi\\Документы\\GitHub\\djangoProject\\statistic_scipts\\vacancies.csv'
    pd_reader = pd.read_csv(csv)
    pd_reader = refactor_df(pd_reader)
    check(pd_reader)
    years_stat = create_years_statistic_dataframes(pd_reader)[['year', 'mid_salary_of_year', 'count']]
    for index, row in years_stat.iterrows():
        models.AllYearsStatistic.objects.create(year=row['year'], salary=row['mid_salary_of_year'], count=row['count'])


def fill_years_stat_only_with_name():
    csv = 'C:\\Users\\maksi\\Документы\\GitHub\\djangoProject\\statistic_scipts\\my_vacancies.csv'
    pd_reader = pd.read_csv(csv)
    pd_reader = refactor_df(pd_reader)
    check(pd_reader)
    years_stat = create_years_statistic_dataframes(pd_reader)[['year', 'mid_salary_of_year', 'count']]
    for index, row in years_stat.iterrows():
        models.YearStatWithName.objects.create(year=row['year'], salary=row['mid_salary_of_year'], count=row['count'])

