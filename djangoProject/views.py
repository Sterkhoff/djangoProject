from django.shortcuts import render
from djangoProject import models


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
    return render(request, "skills.html")


def last_vacancies_page(request):
    return render(request, "last_vacancies.html")
