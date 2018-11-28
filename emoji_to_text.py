#!/usr/bin/python
# -*- encoding: utf-8 -*-

import emoji
import pymongo
from pymongo.errors import ConnectionFailure, DuplicateKeyError

with open('emojis.txt', 'r') as f:
    try:
        print("Connecting to MongoDB...")
        connection = pymongo.MongoClient("mongodb://localhost")
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
    if text is not None:
        try:
            emoji_text = emoji.demojize(text)
        except Exception as e:
            print(e)
            return False
        return emoji_text
