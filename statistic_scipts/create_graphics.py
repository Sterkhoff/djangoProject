import matplotlib.pyplot as plt
from djangoProject import models

def create_all_graphics():
    create_histogram_graph([x.year for x in models.AllYearsStatistic.objects.all()],
                                           [x.salary for x in models.AllYearsStatistic.objects.all()],
                                           "Динамика уровня зарплат по годам", "Динамика уровня зарплат по годам",
                                           "third_graph.png", "Средняя з/п, руб.")

    create_histogram_graph([x.year for x in models.AllYearsStatistic.objects.all()],
                                           [x.count for x in models.AllYearsStatistic.objects.all()],
                                           "Динамика количества вакансий по годам",
                                           "Динамика количества вакансий по годам",
                                           "fourth_graph.png", "Кол-во вакансий.")

    create_histogram_graph([x.year for x in models.YearStatWithName.objects.all()],
                                           [x.salary for x in models.YearStatWithName.objects.all()],
                                           "Динамика уровня зарплат по годам для профессии 'Backend-разработчик'",
                                           "Динамика уровня зарплат по годам для профессии 'Backend-разработчик'",
                                           "first_graph.png", "Средняя з/п, руб.")

    create_histogram_graph([x.year for x in models.YearStatWithName.objects.all()],
                                           [x.count for x in models.YearStatWithName.objects.all()],
                                           "Динамика количества вакансий по годам для профессии 'Backend-разработчик'",
                                           "Динамика количества вакансий по годам для профессии 'Backend-разработчик'",
                                           "second_graph.png", "Средняя з/п, руб.")

    create_histogram_graph(
        [x.city for x in sorted(models.AllCitiesStat.objects.all(), key=lambda x: x.salary, reverse=True)],
        [x.salary for x in sorted(models.AllCitiesStat.objects.all(), key=lambda x: x.salary, reverse=True)],
        "Уровень зарплат по городам", "Уровень зарплат по городам",
        "first_geo_graph.png", "Средняя p/п, руб.")

    create_histogram_graph(
        [x.city for x in sorted(models.CitiesStatWithName.objects.all(), key=lambda x: x.salary, reverse=True)],
        [x.salary for x in sorted(models.CitiesStatWithName.objects.all(), key=lambda x: x.salary, reverse=True)],
        "Уровень зарплат по городам для профессии 'Backend-разработчик'",
        "Уровень зарплат по городам для профессии 'Backend-разработчик'",
        "third_geo_graph.png", "Средняя з/п, руб.")

    create_circle_graph([x.city for x in models.AllCitiesStat.objects.all()],
                                        [x.percent for x in models.AllCitiesStat.objects.all()],
                                        "second_geo_graph.png", "Доля вакансий по городам")

    create_circle_graph([x.city for x in models.CitiesStatWithName.objects.all()],
                                        [x.percent for x in models.CitiesStatWithName.objects.all()],
                                        "fourth_geo_graph.png",
                                        "Доля вакансий по городам для профессии 'Backend-разработчик'")

def create_histogram_graph(x_values, y_values, label, title, file_name, ylabel):
    fig, ax = plt.subplots()
    ax.bar(x_values, y_values, label=label)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.set_xticks(x_values)
    ax.set_xticklabels(x_values, rotation=90)
    plt.tight_layout()
    plt.savefig(f'C:\\Users\\maksi\\Документы\\GitHub\\djangoProject\\static\\images\\{file_name}', bbox_inches='tight')


def create_circle_graph(cities, percents, file_name, title):
    fig, ax = plt.subplots()
    groups = cities + ["Другие"]
    values = percents + [(100 - sum(percents))]
    ax.pie(values, labels=groups)
    ax.set_title(title)
    plt.tight_layout()
    plt.savefig(f'C:\\Users\\maksi\\Документы\\GitHub\\djangoProject\\static\\images\\{file_name}', bbox_inches='tight')