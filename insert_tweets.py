#!/usr/bin/python
# -*- encoding: utf-8 -*-

__author__ = "Emre Arkan"
__copyright__ = "Copyright 2018, Project for Natural Language Processing and Text Mining, University of Oulu"

from mongodb_functions import *

filter_dict = {
    'tweets_en': {"lang": "en"},
    'tweets_sv': {"lang": "sv"},
    'tweets_da': {"lang": "da"},
    'tweets_fi': {"lang": "fi"},
    'tweets_no': {"lang": "no"}
}


def main():
    successfull = import_tweets("tweets/tweets.json")
    if successfull:
        # select only id, text, user and lang
        projection = {"_id": 1, "text": 1, "user": 1, "lang": 1}

        # <collection_name> : <language_tag>

        for key, val in filter_dict.items():
            export_tweets_into_collection(val, projection, key)


if __name__ == '__main__':
    main()
