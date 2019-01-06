#!/usr/bin/python
# -*- encoding: utf-8 -*-

__author__ = "Emre Arkan"
__copyright__ = "Copyright 2018, Project for Natural Language Processing and Text Mining, University of Oulu"
__email__ = "emrearkan@outlook.de"

import operator
import os
import sys
from contextlib import contextmanager

import mongodb_functions as mdb
from insert_tweets import filter_dict


@contextmanager
def suppress_stdout():
    """
    to suppress some console outputs
    found on https://gist.github.com/djsmith42/3956189#file-gistfile1-py
    """
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout


def find_x_most_active_users(collection_name, db_name='tweets', num_of_users=None, filter={}):
    """
    Sorts users by tweet number in a descending order in a given tweet collection and returns the given most active users
    :param collection_name: collection to be opened
    :param db_name: database to be connected to
    :param num_of_users: limits the number of returned users, if not passed there is no limit
    :param filter: filter to be applied to the collection
    :return: dict of users sorted by number of tweets in descending order {id: tweet_count}
    """
    if type(num_of_users) is not int or num_of_users <= 0:
        raise ValueError('num_of_users must be a positive integer or None')
    tweet_collection = mdb.open_collection(collection_name, db_name)
    users = tweet_collection.distinct('user.id', filter)
    users_dict = {}
    for user in users:
        users_dict[user] = tweet_collection.aggregate([{'$match': {'user.id': user}}, {'$count': 'count'}]).next()[
            'count']
    desc_users = sorted(users_dict.items(), key=operator.itemgetter(1), reverse=True)
    return dict((x, y) for x, y in desc_users[:num_of_users])


def avg_sentiment_of_active_user(user_id, collection_name, db_name='tweets'):
    """
    Returns average sentiment values for given user
    :param user_id: id of the user, whose tweets are being analysed
    :param collection_name: collection to be opened
    :param db_name: database to be connected to
    :return: dict of the average sentiment scores of the given user
    """
    with suppress_stdout():
        senti_strength = mdb.apply_query({'user.id': user_id}, {'_id': 0, 'SentiStrength': 1},
                                         collection_name=collection_name)
        senti_strength = [val['SentiStrength'] for val in senti_strength]

        senti_word_net = mdb.apply_query({'user.id': user_id}, {'_id': 0, 'SentiWordNet': 1},
                                         collection_name=collection_name)
        senti_word_net = [val['SentiWordNet'] for val in senti_word_net]

        text_blob = mdb.apply_query({'user.id': user_id}, {'_id': 0, 'Textblob': 1}, collection_name=collection_name)
        text_blob = [val['Textblob'][0] for val in text_blob]

    senti_strength_avg = 0
    senti_word_net_avg = 0
    text_blob_avg = 0
    for i in range(0, len(senti_strength)):
        senti_strength_avg += senti_strength[i]
        senti_word_net_avg += senti_word_net[i]
        text_blob_avg += text_blob[i]
    senti_strength_avg /= len(senti_strength)
    senti_word_net_avg /= len(senti_word_net)
    text_blob_avg /= len(text_blob)
    return {'senti_strength_avg': senti_strength_avg, 'senti_word_net_avg': senti_word_net_avg,
            'text_blob_avg': text_blob_avg}


def main():
    collection_names = [key for key in filter_dict.keys()]
    num_of_users = 2
    for collection_name in collection_names:
        if collection_name == 'tweets_fi':
            users = find_x_most_active_users(collection_name, num_of_users=num_of_users,
                                             filter={'$nor': [{'user.id': 550261599}, {'user.id': 2831214083},
                                                              {'user.id': 3291286474}]}
                                             )
        else:
            users = find_x_most_active_users(collection_name, num_of_users=num_of_users)
        print(''.center(50, '-'))
        print(num_of_users, 'most active users in', collection_name, 'are:')
        i = 1
        for key in users.keys():
            print('\t', '{}.'.format(i), 'User ID:', key, 'with', users[key], 'tweets:')
            sentiments = avg_sentiment_of_active_user(key, collection_name=collection_name)
            print('\t\t', 'Average sentiment score of SentiStrength = {}'.format(sentiments['senti_strength_avg']))
            print('\t\t', 'Average sentiment score of SentiWordNet = {}'.format(sentiments['senti_word_net_avg']))
            print('\t\t', 'Average sentiment score of Textblob = {}'.format(sentiments['text_blob_avg']))
            i += 1
        print()


if __name__ == "__main__": main()
