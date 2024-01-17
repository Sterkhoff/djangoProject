import requests
import json
vacancies = []
names_list = ['backend', 'бэкэнд', 'бэкенд', 'бекенд', 'бекэнд', 'back end',
              'бэк энд', 'бэк енд', 'django', 'flask', 'laravel', 'yii', 'symfony']

years_stat = {}
for name in names_list:
    for i in range(1, 20):
        try:
            req = requests.get(f"https://api.hh.ru/vacancies?text={name}&only_with_salary=true&per_page=100&page={i}").json()
            vacancies += req['items']
        except:
            continue

for vacancy in vacancies:
    year = vacancy['published_at'][:4]
    if year not in years_stat.keys():
        to = vacancy['salary']['to']
        fro = vacancy['salary']['from']
        if vacancy['salary']['from'] is not None and vacancy['salary']['to'] is not None:
            years_stat[year] = (1, (float(vacancy['salary']['from']) + float(vacancy['salary']['to'])) / 2)
        if vacancy['salary']['from'] is None:
            years_stat[year] = (1, float(vacancy['salary']['to']))
        if vacancy['salary']['to'] is None:
            years_stat[year] = (1, float(vacancy['salary']['from']))
    else:
        years_stat[year] = (years_stat[year][0] + 1, years_stat[year][1] + (float(vacancy['salary']['from']) + float(vacancy['salary']['to'])) / 2)

print(years_stat)


