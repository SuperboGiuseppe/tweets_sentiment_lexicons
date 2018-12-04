#!/usr/bin/python
# -*- encoding: utf-8 -*-

__author__ = "Emre Arkan"
__copyright__ = "Copyright 2018, Project for Natural Language Processing and Text Mining, University of Oulu"

import operator

import mongodb_functions as mdb
from insert_tweets import filter_dict


def find_x_most_active_users(collection_name, db_name='tweets', num_of_users=None, filter={}):
    """
    Sorts users by tweet number in a descending order in a given tweet collection and return the given most active users
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
            print('\t', '{}.'.format(i), 'User ID:', key, 'with', users[key], 'tweets.')
            i += 1
        print()


if __name__ == "__main__": main()
