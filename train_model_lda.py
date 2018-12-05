#!/usr/bin/python
# -*- encoding: utf-8 -*-

import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
import gensim
from gensim.models.ldamodel import LdaModel
from gensim.parsing.preprocessing import STOPWORDS

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

def filter_stopwords(doc):
    filtered_tokens = []
    for token in doc:
        if token not in STOPWORDS and len(token) > 3 and token.isalpha():
            filtered_tokens.append(token)
    return filtered_tokens

#creates a dictionary and a bag of words for LDA
def create_bow(lemmatized_data):
    print('creating bow')
    dictionary = gensim.corpora.Dictionary(lemmatized_data)
    corpus = [dictionary.doc2bow(token) for token in lemmatized_data]
    return dictionary, corpus


def main():
    with open('lda_files/wikipedia_lemmatized.txt', 'r', encoding='utf-8') as wikipedia_corpus:
        try:
            corp = [filter_stopwords(wikipedia_corpus.readline().split()) for line in wikipedia_corpus]
        except FileNotFoundError as fnf:
            print(wikipedia_corpus, fnf.strerror)
    wikipedia_corpus.close()


    id2word, corpus = create_bow(corp)

    lda_model = LdaModel(corpus=corpus, id2word=id2word, num_topics=20, update_every=1, chunksize=100, passes=5, per_word_topics=True)

    lda_model.save('lda_files/wikipedia.model')


if __name__ == "__main__": main()