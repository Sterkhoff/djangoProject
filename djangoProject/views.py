from django.shortcuts import render
from djangoProject import models
from statistic_scipts import last_vacancies
from statistic_scipts import create_graphics

def main_page(request):
    return render(request, "main_page.html")


def demand_page(request):
    years_stat_with_name = models.YearStatWithName.objects.all()
    all_years_stat = models.AllYearsStatistic.objects.all()
    return render(request, "demand_page.html", {"years": years_stat_with_name, "all_years": all_years_stat})


def geography_page(request):
    all_cities_stat = models.AllCitiesStat.objects.all()
    cities_stat_with_name = models.CitiesStatWithName.objects.all()
    return render(request, "geography.html",
                  {"cities_with_name": cities_stat_with_name, "all_cities": all_cities_stat})


def skills_page(request):
    skills_with_name = models.TopSkillsWithName.objects.all()
    all_skills = models.AllTopSkills.objects.all()
    return render(request, "skills.html", {"top_skills_in_years": all_skills,
                                           "top_skills_in_years_with_name": skills_with_name})


def last_vacancies_page(request):
    last_vac_list = last_vacancies.vacancies_to_dict()
    return render(request, "last_vacancies.html", {"vacancies": last_vac_list})
