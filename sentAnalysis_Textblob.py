"""
Nicola Zotto
"""

import textblob as tb
import mongodb_functions as mdb

def create_dictionary(tweet_list):
    """
    Transforms a list of tweets into a dictionary with the tweet text as key and it's sentiment as value.
    :param tweet_list: a list of non-tokenized tweets.
    :return: a dictionary associating a tweet to it's perceived sentiment
    """
    result = dict()
    for tweet in tweet_list:
        result[tweet] = get_tweet_sentiment(tweet)
    return result

def get_tweet_sentiment(tweet):
    """ 
    Classifies sentiment of a single tweet using textblob's sentiment method 
    :param tweet: a non-tokenized tweets.
    :return: the perceived sentiment of the inputed tweet
    """
    tweetblob = tb.TextBlob(tweet)     
    if tweetblob.sentiment.polarity > 0: 
        return 'positive'
    elif tweetblob.sentiment.polarity == 0:
        return 'neutral'
    else: 
        return 'negative'

def main():

    bots_fi = {'$nor': [{'user.id': 550261599}, {'user.id': 2831214083}]}
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

    result = create_dictionary(all_words)
    
    pos_tweets = [tweet for tweet in result if result[tweet] == 'positive']
    neu_tweets = [tweet for tweet in result if result[tweet] == 'neutral']
    neg_tweets = [tweet for tweet in result if result[tweet] == 'negative']

    ## What do we do with it now? a plot?

    print("positive tweets: ", len(pos_tweets))
    print("neutral tweets: ", len(neu_tweets))
    print("negative tweets: ", len(neg_tweets))
    
if __name__ == "__main__": main()
