import requests
import json
import os.path
from djangoProject.settings import BASE_DIR
import io
import pandas as pd

currency_dict = json.load(open(os.path.join(BASE_DIR, 'data_files', 'currency_values.json'), "r"))

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


def get_currency_value(currency_code, year, month):
    response = (requests.get
                (f"http://www.cbr.ru/scripts/XML_dynamic.asp?date_req1=01/{month}/{year}&date_req2=28/{month}/{year}"
                 f"&VAL_NM_RQ={currency_code}"))
    text = io.StringIO(response.text)
    new_df = pd.read_xml(text)
    new_df = new_df.set_index('Date')
    value = str(new_df['Value'].iloc[0]).replace(',', '.')
    return str(float(value) / float(new_df['Nominal'].iloc[0]))


def create_curr_dict():
    curr_dict = {}
    for month in range(1, 13):
        for year in range(3, 2024):
            date_str = f"{str(month).zfill(2)}.20{str(year).zfill(2)}"
            for key, value in curr_dict.items():
                curr_dict[key] = \
                    {date_str: get_currency_value(value, str(month).zfill(2), "20" + str(year).zfill(2))}
    with open(os.path.join(BASE_DIR, 'data_files', 'currency_values.json'), "w") as outfile:
        outfile.write(json.dumps(curr_dict))


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
                multiplier = get_currency_value(currency_codes[currency], year, month)
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