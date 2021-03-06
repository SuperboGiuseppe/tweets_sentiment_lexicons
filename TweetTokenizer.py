#!/usr/bin/python
# -*- encoding: utf-8 -*-

"""
Nicola Zotto

Step 3: "Use TweetTokenizer package to tokenize the tweet messages and remove all links and special characters, and draw histogram of the most common terms, excluding stop-words."
"""
import operator
import sys
import unicodedata
from string import punctuation

# import nltk:
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer

import draw_bar_plot as plt
# import custom modules:
import mongodb_functions as mdb

uc_punctuations = dict.fromkeys(i for i in range(sys.maxunicode) if unicodedata.category(chr(i)).startswith('P'))


def remove_punctuation(text):
    return text.translate(uc_punctuations)


def tokenizer_term_to_count(tweets, case_sensityvity=True, reduced_length=True, delete_handles=True):
    """
    Tokenizes a collection of tweets and counts the appearences of each token.
    :param tweets: a list (or any iterable) containing the tweets to be tokenized and analysed
    :param case_sensityvity: if False, the tokenizer is downcases all words except for emoticons (default to False)
    :param reduced_length: if True, the tokenizer normalizes repeated characters to only 3 characters (default to True)
    :param delete_handles: if True, the tokenizer removes user handles such as "@Erme" (default to True)
    :return: a dictionary with a term as key and the number of appearances of the term as value
    """
    tknzr = TweetTokenizer(preserve_case=case_sensityvity, strip_handles=delete_handles, reduce_len=reduced_length)
    res = dict()
    temp = []
    emojis = mdb.open_collection(collection_name='emojis')
    for tw in tweets:
        temp = tknzr.tokenize(tw)
        filtered_tweets = [w for w in temp if w.lower() not in stopwords.words('english')]
        for token in filtered_tweets:
            if str(token).find('http') != -1:
                continue
            #                                                    Variation Selector(\uFE0F)
            if remove_punctuation(token) == "" or token in punctuation or token == '\uFE0F':
                continue
            emoji = emojis.find_one({'emoji': token}, {'_id': 0, 'emoji_text': 1})
            if emoji is not None:
                token = emoji['emoji_text']
            if token in res.keys():
                res[token] += 1
            else:
                res[token] = 1
    return res


def main():
    #    tweets = ["David Bowey is dead !!!!!!!!!!!!", "@A_Name LOOOOng live David bowey !"]
    bots_fi = {'$nor': [{'user.id': 550261599}, {'user.id': 2831214083}, {'user.id': 3291286474}]}
    tweets_en = mdb.apply_query({}, {'_id': 0, 'text': 1}, collection_name='tweets_en')
    tweets_da = mdb.apply_query({}, {'_id': 0, 'translated_text': 1}, collection_name='tweets_da')
    tweets_fi = mdb.apply_query(bots_fi, {'_id': 0, 'translated_text': 1}, collection_name='tweets_fi')
    tweets_no = mdb.apply_query({}, {'_id': 0, 'translated_text': 1}, collection_name='tweets_no')
    tweets_sv = mdb.apply_query({}, {'_id': 0, 'translated_text': 1}, collection_name='tweets_sv')

    words_en = [text['text'] for text in tweets_en]
    words_da = [text['translated_text'] for text in tweets_da]
    words_fi = [text['translated_text'] for text in tweets_fi]
    words_no = [text['translated_text'] for text in tweets_no]
    words_sv = [text['translated_text'] for text in tweets_sv]

    all_words = words_en + words_da + words_fi + words_no + words_sv

    d = tokenizer_term_to_count(all_words)

    s = sorted(d.items(), key=operator.itemgetter(1), reverse=True)
    for value in s:
        print(value)

    di = dict((x, y) for x, y in s[:20])

    plt.draw_bar_plot(di, 'Distribution Of Words', 'Word', 'Occurrences', 'distribution_of_words.svg',
                      x_ticks_rotation=90)
    plt.draw_bar_plot(di, 'Distribution Of Words', 'Word', 'Occurrences', 'distribution_of_words.pdf',
                      x_ticks_rotation=90)
    plt.draw_bar_plot(di, 'Distribution Of Words', 'Word', 'Occurrences', 'distribution_of_words.png',
                      x_ticks_rotation=90)


if __name__ == "__main__": main()
