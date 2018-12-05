#!/usr/bin/python
# -*- encoding: utf-8 -*-

import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
import gensim
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn
from nltk.corpus import twitter_samples
from gensim.parsing.preprocessing import STOPWORDS
from gensim.models.ldamodel import LdaModel

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


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
        if token[0] not in STOPWORDS:
            lemmatized_tokens.append(WordNetLemmatizer().lemmatize(token[0], get_wordnet_pos(token[1])))
    return lemmatized_tokens


def create_bow(lemmatized_data):
    print('creating bow')
    dictionary = gensim.corpora.Dictionary(lemmatized_data)
    corpus = [dictionary.doc2bow(token) for token in lemmatized_data]
    #print([[(dictionary[id], freq) for id, freq in cp] for cp in corpus[:1]])
    return dictionary, corpus


def main():
    with open('lda_files/wikipedia_lemmatized.txt', 'r', encoding='utf-8') as wikipedia_corpus:
        try:
            corp = [wikipedia_corpus.readline().split() for line in wikipedia_corpus]
        except FileNotFoundError as fnf:
            print(wikipedia_corpus, fnf.strerror)
    wikipedia_corpus.close()

    print('lemmatizing')
    for text in raw_text:
        lda_corpus.append(lemmatize(text))

    id2word, corpus = create_bow(lda_corpus)

    lda_model = LdaModel(corpus=corpus, id2word=id2word, num_topics=20, update_every=1, chunksize=100, passes=10, per_word_topics=True)

    lda_model.save('lda_files/twitter.model')


if __name__ == "__main__": main()