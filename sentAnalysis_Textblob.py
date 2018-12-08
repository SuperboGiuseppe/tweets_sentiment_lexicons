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
    :return: a tuple, the sentiment score and the perceived sentiment of the inputed tweet
    """
    tweetblob = tb.TextBlob(tweet)
    if tweetblob.sentiment.polarity > 0:
        return (tweetblob.sentiment.polarity, 'positive')
    elif tweetblob.sentiment.polarity == 0:
        return (tweetblob.sentiment.polarity, 'neutral')
    else:
        return (tweetblob.sentiment.polarity, 'negative')


def main():
    bots_fi = {'$nor': [{'user.id': 550261599}, {'user.id': 2831214083}, {'user.id': 3291286474}]}
    tweets_en = mdb.apply_query({}, {'_id': 0, 'demojized_text': 1}, collection_name='tweets_en')
    tweets_da = mdb.apply_query({}, {'_id': 0, 'demojized_text': 1}, collection_name='tweets_da')
    tweets_fi = mdb.apply_query(bots_fi, {'_id': 0, 'demojized_text': 1}, collection_name='tweets_fi')
    tweets_no = mdb.apply_query({}, {'_id': 0, 'demojized_text': 1}, collection_name='tweets_no')
    tweets_sv = mdb.apply_query({}, {'_id': 0, 'demojized_text': 1}, collection_name='tweets_sv')

    words_en = [text['demojized_text'] for text in tweets_en]
    words_da = [text['demojized_text'] for text in tweets_da]
    words_fi = [text['demojized_text'] for text in tweets_fi]
    words_no = [text['demojized_text'] for text in tweets_no]
    words_sv = [text['demojized_text'] for text in tweets_sv]
    all_words = words_en + words_da + words_fi + words_no + words_sv

    ## english:
    result = create_dictionary(words_en)
    mean_en = 0
    for i in result:
        mean_en += result[i][0]
    mean_en = mean_en / len(result)
    pos_tweets_en = [tweet for tweet in result if result[tweet][1] == 'positive']
    neu_tweets_en = [tweet for tweet in result if result[tweet][1] == 'neutral']
    neg_tweets_en = [tweet for tweet in result if result[tweet][1] == 'negative']

    ## danish:
    result = create_dictionary(words_da)
    mean_da = 0
    for i in result:
        mean_da += result[i][0]
    mean_da = mean_da / len(result)
    pos_tweets_da = [tweet for tweet in result if result[tweet][1] == 'positive']
    neu_tweets_da = [tweet for tweet in result if result[tweet][1] == 'neutral']
    neg_tweets_da = [tweet for tweet in result if result[tweet][1] == 'negative']

    ## finnish:
    result = create_dictionary(words_fi)
    mean_fi = 0
    for i in result:
        mean_fi += result[i][0]
    mean_fi = mean_fi / len(result)
    pos_tweets_fi = [tweet for tweet in result if result[tweet][1] == 'positive']
    neu_tweets_fi = [tweet for tweet in result if result[tweet][1] == 'neutral']
    neg_tweets_fi = [tweet for tweet in result if result[tweet][1] == 'negative']

    ## norvegian:
    result = create_dictionary(words_no)
    mean_no = 0
    for i in result:
        mean_no += result[i][0]
    mean_no = mean_no / len(result)
    pos_tweets_no = [tweet for tweet in result if result[tweet][1] == 'positive']
    neu_tweets_no = [tweet for tweet in result if result[tweet][1] == 'neutral']
    neg_tweets_no = [tweet for tweet in result if result[tweet][1] == 'negative']

    ## swedish:
    result = create_dictionary(words_sv)
    mean_sv = 0
    for i in result:
        mean_sv += result[i][0]
    mean_sv = mean_sv / len(result)
    pos_tweets_sv = [tweet for tweet in result if result[tweet][1] == 'positive']
    neu_tweets_sv = [tweet for tweet in result if result[tweet][1] == 'neutral']
    neg_tweets_sv = [tweet for tweet in result if result[tweet][1] == 'negative']

    ## all languages:
    result = create_dictionary(all_words)
    mean_global = 0
    for i in result:
        mean_global += result[i][0]
    mean_global = mean_global / len(result)
    pos_tweets_global = [tweet for tweet in result if result[tweet][1] == 'positive']
    neu_tweets_global = [tweet for tweet in result if result[tweet][1] == 'neutral']
    neg_tweets_global = [tweet for tweet in result if result[tweet][1] == 'negative']

    ## printing the results:
    print("positive tweets percentage:")
    print("all languages: ", len(pos_tweets_global) / len(all_words), "english: ", len(pos_tweets_en) / len(words_en),
          "danish: ", len(pos_tweets_da) / len(words_da), "finnish: ", len(pos_tweets_fi) / len(words_fi),
          "norvegian: ", len(pos_tweets_no) / len(words_no), "swedish: ", len(pos_tweets_sv) / len(words_sv))
    print("neutral tweets percentage:")
    print("all languages: ", len(neu_tweets_global) / len(all_words), "english: ", len(neu_tweets_en) / len(words_en),
          "danish: ", len(neu_tweets_da) / len(words_da), "finnish: ", len(neu_tweets_fi) / len(words_fi),
          "norvegian: ", len(neu_tweets_no) / len(words_no), "swedish: ", len(neu_tweets_sv) / len(words_sv))
    print("negative tweets percentage:")
    print("all languages: ", len(neg_tweets_global) / len(all_words), "english: ", len(neg_tweets_en) / len(words_en),
          "danish: ", len(neg_tweets_da) / len(words_da), "finnish: ", len(neg_tweets_fi) / len(words_fi),
          "norvegian: ", len(neg_tweets_no) / len(words_no), "swedish: ", len(neg_tweets_sv) / len(words_sv))
    print()
    print("average scores by language:")
    print("global score: ", mean_global)
    print("english score: ", mean_en)
    print("danish score: ", mean_da)
    print("finnish score: ", mean_fi)
    print("norvegian score: ", mean_no)
    print("swedish score: ", mean_sv)


if __name__ == "__main__": main()
