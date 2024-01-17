from django.db import models


class YearStatWithName(models.Model):
    year = models.IntegerField("Год")
    count = models.IntegerField("Количество вакансий")
    salary = models.IntegerField("Средняя з/п")


class AllYearsStatistic(models.Model):
    year = models.IntegerField("Год")
    count = models.IntegerField("Количество вакансий")
    salary = models.IntegerField("Средняя з/п")


class CitiesStatWithName(models.Model):
    city = models.CharField(max_length=255)
    percent = models.IntegerField("Процент вакансий")
    salary = models.IntegerField("Средняя з/п")


class AllCitiesStat(models.Model):
    city = models.CharField(max_length=255)
    percent = models.IntegerField("Процент вакансий")
    salary = models.IntegerField("Средняя з/п")
    