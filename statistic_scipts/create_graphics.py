import matplotlib.pyplot as plt
import numpy as np


def create_histogram_graph(x_values, y_values, label, title, file_name, ylabel):
    fig, ax = plt.subplots()
    ax.bar(x_values, y_values, label=label)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.set_xticks(x_values)
    ax.set_xticklabels(x_values, rotation=90)
    plt.savefig(f'C:\\Users\\maksi\\Документы\\GitHub\\djangoProject\\static\\images\\{file_name}')


def create_circle_graph(cities, percents, file_name, title):
    fig, ax = plt.subplots()
    groups = cities + ["Другие"]
    values = percents + [(100 - sum(percents))]
    ax.pie(values, labels=groups, textprops={'fontsize': 6})
    ax.set_title(title, fontsize=8)
    plt.savefig(f'C:\\Users\\maksi\\Документы\\GitHub\\djangoProject\\static\\images\\{file_name}')