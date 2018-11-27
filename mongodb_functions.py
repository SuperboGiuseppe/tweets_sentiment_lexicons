#!/usr/bin/python
# -*- encoding: utf-8 -*-

import json

import pymongo
from pymongo.errors import ConnectionFailure


def import_tweets(file_path, db_name='tweets', collection_name='tweet_collection'):
    """
    To import tweets into the a mongo DB of given name and collection
    :param file_path: absolute path to the file
    :param db_name: name of the database to be written into
    :param collection_name: name of the collection which is to contain the tweets
    :return:
    """
    try:
        print("Connecting to MongoDB...")
        connection = pymongo.MongoClient("mongodb://localhost")
        print("Connecting to", db_name, "database...")
        db = connection[db_name]
        print("Opening", collection_name, "collection...")
        tweets = db[collection_name]
        print("Opening", file_path, "...")
        with open(file_path, 'r', encoding='utf8') as f:
            parsed = json.loads(f.read())
        print("Inserting items...")
        for item in parsed:
            try:
                tweets.insert(item)
            except pymongo.errors.DuplicateKeyError:
                continue
        print(len(parsed), "Tweets have been imported successfully.")
        return True
    except ConnectionFailure as cf:
        print(cf.__str__())
    except FileNotFoundError as fnf:
        print(fnf.strerror)
    except ValueError:
        print("Decoding JSON has failed")


def export_tweets_into_collection(filter, projection, to_collection_name, db_name='tweets',
                                  from_collection_name='tweet_collection'):
    """
    Applies query to a given collection and stores the result in a new collection
    :param filter: filter to be applied to the data in 'from_collection_name'
    :param projection: data fields to be written in to 'to_collection_name'
    :param to_collection_name: name target collection
    :param db_name: name of database
    :param from_collection_name: name of the base collection
    :return:
    """
    try:
        print("Connecting to MongoDB...")
        connection = pymongo.MongoClient("mongodb://localhost")
        print("Connecting to", db_name, "database...")
        db = connection[db_name]
        print("Opening", from_collection_name, "collection...")
        tweets_from = db[from_collection_name]
        data = tweets_from.find(filter, projection)
        print("Opening", to_collection_name, "collection...")
        tweets_to = db[to_collection_name]
        print("Inserting items...")
        for item in data:
            try:
                tweets_to.insert(item)
            except pymongo.errors.DuplicateKeyError:
                continue
        print("Tweets have been exported from", from_collection_name, "to", to_collection_name, "with", filter,
              projection, "filter.")
    except ConnectionFailure as cf:
        print(cf.__str__())


def get_count(collection_name, db_name='tweets'):
    try:
        print("Connecting to MongoDB...")
        connection = pymongo.MongoClient("mongodb://localhost")
        print("Connecting to", db_name, "database...")
        db = connection[db_name]
        print("Opening", collection_name, "collection...")
        tweet_collection = db[collection_name]
        return tweet_collection.count()
    except ConnectionFailure as cf:
        print(cf.__str__())


def apply_query(filter, projection, collection_name, db_name='tweets'):
    """
    :param filter: filter to be applied to the collection
    :param projection: projection to be applied to the collection
    :param collection_name: collection to be opened
    :param db_name: database to be connected to
    :return: query result
    """
    if filter is not None and projection is not None:
        try:
            print("Connecting to MongoDB...")
            connection = pymongo.MongoClient("mongodb://localhost")
            print("Connecting to", db_name, "database...")
            db = connection[db_name]
            print("Opening", collection_name, "collection...")
            collection = db[collection_name]
            data = collection.find(filter, projection)
            print("Tweets have been filtered from", collection_name, "with", filter, projection, "filter.")
            return data
        except ConnectionFailure as cf:
            print(cf.__str__())
