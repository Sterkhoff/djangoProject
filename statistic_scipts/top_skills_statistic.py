import pandas as pd
import json
from collections import Counter
from djangoProject import models



def fill_skills_with_name():
    skills_dict = {}
    skills_count_dict = {}
    csv = 'C:\\Users\\maksi\\Документы\\GitHub\\djangoProject\\statistic_scipts\\my_vacancies.csv'
    pd_reader = pd.read_csv(csv)
    for index, row in pd_reader.iterrows():
        year = int(row["published_at"][:4])
        if isinstance(row['key_skills'], str):
            if year in skills_dict.keys():
                skills_dict[year] = skills_dict[year] + row['key_skills'].replace('\r', '').split('\n')
            else:
                skills_dict[year] = row['key_skills'].replace('\r', '').split('\n')


    for year in skills_dict:
        skills_dict[year] = dict(sorted(Counter(skills_dict[year]).items(), key=lambda x: x[1], reverse=True))

    for key, value in skills_dict.items():
        for key2, value2 in value.items():
            if key2 in skills_count_dict.keys():
                skills_count_dict[key2] += value2
            else:
                skills_count_dict[key2] = value2

    skills_count_dict = dict(sorted(skills_count_dict.items(), key=lambda r: r[1], reverse=True)[:20])

    for key, value in skills_dict.items():
        models.TopSkillsWithName.objects.create(year=key, skills=", ".join(list(value.keys())[:20]))

    for key, value in skills_count_dict.items():
        models.TopSkillsInAllYearsWithName.objects.create(name=key, count=value)

def fill_skills():
    f = open("years_with_skills.json", 'r')
    skills_dict = json.load(f)
    skills_count_dict = {}
    for year in skills_dict:
        skills_dict[year] = dict(sorted(Counter(skills_dict[year]).items(), key=lambda x: x[1], reverse=True))
    for key, value in skills_dict.items():
        for key2, value2 in value.items():
            if key2 in skills_count_dict.keys():
                skills_count_dict[key2] += value2
            else:
                skills_count_dict[key2] = value2

    skills_count_dict = dict(sorted(skills_count_dict.items(), key=lambda r: r[1], reverse=True)[:20])

    for key, value in skills_count_dict.items():
        models.TopSkillInAllYears.objects.create(name=key, count=value)
