import asyncio

import requests
from datetime import datetime, timedelta, timezone
from djangoProject.classes import Vacancy
import re
import pytz


async def get_vacancies_from_api():
    vacancies = []
    names_list = ['backend', 'бэкэнд', 'бэкенд', 'бекенд', 'бекэнд', 'back end',
                  'бэк энд', 'бэк енд', 'django', 'flask', 'laravel', 'yii', 'symfony']
    moscow_time_zone = pytz.timezone("Europe/Moscow")
    date_from = (datetime.now(moscow_time_zone) - timedelta(days=1)).date()
    for name in names_list:
        for i in range(1, 20):
            try:
                x = (f"https://api.hh.ru/vacancies?text={name}&search_field=name&date_from={date_from}"
                     f"&date_to={datetime.now().date()}&only_with_salary=true&per_page=10&page=0")
                req = requests.get(x).json()
                vacancies += req['items']
                if len(vacancies) >= 10:
                    break
            except:
                continue
        if len(vacancies) >= 10:
            break

    vacancies.sort(key=lambda vac: vac['published_at'], reverse=True)
    return vacancies


async def dict_to_vacancy(vacancy):

    req = requests.get(f'https://api.hh.ru/vacancies/{vacancy["id"]}').json()
    if vacancy['salary']["from"] is not None and vacancy['salary']["to"] is not None:
        salary = f"{vacancy['salary']['from']} - {vacancy['salary']['to']} ({vacancy['salary']['currency']})"
    elif vacancy['salary']["to"] is not None:
        salary = f"{vacancy['salary']['to']} ({vacancy['salary']['currency']})"
    elif vacancy['salary']["from"] is not None:
        salary = f"{vacancy['salary']['from']} ({vacancy['salary']['currency']})"
    else:
        salary = "Не указана"

    return Vacancy(vacancy['name'], re.sub(r"<[^>]+>", "", req['description'], flags=re.S),
                             ", ".join([x['name'] for x in req['key_skills']]),
                             vacancy['employer']['name'], salary, vacancy["area"]["name"],
                             vacancy["published_at"][:10])

async def dict_to_vacancies_objects():
    vacancies_dicts = await get_vacancies_from_api()
    tasks = [dict_to_vacancy(vac) for vac in vacancies_dicts]
    vacancies = await asyncio.gather(*tasks)
    return vacancies


