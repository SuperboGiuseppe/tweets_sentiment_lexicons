#!/usr/bin/python
# -*- encoding: utf-8 -*-

__author__ = "Emre Arkan"
__copyright__ = "Copyright 2018, Project for Natural Language Processing and Text Mining, University of Oulu"
__email__ = "emrearkan@outlook.de"

import operator

from empath import Empath

import mongodb_functions as mdb

lexicon = Empath()


def analyze_tweets(tweets):
    """
    Analyzes given tweet or list of tweets and returns the analysis
    :param tweets: tweets to be analyzed
    :return: anlysis result
    """
    if type(tweets) is not list or tweets[0] == "" or len(tweets) == 0:
        raise ValueError("tweets must be a non-empty string or non-empty list of strings!")
    try:
        analysis = lexicon.analyze(tweets, normalize=True)
        return analysis
    except Exception as e:
        print(e)


def main():
    tweets_en = mdb.apply_query({}, {'_id': 0, 'demojized_text': 1}, collection_name='tweets_en')
    tweets_en = [text['demojized_text'] for text in tweets_en]

    tweets_da = mdb.apply_query({}, {'_id': 0, 'demojized_text': 1}, collection_name='tweets_da')
    tweets_da = [text['demojized_text'] for text in tweets_da]

    bots_fi = {'$or': [{'user.id': 550261599}, {'user.id': 2831214083}, {'user.id': 3291286474}]}
    tweets_fi = mdb.apply_query(bots_fi, {'_id': 0, 'demojized_text': 1}, collection_name='tweets_fi')
    tweets_fi = [text['demojized_text'] for text in tweets_fi]

    tweets_no = mdb.apply_query({}, {'_id': 0, 'demojized_text': 1}, collection_name='tweets_no')
    tweets_no = [text['demojized_text'] for text in tweets_no]

    tweets_sv = mdb.apply_query({}, {'_id': 0, 'demojized_text': 1}, collection_name='tweets_sv')
    tweets_sv = [text['demojized_text'] for text in tweets_sv]
    try:
        analysis_en = analyze_tweets(tweets_en)
        analysis_da = analyze_tweets(tweets_da)
        analysis_fi = analyze_tweets(tweets_fi)
        analysis_no = analyze_tweets(tweets_no)
        analysis_sv = analyze_tweets(tweets_sv)
        sorted_en = sorted(analysis_en.items(), key=operator.itemgetter(1), reverse=True)
        di_en = dict((x, y) for x, y in sorted_en[:20])
        sorted_da = sorted(analysis_da.items(), key=operator.itemgetter(1), reverse=True)
        di_da = dict((x, y) for x, y in sorted_da[:20])
        sorted_fi = sorted(analysis_fi.items(), key=operator.itemgetter(1), reverse=True)
        di_fi = dict((x, y) for x, y in sorted_fi[:20])
        sorted_no = sorted(analysis_no.items(), key=operator.itemgetter(1), reverse=True)
        di_no = dict((x, y) for x, y in sorted_no[:20])
        sorted_sv = sorted(analysis_sv.items(), key=operator.itemgetter(1), reverse=True)
        di_sv = dict((x, y) for x, y in sorted_sv[:20])
        print('English:', di_en)
        print('Danish:', di_da)
        print('Finnish:', di_fi)
        print('Norwegian:', di_no)
        print('Swedish:', di_sv)
    except ValueError as ve:
        print(ve)


if __name__ == '__main__': main()
