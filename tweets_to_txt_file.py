#!/usr/bin/python
# -*- encoding: utf-8 -*-

import csv
from mongodb_functions import apply_query


def tweets_to_txt_file(tweet_cursor, file_name, fields):
    with open(file_name, "w+", encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fields, delimiter='\t')
        writer.writeheader()
        for tweet in tweet_cursor:
            writer.writerow(tweet)
    file.close()


def main():
    # bots_fi = {'$nor': [{'user.id': 550261599}, {'user.id': 2831214083}, 'user.id': 3291286474}]}
    tweets_en = apply_query({}, {'_id': 1, 'demojized_text': 1}, collection_name='tweets_en')
    tweets_da = apply_query({}, {'_id': 1, 'demojized_text': 1}, collection_name='tweets_da')
    tweets_fi = apply_query({}, {'_id': 1, 'demojized_text': 1}, collection_name='tweets_fi')
    tweets_no = apply_query({}, {'_id': 1, 'demojized_text': 1}, collection_name='tweets_no')
    tweets_sv = apply_query({}, {'_id': 1, 'demojized_text': 1}, collection_name='tweets_sv')

    tweets_to_txt_file(tweets_en, 'textfiles/tweets_en.txt', ['_id', 'demojized_text'])
    tweets_to_txt_file(tweets_da, 'textfiles/tweets_da.txt', ['_id', 'demojized_text'])
    tweets_to_txt_file(tweets_fi, 'textfiles/tweets_fi.txt', ['_id', 'demojized_text'])
    tweets_to_txt_file(tweets_no, 'textfiles/tweets_no.txt', ['_id', 'demojized_text'])
    tweets_to_txt_file(tweets_sv, 'textfiles/tweets_sv.txt', ['_id', 'demojized_text'])


if __name__ == "__main__": main()
