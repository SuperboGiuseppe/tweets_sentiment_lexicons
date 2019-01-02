from nltk.tokenize import MWETokenizer
from nltk.corpus import stopwords
from nltk import Tree
from nltk import RegexpParser
from nltk import pos_tag
import mongodb_functions as mdb
import wordninja
import string

"""
Giuseppe Superbo

Step 6.1: Use MWETokenizer in order to handle composed words
"""


def extract_phrases(my_tree, phrase):
    """
    This function retrieves all the phrase that we need to analyze in order to
    retrieve all the composed words of proper names.
    :param my_tree: Parsing tree of the POS contained in our corpus
    :param phrase: The type of phrase in which we want to retrieve our composed words
    :return: The function returns all the phrases that may contain composed words
    """
    my_phrases = []
    if my_tree.label() == phrase:
        my_phrases.append(my_tree.copy(True))

    for child in my_tree:
        if type(child) is Tree:
            list_of_phrases = extract_phrases(child, phrase)
            if len(list_of_phrases) > 0:
                my_phrases.extend(list_of_phrases)
                # print(my_phrases)
    return my_phrases


def retrieve_composedword(corpus):
    """
    This function group all the composed words found in the corpus by selecting only the noun phrases.
    All the combinations of proper names are grouped in one single list.
    :param corpus: All the documents where we can retrieve composed words.
    :return: List of composed words found in the corpus
    """
    grammar = "NP: {<NNP><NNP>+|(<NNP>|<NNPS>)+<IN><NNP>+}"
    cp = RegexpParser(grammar)
    res = []
    for x in range(len(corpus)):
        document = pos_tag(corpus[x].split())
        tree = cp.parse(document)
        list_of_noun_phrases = extract_phrases(tree, 'NP')
        for phrase in list_of_noun_phrases:
            temp = []
            temp += ([x[0] for x in phrase.leaves()])
            res.append(temp)
    return res


def tokenizer_composedword(corpus_cursor, field):
    """
    Extract corpus from the DB of tweets and create a lexicon of composed words from it. MWETokenizer is going
    to merge all the tokens which are composed by multi word expressions of the lexicon that we have retrieved
    by calling retrieve_composed word function and given to MWETokenizer. Also some filtering like removing
    punctuation, stopwords, tag links and http links are removed in order to have cleaner result.
    :param: corpus_cursor:retrieved from a specific query executed on the DB
    :param: field: is the field of the result of the query that we want to tokenize
    :return: The list of tokens with most of the composed word handled.
    """
    stop_words = set(stopwords.words('english'))
    punctuation = set((string.punctuation.replace("_","")).replace(":",""))
    corpus = []
    corpus_dict = list(corpus_cursor)
    for subVal in corpus_dict:
        corpus.append(subVal[field])
    res = []
    tokenizer = MWETokenizer(retrieve_composedword(corpus))
    for x in range(len(corpus)):
        tweet = corpus[x]
        tweet = tweet.replace("https ", "https:")
        print(tokenizer.tokenize(tweet.split()))
        temp = tokenizer.tokenize(tweet.split())
        temp = [item for item in temp if item[0] != '@' and str(item).find('https') == -1 and item not in stop_words and item not in punctuation]
        for i, y in enumerate(temp):
            if y[0] == '#':
                del temp[i]
                temp[i:i] = wordninja.split(y)
        for i,y in enumerate(temp):
            flag = 0
            if y.find(":") != -1:
                if y.find("_") != -1:
                    flag = 1
                temp[i] = temp[i].replace(":","")
                temp[i] = temp[i].replace("_","")
                if flag == 1:
                    remove_index = len(wordninja.split(temp[i]))
                    temp[i:i] = wordninja.split(temp[i])
                    del temp[i + remove_index]
                #continue
        for i, y in enumerate(temp):
            for c in punctuation:
                temp[i] = temp[i].replace(c, '')
            #x += 1
        temp = [item for item in temp if len(item) > 2]
        print(temp)
        res.append(temp)
    return res


def ID_extractor(cursor_ID):
    """
    In order to update the DB with the new tokenized text, we need to extract the list of IDs
    of all the tweets of the corpus
    :param cursor_ID: cursor which contains all the IDs retrieved from the query
    :return: List of IDs ready to be used during the update
    """
    res = []
    temp = list(cursor_ID)
    for subVal in temp:
        res.append(subVal['_id'])
    return res


def update_database(ListID, List_Tokens, collection_name):
    """
    This procedure updates the DB with the tokenized tweets
    :param ListID: List that contains all the IDs of the tokenized tweets
    :param List_Tokens: Tokenized tweets
    :param collection_name: Name of the collection to be updated
    """
    collection = mdb.open_collection(collection_name, 'tweets')
    for x in range(len(ListID)):
        collection.update({'_id': ListID[x]}, {'$set': {'tokenized_text_MWETokenizer': List_Tokens[x]}})


def composed_word_handler():
    corpus_cursor_en = mdb.apply_query({}, {'_id': 0, 'demojized_text': 1}, collection_name='tweets_en')
    corpus_cursor_da = mdb.apply_query({}, {'_id': 0, 'demojized_text': 1}, collection_name='tweets_da')
    corpus_cursor_no = mdb.apply_query({}, {'_id': 0, 'demojized_text': 1}, collection_name='tweets_no')
    corpus_cursor_fi = mdb.apply_query({}, {'_id': 0, 'demojized_text': 1}, collection_name='tweets_fi')
    corpus_cursor_sv = mdb.apply_query({}, {'_id': 0, 'demojized_text': 1}, collection_name='tweets_sv')
    tokenized_tweets_en = tokenizer_composedword(corpus_cursor_en, 'demojized_text')
    tokenized_tweets_da = tokenizer_composedword(corpus_cursor_da, 'demojized_text')
    tokenized_tweets_no = tokenizer_composedword(corpus_cursor_no, 'demojized_text')
    tokenized_tweets_fi = tokenizer_composedword(corpus_cursor_fi, 'demojized_text')
    tokenized_tweets_sv = tokenizer_composedword(corpus_cursor_sv, 'demojized_text')
    ID_cursor_en = mdb.apply_query({}, {'_id': 1}, collection_name='tweets_en')
    ID_cursor_da = mdb.apply_query({}, {'_id': 1}, collection_name='tweets_da')
    ID_cursor_sv = mdb.apply_query({}, {'_id': 1}, collection_name='tweets_sv')
    ID_cursor_no = mdb.apply_query({}, {'_id': 1}, collection_name='tweets_no')
    ID_cursor_fi = mdb.apply_query({}, {'_id': 1}, collection_name='tweets_fi')
    ListID_en = ID_extractor(ID_cursor_en)
    ListID_da = ID_extractor(ID_cursor_da)
    ListID_sv = ID_extractor(ID_cursor_sv)
    ListID_no = ID_extractor(ID_cursor_no)
    ListID_fi = ID_extractor(ID_cursor_fi)
    update_database(ListID_en, tokenized_tweets_en, 'tweets_en')
    update_database(ListID_da, tokenized_tweets_da, 'tweets_da')
    update_database(ListID_fi, tokenized_tweets_fi, 'tweets_fi')
    update_database(ListID_no, tokenized_tweets_no, 'tweets_no')
    update_database(ListID_sv, tokenized_tweets_sv, 'tweets_sv')


if __name__ == '__main__':
    composed_word_handler()