#!/usr/bin/python
# -*- encoding: utf-8 -*-

import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
import gensim
from gensim.models.ldamodel import LdaModel
from gensim.parsing.preprocessing import STOPWORDS
import mongodb_functions as mdb
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn


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
        if token not in STOPWORDS and token[0].isalpha():
            lemmatized_tokens.append(WordNetLemmatizer().lemmatize(token[0], get_wordnet_pos(token[1])))
    return lemmatized_tokens

def print_results():
    bots_fi = {'$nor': [{'user.id': 550261599}, {'user.id': 2831214083}, {'user.id': 3291286474}]}
    words_en = [text['tokenized_text_MWETokenizer'] for text in
                mdb.apply_query({}, {'_id': 0, 'tokenized_text_MWETokenizer': 1}, collection_name='tweets_en')]
    words_da = [text['tokenized_text_MWETokenizer'] for text in
                mdb.apply_query({}, {'_id': 0, 'tokenized_text_MWETokenizer': 1}, collection_name='tweets_da')]
    words_fi = [text['tokenized_text_MWETokenizer'] for text in
                mdb.apply_query(bots_fi, {'_id': 0, 'tokenized_text_MWETokenizer': 1}, collection_name='tweets_fi')]
    words_no = [text['tokenized_text_MWETokenizer'] for text in
                mdb.apply_query({}, {'_id': 0, 'tokenized_text_MWETokenizer': 1}, collection_name='tweets_no')]
    words_sv = [text['tokenized_text_MWETokenizer'] for text in
                mdb.apply_query({}, {'_id': 0, 'tokenized_text_MWETokenizer': 1}, collection_name='tweets_sv')]

    most_active_en = [text['tokenized_text_MWETokenizer'] for text in
                      mdb.apply_query({'$or': [{'user.id': 99111435}, {'user.id': 925161145}]},
                                      {'_id': 0, 'tokenized_text_MWETokenizer': 1}, collection_name='tweets_en')]
    most_active_da = [text['tokenized_text_MWETokenizer'] for text in
                      mdb.apply_query({'$or': [{'user.id': 2872769877}, {'user.id': 906613032398225408}]},
                                      {'_id': 0, 'tokenized_text_MWETokenizer': 1}, collection_name='tweets_da')]
    most_active_fi = [text['tokenized_text_MWETokenizer'] for text in
                      mdb.apply_query({'$or': [{'user.id': 3022665861}, {'user.id': 866717150991577092}]},
                                      {'_id': 0, 'tokenized_text_MWETokenizer': 1}, collection_name='tweets_fi')]
    most_active_no = [text['tokenized_text_MWETokenizer'] for text in
                      mdb.apply_query({'$or': [{'user.id': 251308116}, {'user.id': 356852568}]},
                                      {'_id': 0, 'tokenized_text_MWETokenizer': 1}, collection_name='tweets_no')]
    most_active_sv = [text['tokenized_text_MWETokenizer'] for text in
                      mdb.apply_query({'$or': [{'user.id': 786836773829746688}, {'user.id': 5612352}]},
                                      {'_id': 0, 'tokenized_text_MWETokenizer': 1}, collection_name='tweets_sv')]

    # for each language
    lemma_en = lemmatize([item for sublist in words_en for item in sublist])
    lemma_da = lemmatize([item for sublist in words_da for item in sublist])
    lemma_fi = lemmatize([item for sublist in words_fi for item in sublist])
    lemma_no = lemmatize([item for sublist in words_no for item in sublist])
    lemma_sv = lemmatize([item for sublist in words_sv for item in sublist])
    # most active users
    ma_lemma_en = lemmatize([item for sublist in most_active_en for item in sublist])
    ma_lemma_da = lemmatize([item for sublist in most_active_da for item in sublist])
    ma_lemma_fi = lemmatize([item for sublist in most_active_fi for item in sublist])
    ma_lemma_no = lemmatize([item for sublist in most_active_no for item in sublist])
    ma_lemma_sv = lemmatize([item for sublist in most_active_sv for item in sublist])

    try:
        lda_model = LdaModel.load('lda_files/wikipedia.model')
    except EOFError as eofe:
        print(eofe.strerror)

    dictionary = gensim.corpora.Dictionary.load('lda_files/wikipedia.model.id2word')

    bow_en = dictionary.doc2bow(lemma_en)
    bow_da = dictionary.doc2bow(lemma_da)
    bow_fi = dictionary.doc2bow(lemma_fi)
    bow_no = dictionary.doc2bow(lemma_no)
    bow_sv = dictionary.doc2bow(lemma_sv)
    # most active users
    ma_bow_en = dictionary.doc2bow(ma_lemma_en)
    ma_bow_da = dictionary.doc2bow(ma_lemma_da)
    ma_bow_fi = dictionary.doc2bow(ma_lemma_fi)
    ma_bow_no = dictionary.doc2bow(ma_lemma_no)
    ma_bow_sv = dictionary.doc2bow(ma_lemma_sv)

    test_en = lda_model.get_document_topics(bow_en)
    test_da = lda_model.get_document_topics(bow_da)
    test_fi = lda_model.get_document_topics(bow_fi)
    test_no = lda_model.get_document_topics(bow_no)
    test_sv = lda_model.get_document_topics(bow_sv)
    # most active users
    ma_test_en = lda_model.get_document_topics(ma_bow_en)
    ma_test_da = lda_model.get_document_topics(ma_bow_da)
    ma_test_fi = lda_model.get_document_topics(ma_bow_fi)
    ma_test_no = lda_model.get_document_topics(ma_bow_no)
    ma_test_sv = lda_model.get_document_topics(ma_bow_sv)

    print("\nEnglish:")
    for index, prob in sorted(test_en, key=lambda var: -1 * var[1]):
        print("Probability: {}\t Topic: {}".format(prob, lda_model.print_topic(index, 5)))
    print("\nDanish:")
    for index, prob in sorted(test_da, key=lambda var: -1 * var[1]):
        print("Probability: {}\t Topic: {}".format(prob, lda_model.print_topic(index, 5)))
    print("\nFinnish:")
    for index, prob in sorted(test_fi, key=lambda var: -1 * var[1]):
        print("Probablity: {}\t Topic: {}".format(prob, lda_model.print_topic(index, 5)))
    print("\nNorwegian:")
    for index, prob in sorted(test_no, key=lambda var: -1 * var[1]):
        print("Probability: {}\t Topic: {}".format(prob, lda_model.print_topic(index, 5)))
    print("\nSwedish:")
    for index, prob in sorted(test_sv, key=lambda var: -1 * var[1]):
        print("Probablity: {}\t Topic: {}".format(prob, lda_model.print_topic(index, 5)))

    # most active users
    print("\nMost active users of English Tweets:")
    for index, prob in sorted(ma_test_en, key=lambda var: -1 * var[1]):
        print("Probablity: {}\t Topic: {}".format(prob, lda_model.print_topic(index, 5)))
    print("\nMost active users of Danish Tweets:")
    for index, prob in sorted(ma_test_da, key=lambda var: -1 * var[1]):
        print("Probablity: {}\t Topic: {}".format(prob, lda_model.print_topic(index, 5)))
    print("\nMost active users of Finnish Tweets:")
    for index, prob in sorted(ma_test_fi, key=lambda var: -1 * var[1]):
        print("Probablity: {}\t Topic: {}".format(prob, lda_model.print_topic(index, 5)))
    print("\nMost active users of Norwegian Tweets:")
    for index, prob in sorted(ma_test_no, key=lambda var: -1 * var[1]):
        print("Probablity: {}\t Topic: {}".format(prob, lda_model.print_topic(index, 5)))
    print("\nMost active users of Swedish Tweets:")
    for index, prob in sorted(ma_test_sv, key=lambda var: -1 * var[1]):
        print("Probablity: {}\t Topic: {}".format(prob, lda_model.print_topic(index, 5)))


def main():
    print_results()


if __name__ == "__main__": main()