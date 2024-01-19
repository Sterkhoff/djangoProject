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


class TopSkillsWithName(models.Model):
    year = models.IntegerField("Год")
    skills = models.CharField(max_length=255)


class AllTopSkills(models.Model):
    year = models.IntegerField("Год")
    skills = models.CharField(max_length=255)


class TopSkillInAllYears(models.Model):
    name = models.CharField(max_length=255)
    count = models.IntegerField("Количество")


class TopSkillsInAllYearsWithName(models.Model):
    name = models.CharField(max_length=255)
    count = models.IntegerField("Количество")