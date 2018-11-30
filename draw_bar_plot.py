#!/usr/bin/python
# -*- encoding: utf-8 -*-

from time import time

import matplotlib.pyplot as plt
import numpy as np

from insert_tweets import filter_dict
from mongodb_functions import get_count


def draw_bar_plot(dictionary, title, x_axis_label, y_axis_label, file_name_format="{}".format(time()),
                  x_ticks_rotation=0):
    '''
    Draws a bar plot using a dictionary.
    :param dictionary: Values of the dictionary will be the value on the y-axis and the keys of the dictionary will become the labels
    :param title: Title of the plot
    :param x_axis_label: Label of the x-axis
    :param y_axis_label: Label of the y-axis
    :param file_name_format: the name of the plot
    :return:
    '''
    is_tuple = type(list(dictionary.values())[0]) is tuple
    if is_tuple:
        bar_values = [val[0] for val in dictionary.values()]  # e. g. the number of tweets
        bar_values_irr = [val[1] for val in dictionary.values()]
    else:
        bar_values = dictionary.values()  # e. g. the number of tweets
    labels = dictionary.keys()

    n = len(bar_values)

    x = np.arange(n)
    if is_tuple:
        p1 = plt.bar(x, height=bar_values)
        p2 = plt.bar(x, height=bar_values_irr)
        plt.legend((p1[0], p2[0]), ('Actual', 'Bot'))
    else:
        plt.bar(x, height=bar_values)
    plt.xticks(x, labels)
    plt.title(title, fontweight="bold")
    plt.xlabel(x_axis_label, fontweight="bold")
    plt.ylabel(y_axis_label, fontweight="bold")
    plt.grid(axis='y', alpha=0.75)
    plt.xticks(rotation=x_ticks_rotation)
    plt.savefig("plots/{}".format(file_name_format), bbox_inches='tight')
    plt.show()


def main():
    collection_names = [key for key in filter_dict.keys()]
    # filter for the bots
    bots_fi = {'$or': [{'user.id': 550261599}, {'user.id': 2831214083}]}
    dictionary = {
        'English': (get_count(collection_names[0]), 0),
        'Swedish': (get_count(collection_names[1]), 0),
        'Danish': (get_count(collection_names[2]), 0),
        'Finnish': (get_count(collection_names[3]), get_count(collection_names[3], filter=bots_fi)),
        'Norwegian': (get_count(collection_names[4]), 0)
    }
    print(dictionary.values())
    draw_bar_plot(dictionary, "Distribution of Tweets in Several Languages", "Language", "Number of Tweets",
                  "tweets_per_language.svg")


if __name__ == "__main__": main()
