#!/usr/bin/python
# -*- encoding: utf-8 -*-

import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
import gensim
from gensim.models.ldamodel import LdaModel
import mongodb_functions as mdb
from train_model_lda import lemmatize, create_bow


def main():
    #this is a WIP and will be updated once the tokens are in the db
    doc_en = []
    lemma_en = []
    words_en = [text['text'] for text in mdb.apply_query({}, {'_id': 0, 'text': 1}, collection_name='tweets_en')]
    #words_da = [text['text'] for text in mdb.apply_query({}, {'_id': 0, 'tokens': 1}, collection_name='tweets_da')]
    #words_fi = [text['text'] for text in mdb.apply_query({}, {'_id': 0, 'tokens': 1}, collection_name='tweets_fi')]
    #words_no = [text['text'] for text in mdb.apply_query({}, {'_id': 0, 'tokens': 1}, collection_name='tweets_no')]
    #words_sv = [text['text'] for text in mdb.apply_query({}, {'_id': 0, 'tokens': 1}, collection_name='tweets_sv')]

    lda_model = LdaModel.load('lda_files/twitter.model')

    # just here to make tests, will be removed when the tokens are in the db
    for text in words_en:
        doc_en.append(gensim.utils.simple_preprocess(text))

    for text in doc_en:
        lemma_en.append(lemmatize(text))

    dictionary = gensim.corpora.Dictionary.load('lda_files/twitter.model.id2word')

    #idk how to display something humanly readable. will figure it out soon
    bow = dictionary.doc2bow(lemma_en[2])
    test = lda_model[bow]

    print(test)

if __name__ == "__main__": main()