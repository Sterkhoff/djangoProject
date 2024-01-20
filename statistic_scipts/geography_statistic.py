import os.path
from pathlib import Path
import pandas as pd
from djangoProject import models
from statistic_scipts import currency_scripts
from djangoProject.settings import BASE_DIR


def refactor_df(pd_reader: pd.DataFrame):
    pd_reader['mid_salary'] = (pd_reader.apply(currency_scripts.find_salary, axis=1))
    pd_reader = pd_reader[pd_reader['mid_salary'] <= 10000000]
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
    csv = os.path.join(BASE_DIR, 'data_files', 'vacancies.csv')
    pd_reader = pd.read_csv(csv)
    pd_reader = refactor_df(pd_reader)
    cities_stat = create_cities_statistic_dataframes(pd_reader)[['area_name', 'mid_salary_of_city', 'part_of_vacancies']]
    for index, row in cities_stat.iterrows():
        models.AllCitiesStat.objects.create(city=row['area_name'],
                                            salary=row['mid_salary_of_city'],
                                            percent=row['part_of_vacancies'])


def fill_cities_stat_only_with_name():
    csv = os.path.join(BASE_DIR, 'data_files', 'my_vacancies.csv')
    pd_reader = pd.read_csv(csv)
    pd_reader = refactor_df(pd_reader)
    cities_stat = create_cities_statistic_dataframes(pd_reader)[['area_name', 'mid_salary_of_city', 'part_of_vacancies']]
    for index, row in cities_stat.iterrows():
        models.CitiesStatWithName.objects.create(city=row['area_name'],
                                                 salary=row['mid_salary_of_city'],
                                                 percent=row['part_of_vacancies'])

