#!/usr/bin/python
# -*- encoding: utf-8 -*-

__author__ = "Emre Arkan"
__copyright__ = "Copyright 2018, Project for Natural Language Processing and Text Mining, University of Oulu"

import emoji
import pymongo
from pymongo.errors import ConnectionFailure, DuplicateKeyError

import mongodb_functions as mdb

with open('emojis.txt', 'r') as f:
    try:
        print("Connecting to MongoDB...")
        connection = pymongo.MongoClient("mongodb://localhost:20000")
        print("Connecting to", 'tweets', "database...")
        db = connection['tweets']
        print("Opening", 'emojis', "collection...")
        emojis = db['emojis']
        print("Inserting items...")
        for c in f.read():
            emoji_text = emoji.demojize(c)
            if c != '\n' and c != ' ' and emoji_text[0] == ":" and emojis.find_one({'emoji_text': emoji_text}) is None:
                try:
                    emojis.insert({'emoji_text': emoji_text, 'emoji': c})
                except DuplicateKeyError:
                    continue
        print("Emojis have been imported successfully.")
    except ConnectionFailure as cf:
        print(cf.__str__())
    except FileNotFoundError as fnf:
        print(fnf.strerror)


def demojize(text):
    """
    Convert all emojis in the passed string in text format (i.e. :emoji:)
    :param text: string to be demojized
    :return: demojized string
    """
    if text is not None:
        try:
            emoji_text = emoji.demojize(text)
        except Exception as e:
            print(e)
            return False
        return emoji_text


def main():
    from insert_tweets import filter_dict
    collection_names = [key for key in filter_dict.keys()]
    for collection_name in collection_names:
        collection = mdb.open_collection(collection_name)
        if collection_name == 'tweets_en':
            tweets = collection.find({}, {'_id': 1, 'text': 1})
        else:
            tweets = collection.find({}, {'_id': 1, 'translated_text': 1})
        for tweet in tweets:
            demojized_text = demojize(list(dict(tweet).values())[1])
            collection.update({'_id': tweet['_id']}, {'$set': {'demojized_text': demojized_text}})


if __name__ == "__main__": main()
