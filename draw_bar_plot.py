#!/usr/bin/python
# -*- encoding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np

from insert_tweets import filter_dict
from mongodb_functions import get_count


def draw_bar_plot(dictionary, title, x_axis_label, y_axis_label):
    '''
    Draws a bar plot using a dictionary.
    :param dictionary: Values of the dictionary will be the value on the y-axis and the keys of the dictionary will become the labels
    :param title: Title of the plot
    :param x_axis_label: Label of the x-axis
    :param y_axis_label: Label of the y-axis
    :return:
    '''
    bar_values = dictionary.values()  # e. g. the number of tweets
    labels = dictionary.keys()
    n = len(bar_values)

    x = np.arange(n)
    plt.bar(x, height=bar_values)
    plt.xticks(x, labels)
    plt.title(title, fontweight="bold")
    plt.xlabel(x_axis_label, fontweight="bold")
    plt.ylabel(y_axis_label, fontweight="bold")
    plt.grid(axis='y', alpha=0.75)
    plt.savefig('plots/tweets_per_language.png')
    plt.show()


def main():
    collection_names = [key for key in filter_dict.keys()]
    dictionary = {
        'English': get_count(collection_names[0]),
        'Swedish': get_count(collection_names[1]),
        'Danish': get_count(collection_names[2]),
        'Finnish': get_count(collection_names[3]),
        'Norwegian': get_count(collection_names[4])
    }
    print(dictionary.values())
    draw_bar_plot(dictionary, "Distribution of Tweets in Several Languages", "Language", "Number of Tweets")


if __name__ == "__main__": main()
