#!/usr/bin/python
# -*- encoding: utf-8 -*-

import mongodb_functions as mdb
from mongodb_functions import apply_query
import csv

def tweets_to_txt_file(tweet_cursor, file_name, fields):
    with open(file_name, "w+", encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fields, delimiter='\t')
        writer.writeheader()
        for tweet in tweet_cursor:
            writer.writerow(tweet)
    file.close()


def main():
    tweets_en = mdb.apply_query({}, {'_id': 1, 'text': 1}, collection_name='tweets_en')
    tweets_da = mdb.apply_query({}, {'_id': 1, 'translated_text': 1}, collection_name='tweets_da')
    tweets_fi = mdb.apply_query({}, {'_id': 1, 'translated_text': 1}, collection_name='tweets_fi')
    tweets_no = mdb.apply_query({}, {'_id': 1, 'translated_text': 1}, collection_name='tweets_no')
    tweets_sv = mdb.apply_query({}, {'_id': 1, 'translated_text': 1}, collection_name='tweets_sv')

    tweets_to_txt_file(tweets_en, 'textfiles/tweets_en.txt', ['_id', 'text'])
    tweets_to_txt_file(tweets_da, 'textfiles/tweets_da.txt', ['_id', 'translated_text'])
    tweets_to_txt_file(tweets_fi, 'textfiles/tweets_fi.txt', ['_id', 'translated_text'])
    tweets_to_txt_file(tweets_no, 'textfiles/tweets_no.txt', ['_id', 'translated_text'])
    tweets_to_txt_file(tweets_sv, 'textfiles/tweets_sv.txt', ['_id', 'translated_text'])


if __name__ == "__main__": main()