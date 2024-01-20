from datetime import datetime
import pandas as pd
import os.path
from djangoProject import models
from djangoProject.settings import BASE_DIR
from statistic_scipts import currency_scripts


vacancies = []
names_list = ['backend', 'бэкэнд', 'бэкенд', 'бекенд', 'бекэнд', 'back end',
              'бэк энд', 'бэк енд', 'django', 'flask', 'laravel', 'yii', 'symfony']


def change_date_on_year(pd_reader):
    date_column = pd_reader['published_at']
    new_date_column = date_column.apply(lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%S%z').year)
    pd_reader['published_at'] = new_date_column
    return pd_reader


def refactor_df(pd_reader: pd.DataFrame):
    pd_reader['mid_salary'] = (pd_reader.apply(currency_scripts.find_salary, axis=1))
    pd_reader = pd_reader[pd_reader['mid_salary'] <= 10000000]
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


def fill_all_years_stat():
    csv = os.path.join(BASE_DIR, 'data_files', 'vacancies.csv')
    pd_reader = pd.read_csv(csv)
    pd_reader = refactor_df(pd_reader)
    years_stat = create_years_statistic_dataframes(pd_reader)[['year', 'mid_salary_of_year', 'count']]
    for index, row in years_stat.iterrows():
        models.AllYearsStatistic.objects.create(year=row['year'], salary=row['mid_salary_of_year'], count=row['count'])


def create_my_vacancies():
    csv = os.path.join(BASE_DIR, 'data_files', 'vacancies.csv')
    df = pd.read_csv(csv)
    df[df.str.contains('|'.join(names_list))].to_csv(os.path.join(BASE_DIR, 'data_files', 'my_vacancies.csv'))


def fill_years_stat_only_with_name():
    csv = os.path.join(BASE_DIR, 'data_files', 'my_vacancies.csv')
    pd_reader = pd.read_csv(csv)
    pd_reader = refactor_df(pd_reader)
    years_stat = create_years_statistic_dataframes(pd_reader)[['year', 'mid_salary_of_year', 'count']]
    for index, row in years_stat.iterrows():
        models.YearStatWithName.objects.create(year=row['year'], salary=row['mid_salary_of_year'], count=row['count'])

