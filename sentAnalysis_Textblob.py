"""
Nicola Zotto
"""

import textblob as tb
import mongodb_functions as mdb
import draw_bar_plot as plt

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

def update_database(Dict_Results, collection_name):
    """
    This procedure updates the DB with the textblob results for each tweet
    :param collection_name: Name of the collection to be updated
    :param Dict_Results: Dictionary of all the results of tweets
    """
    collection = mdb.open_collection(collection_name, 'tweets')
    collection.update_many({}, {'$unset' : {'Textblob':1}})
    keys = list(Dict_Results.keys())
    for x in keys:
        collection.update({'demojized_text': x}, {'$set': {'Textblob': Dict_Results[x]}})

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
    result_en = create_dictionary(words_en)
    update_database(result_en, 'tweets_en')
    mean_en = 0
    for i in result_en:
        mean_en += result_en[i][0]
    mean_en = mean_en / len(result_en)
    pos_tweets_en = [tweet for tweet in result_en if result_en[tweet][1] == 'positive']
    neu_tweets_en = [tweet for tweet in result_en if result_en[tweet][1] == 'neutral']
    neg_tweets_en = [tweet for tweet in result_en if result_en[tweet][1] == 'negative']

    ## danish:
    result_da = create_dictionary(words_da)
    update_database(result_da, 'tweets_da')
    mean_da = 0
    for i in result_da:
        mean_da += result_da[i][0]
    mean_da = mean_da / len(result_da)
    pos_tweets_da = [tweet for tweet in result_da if result_da[tweet][1] == 'positive']
    neu_tweets_da = [tweet for tweet in result_da if result_da[tweet][1] == 'neutral']
    neg_tweets_da = [tweet for tweet in result_da if result_da[tweet][1] == 'negative']

    ## finnish:
    result_fi = create_dictionary(words_fi)
    update_database(result_fi, 'tweets_fi')
    mean_fi = 0
    for i in result_fi:
        mean_fi += result_fi[i][0]
    mean_fi = mean_fi / len(result_fi)
    pos_tweets_fi = [tweet for tweet in result_fi if result_fi[tweet][1] == 'positive']
    neu_tweets_fi = [tweet for tweet in result_fi if result_fi[tweet][1] == 'neutral']
    neg_tweets_fi = [tweet for tweet in result_fi if result_fi[tweet][1] == 'negative']

    ## norvegian:
    result_no = create_dictionary(words_no)
    update_database(result_no, 'tweets_no')
    mean_no = 0
    for i in result_no:
        mean_no += result_no[i][0]
    mean_no = mean_no / len(result_no)
    pos_tweets_no = [tweet for tweet in result_no if result_no[tweet][1] == 'positive']
    neu_tweets_no = [tweet for tweet in result_no if result_no[tweet][1] == 'neutral']
    neg_tweets_no = [tweet for tweet in result_no if result_no[tweet][1] == 'negative']

    ## swedish:
    result_sv = create_dictionary(words_sv)
    update_database(result_sv, 'tweets_sv')
    mean_sv = 0
    for i in result_sv:
        mean_sv += result_sv[i][0]
    mean_sv = mean_sv / len(result_sv)
    pos_tweets_sv = [tweet for tweet in result_sv if result_sv[tweet][1] == 'positive']
    neu_tweets_sv = [tweet for tweet in result_sv if result_sv[tweet][1] == 'neutral']
    neg_tweets_sv = [tweet for tweet in result_sv if result_sv[tweet][1] == 'negative']

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

    dict_final = {"All languages":mean_global, "English":mean_en, "Danish":mean_da, "Finnish":mean_fi, "Norvegian":mean_no, "Swedish":mean_sv}
    plt.draw_bar_plot(dict_final, 'Average scores by language', '', '', 'textblob_plot.svg', x_ticks_rotation=90)


if __name__ == "__main__": main()