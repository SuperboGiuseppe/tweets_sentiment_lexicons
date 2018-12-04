from nltk.tokenize import MWETokenizer
from nltk import Tree
from nltk import RegexpParser
from nltk import pos_tag
import mongodb_functions as mdb
import wordninja

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


def composedword_handler(corpus_cursor, field):
    """
    Extract corpus from the DB of tweets and create a lexicon of composed words from it. MWETokenizer is going
    to merge all the tokens which are composed by multi word expressions of the lexicon that we have retrieved
    by calling retrieve_composedword function and given to MWETokenizer.
    :return: The list of tokens with most of the composed word handled.
    """
    corpus = []
    corpus_dict = list(corpus_cursor)
    for subVal in corpus_dict:
        corpus.append(subVal[field])
    res = []
    tokenizer = MWETokenizer(retrieve_composedword(corpus))
    for x in range(len(corpus)):
        # print(tokenizer.tokenize(corpus[x].split()))
        temp = tokenizer.tokenize(corpus[x].split())
        temp2 = temp.copy()
        x = 0
        for y in range(len(temp)):
            if temp[y][0] == '@':
                del temp2[x]
                x = x - 1
            if temp[y][0] == '#':
                del temp2[x]
                temp2[x:x] = wordninja.split(temp[y])
                x += len(wordninja.split(temp[y])) - 1
            if str(temp[y]).find('http') != -1:
                del temp2[x]
                x = x - 1
            # print(temp2)
            x += 1
        # print(temp2)
        res.append(temp2)
    return res


def ID_extractor(cursor_ID):
    res = []
    temp = list(cursor_ID)
    for subVal in temp:
        res.append(subVal['_id'])
    return res


def update_database(ListID, List_Tokens, collection_name):
    collection = mdb.open_collection(collection_name, 'tweets')
    for x in range(len(ListID)):
        collection.update({'_id': ListID[x]}, {'$set': {'tokenized_text_MWETokenizer': List_Tokens[x]}})


def main():
    corpus_cursor_en = mdb.apply_query({}, {'_id': 0, 'demojized_text': 1}, collection_name='tweets_en')
    corpus_cursor_da = mdb.apply_query({}, {'_id': 0, 'demojized_text': 1}, collection_name='tweets_da')
    corpus_cursor_no = mdb.apply_query({}, {'_id': 0, 'demojized_text': 1}, collection_name='tweets_no')
    corpus_cursor_fi = mdb.apply_query({}, {'_id': 0, 'demojized_text': 1}, collection_name='tweets_fi')
    corpus_cursor_sv = mdb.apply_query({}, {'_id': 0, 'demojized_text': 1}, collection_name='tweets_sv')
    tokenized_tweets_en = composedword_handler(corpus_cursor_en, 'demojized_text')
    tokenized_tweets_da = composedword_handler(corpus_cursor_da, 'demojized_text')
    tokenized_tweets_no = composedword_handler(corpus_cursor_no, 'demojized_text')
    tokenized_tweets_fi = composedword_handler(corpus_cursor_fi, 'demojized_text')
    tokenized_tweets_sv = composedword_handler(corpus_cursor_sv, 'demojized_text')
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
    main()