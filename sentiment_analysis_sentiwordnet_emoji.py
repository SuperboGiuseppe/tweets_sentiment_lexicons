import csv
import re
import string
import pymongo

# Source: http://stackoverflow.com/questions/19790188/expanding-english-language-contractions-in-python
# Contractions to be used in tokenizer for possessives
contractions = {
    "ain't": "am not",
    "aren't": "are not",
    "can't": "cannot",
    "can't've": "cannot have",
    "'cause": "because",
    "could've": "could have",
    "couldn't": "could not",
    "couldn't've": "could not have",
    "didn't": "did not",
    "doesn't": "does not",
    "don't": "do not",
    "hadn't": "had not",
    "hadn't've": "had not have",
    "hasn't": "has not",
    "haven't": "have not",
    "he'd": "he would",
    "he'd've": "he would have",
    "he'll": "he will",
    "he'll've": "he will have",
    "he's": "he is",
    "how'd": "how did",
    "how'd'y": "how do you",
    "how'll": "how will",
    "how's": "how is",
    "I'd": "I would",
    "I'd've": "I would have",
    "I'll": "I will",
    "I'll've": "I will have",
    "I'm": "I am",
    "I've": "I have",
    "isn't": "is not",
    "it'd": "it had",
    "it'd've": "it would have",
    "it'll": "it will",
    "it'll've": "it will have",
    "it's": "it is",
    "let's": "let us",
    "ma'am": "madam",
    "mayn't": "may not",
    "might've": "might have",
    "mightn't": "might not",
    "mightn't've": "might not have",
    "must've": "must have",
    "mustn't": "must not",
    "mustn't've": "must not have",
    "needn't": "need not",
    "needn't've": "need not have",
    "o'clock": "of the clock",
    "oughtn't": "ought not",
    "oughtn't've": "ought not have",
    "shan't": "shall not",
    "sha'n't": "shall not",
    "shan't've": "shall not have",
    "she'd": "she had",
    "she'd've": "she would have",
    "she'll": "she will",
    "she'll've": "she will have",
    "she's": "she is",
    "should've": "should have",
    "shouldn't": "should not",
    "shouldn't've": "should not have",
    "so've": "so have",
    "so's": "so is",
    "that'd": "that had",
    "that'd've": "that would have",
    "that's": "that is",
    "there'd": "there had",
    "there'd've": "there would have",
    "there's": "there is",
    "they'd": "they would",
    "they'd've": "they would have",
    "they'll": "they will",
    "they'll've": "they will have",
    "they're": "they are",
    "they've": "they have",
    "to've": "to have",
    "wasn't": "was not",
    "we'd": "we had",
    "we'd've": "we would have",
    "we'll": "we will",
    "we'll've": "we will have",
    "we're": "we are",
    "we've": "we have",
    "weren't": "were not",
    "what'll": "what will",
    "what'll've": "what will have",
    "what're": "what are",
    "what's": "what is",
    "what've": "what have",
    "when's": "when is",
    "when've": "when have",
    "where'd": "where did",
    "where's": "where is",
    "where've": "where have",
    "who'll": "who will",
    "who'll've": "who will have",
    "who's": "who is",
    "who've": "who have",
    "why's": "why is",
    "why've": "why have",
    "will've": "will have",
    "won't": "will not",
    "won't've": "will not have",
    "would've": "would have",
    "wouldn't": "would not",
    "wouldn't've": "would not have",
    "y'all": "you all",
    "y'all'd": "you all would",
    "y'all'd've": "you all would have",
    "y'all're": "you all are",
    "y'all've": "you all have",
    "you'd": "you had",
    "you'd've": "you would have",
    "you'll": "you will",
    "you'll've": "you will have",
    "you're": "you are",
    "you've": "you have"
}

tweet_text = dict()


# read SentiWordNet
def create_senti_emoji_dict():
    scores_file = open("SentiWordNet.txt", "r")
    scores_dict = dict()

    # add the word into the dictionary with the positive score - the negative score
    for line in scores_file:
        line = line.strip()
        if line[0] != "#":
            tmp = line.split()
            word = tmp[4].split("#")
            scores_dict[str(word[0])] = float(tmp[2]) - float(tmp[3])

    return scores_dict


def clean_tweet(tweet):
    new_tweet = re.sub(r"http\S+", "", tweet)
    new_tweet = re.sub(r"@\S+", "", new_tweet)
    new_tweet.replace('#', '')
    return new_tweet


# Function to tokenize text
def tokenizeText(line, wordNet_dict):
    words = line.strip().split()
    tmplist = list()
    returnList = list()
    for word in words:
        if "'" in word:
            if word in contractions:
                expansion = contractions[word]
                all_words = expansion.split()
                for all_word in all_words:
                    tmplist.append(all_word)
        else:
            tmplist.append(word)
    final_tokenized_list = list()
    for tmp_words in tmplist:
        replace_punctuation = str.maketrans(string.punctuation, ' ' * len(string.punctuation))
        tmp_words = tmp_words.translate(replace_punctuation)
        tmp_word = tmp_words.split()
        final_tokenized_list.extend(tmp_word)
    return final_tokenized_list


# returns the score of one tweet
def sentimentAnalysis(tweet_list, scores_dict):
    count = 0.0
    tweet_score = 0.0

    # iterate through each word in a single tweet and get the score from the sentiment library
    for each_tweet_word in tweet_list:
        if each_tweet_word.lower() in scores_dict:
            tweet_score = tweet_score + scores_dict[each_tweet_word.lower()]
            count = count + 1.0

    return tweet_score


def main(db_name='tweets'):
    a=0
    scores_dict = create_senti_emoji_dict()
    connection = pymongo.MongoClient("mongodb://localhost:20000")
    db = connection[db_name]
    bots_fi = {'$nor': [{'user.id': 550261599}, {'user.id': 2831214083}, {'user.id': 3291286474}]}
    tweets_da = db['tweets_da']
    tweets_fi = db['tweets_fi']
    tweets_en = db['tweets_en']
    tweets_no = db['tweets_no']
    tweets_sv = db['tweets_sv']
    try:
        for tweet in tweets_da.find():
            tokenized_tweets = tokenizeText(clean_tweet(tweet["demojized_text"]), scores_dict)
            sentiScore = sentimentAnalysis(tokenized_tweets, scores_dict)
            tweets_da.update({"_id": tweet["_id"]}, {'$set': {"SentiWordNet": sentiScore}})
        for tweet in tweets_fi.find(bots_fi):
            tokenized_tweets = tokenizeText(clean_tweet(tweet["demojized_text"]), scores_dict)
            sentiScore = sentimentAnalysis(tokenized_tweets, scores_dict)
            tweets_fi.update({"_id": tweet["_id"]}, {'$set': {"SentiWordNet": sentiScore}})
        for tweet in tweets_en.find():
            tokenized_tweets = tokenizeText(clean_tweet(tweet["demojized_text"]), scores_dict)
            sentiScore = sentimentAnalysis(tokenized_tweets, scores_dict)
            tweets_en.update({"_id": tweet["_id"]}, {'$set': {"SentiWordNet": sentiScore}})
        for tweet in tweets_no.find():
            tokenized_tweets = tokenizeText(clean_tweet(tweet["demojized_text"]), scores_dict)
            sentiScore = sentimentAnalysis(tokenized_tweets, scores_dict)
            tweets_no.update({"_id": tweet["_id"]}, {'$set': {"SentiWordNet": sentiScore}})
        for tweet in tweets_sv.find():
            tokenized_tweets = tokenizeText(clean_tweet(tweet["demojized_text"]), scores_dict)
            sentiScore = sentimentAnalysis(tokenized_tweets, scores_dict)
            tweets_sv.update({"_id": tweet["_id"]}, {'$set': {"SentiWordNet": sentiScore}})
    except ValueError:
        print(ValueError)

if __name__ == '__main__':
    main()
