#!/usr/bin/python
# -*- encoding: utf-8 -*-

import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')

import gensim
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn
import mongodb_functions as mdb


def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wn.ADJ
    elif treebank_tag.startswith('V'):
        return wn.VERB
    elif treebank_tag.startswith('N'):
        return wn.NOUN
    elif treebank_tag.startswith('R'):
        return wn.ADV
    else:
        return 'n'


def lemmatize(token_list):
    lemmatized_tokens = []
    pos = nltk.pos_tag(token_list)
    for token in pos:
        lemmatized_tokens.append(WordNetLemmatizer().lemmatize(token[0], get_wordnet_pos(token[1])))
    return lemmatized_tokens


def create_bow(lemmatized_data):
    dictionary = gensim.corpora.Dictionary(lemmatized_data)
    corpus = [dictionary.doc2bow(token) for token in lemmatized_data]
    #print([[(dictionary[id], freq) for id, freq in cp] for cp in corpus[:1]])
    return dictionary, corpus


def main():
    docs = []
    docs2 = []

    words_en = [text['text'] for text in mdb.apply_query({}, {'_id': 0, 'text': 1}, collection_name='tweets_en')]
    #words_da = [text['text'] for text in mdb.apply_query({}, {'_id': 0, 'tokens': 1}, collection_name='tweets_da')]
    #words_fi = [text['text'] for text in mdb.apply_query({}, {'_id': 0, 'tokens': 1}, collection_name='tweets_fi')]
    #words_no = [text['text'] for text in mdb.apply_query({}, {'_id': 0, 'tokens': 1}, collection_name='tweets_no')]
    #words_sv = [text['text'] for text in mdb.apply_query({}, {'_id': 0, 'tokens': 1}, collection_name='tweets_sv')]

    #just here to make tests, will be removed when the tokens are in the db
    for text in words_en:
        docs2.append(gensim.utils.simple_preprocess(text))

    d1 = ['loving', 'fishing', 'saw', 'funniest', 'apples']
    d5 = ['so', 'many', 'thanks', 'nice', 'very', 'kind']
    d2 = ['many', 'thanks', 'awesome', 'truly', 'kind']
    d6 = ['testing', 'wow', 'love', 'everyone']
    d3 = ['finally', 'ridiculous', 'fun']
    d7 = ['funny', 'awesome']
    d4 = ['love', 'is', 'in', 'the', 'air']

    docs.append(lemmatize(d1))
    docs.append(lemmatize(d2))
    docs.append(lemmatize(d3))
    docs.append(lemmatize(d4))
    docs.append(lemmatize(d5))
    docs.append(lemmatize(d6))
    docs.append(lemmatize(d7))

    dict1, corpus1 = create_bow(docs2)
    dict2, corpus2 = create_bow(docs)
    lda_model_en = gensim.models.ldamodel.LdaModel(corpus=corpus1,
                                                id2word=dict1,
                                                num_topics=20,
                                                update_every=1,
                                                chunksize=100,
                                                passes=10,
                                                per_word_topics=True)

    lda_model_da = gensim.models.ldamodel.LdaModel(corpus=corpus2,
                                                    id2word=dict2,
                                                   num_topics=20,
                                                   update_every=1,
                                                   chunksize=100,
                                                   passes=10,
                                                   per_word_topics=True)

    print("English: ", lda_model_en.print_topics())
    print("Danish: ", lda_model_da.print_topics())


if __name__ == "__main__": main()