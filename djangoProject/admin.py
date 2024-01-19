from django.contrib import admin
from djangoProject import models

admin.site.register(models.YearStatWithName)
admin.site.register(models.AllYearsStatistic)
admin.site.register(models.CitiesStatWithName)
admin.site.register(models.AllCitiesStat)
admin.site.register(models.TopSkillsWithName)
admin.site.register(models.AllTopSkills)
admin.site.register(models.TopSkillInAllYears)
admin.site.register(models.TopSkillsInAllYearsWithName)
