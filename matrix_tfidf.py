import mongodb_functions as mdb
import math

def calculateTF(words, corpus):
    print("TF")
    tfmatrix = {}
    for y in range(len(corpus)):
        key_tag = "D" + str(y)
        tfDocument = {}
        for x in range(len(words)):
            if len(corpus[y]) != 0:
                if words[x] in corpus[y]:
                    #print(words[x])
                    temp = corpus[y].count(words[x])
                    #print(temp)
                    tfDocument[words[x]] = temp/float(len(corpus[y]))
        tfmatrix[key_tag] = tfDocument
    return tfmatrix


def calculateIDF(words, corpus):
    print("IDF")
    idfmatrix = {}
    for y in range(len(corpus)):
        key_tag = "D" + str(y)
        idfDocument = {}
        for x in range(len(words)):
            if words[x] in corpus[y]:
                df = document_frequency(words[x], corpus)
                idfDocument[words[x]] = math.log(len(corpus)/df, 10)
        idfmatrix[key_tag] = idfDocument
    return idfmatrix

def document_frequency(word, corpus):
    res = 0
    for x in range(len(corpus)):
        res += corpus[x].count(word)
    return res

def calculateTFIDF(words, corpus):
    tf = calculateTF(words, corpus)
    idf = calculateIDF(words, corpus)
    tf_idf = {}
    for y in range(len(tf)):
        key_tag = "D" + str(y)
        tf_idfDocument = {}
        for x in range(len(words)):
            if words[x] in corpus[y]:
                if words[x] in tf[key_tag]:
                    if words[x] in idf[key_tag]:
                        tf_idfDocument[words[x]] = tf[key_tag][words[x]] * idf[key_tag][words[x]]
                    else:
                        tf_idfDocument[words[x]] = 0
                else:
                    tf_idfDocument[words[x]] = 0
        tf_idf[key_tag] = tf_idfDocument
    return tf_idf

def extract_list_tokens(cursor):
    list_corpus = []
    dict = list(cursor)
    for subVal in dict:
        list_corpus.append(subVal['tokenized_text_MWETokenizer'])
    return list_corpus

def word_list(list_tokens):
    res = []
    for x in range(len(list_tokens)):
        for y in range(len(list_tokens[x])):
            if list_tokens[x][y] not in res:
                res.append(list_tokens[x][y])
    return res

def addmatrix_database(matrix, collection_name):
    collection = mdb.open_collection(collection_name, 'tweets')
    collection.insert(matrix, check_keys=False)


def matrix_TFIDF():
    cursor_tokens_en = mdb.apply_query({}, {'_id': 0, 'tokenized_text_MWETokenizer': 1}, collection_name='tweets_en')
    cursor_tokens_da = mdb.apply_query({}, {'_id': 0, 'tokenized_text_MWETokenizer': 1}, collection_name='tweets_da')
    cursor_tokens_no = mdb.apply_query({}, {'_id': 0, 'tokenized_text_MWETokenizer': 1}, collection_name='tweets_no')
    cursor_tokens_fi = mdb.apply_query({}, {'_id': 0, 'tokenized_text_MWETokenizer': 1}, collection_name='tweets_fi')
    cursor_tokens_sv = mdb.apply_query({}, {'_id': 0, 'tokenized_text_MWETokenizer': 1}, collection_name='tweets_sv')
    list_tokens_en = extract_list_tokens(cursor_tokens_en)
    list_tokens_da = extract_list_tokens(cursor_tokens_da)
    list_tokens_no = extract_list_tokens(cursor_tokens_no)
    list_tokens_sv = extract_list_tokens(cursor_tokens_sv)
    list_tokens_fi = extract_list_tokens(cursor_tokens_fi)
    words_en = word_list(list_tokens_en)
    words_da = word_list(list_tokens_da)
    words_no = word_list(list_tokens_no)
    words_sv = word_list(list_tokens_sv)
    words_fi = word_list(list_tokens_fi)
    print("Calculating TF-IDF matrix for english tweets...")
    tfidf_en = calculateTFIDF(words_en, list_tokens_en)
    print("Creating tfidf_en collection with data...")
    mdb.add_collection('tfidf_en')
    addmatrix_database(tfidf_en, 'tfidf_en')
    tfidf_en = 0
    print("Calculating TF-IDF matrix for danish tweets...")
    tfidf_da = calculateTFIDF(words_da, list_tokens_da)
    print("Creating tfidf_da collection with data...")
    mdb.add_collection('tfidf_da')
    addmatrix_database(tfidf_da, 'tfidf_da')
    tfidf_da = 0
    print("Calculating TF-IDF matrix for finnish tweets...")
    tfidf_fi = calculateTFIDF(words_fi, list_tokens_fi)
    print("Creating tfidf_fi collection with data...")
    mdb.add_collection('tfidf_fi')
    addmatrix_database(tfidf_fi, 'tfidf_fi')
    tfidf_fi = 0
    print("Calculating TF-IDF matrix for swedish tweets...")
    tfidf_sv = calculateTFIDF(words_sv, list_tokens_sv)
    print("Creating tfidf_sv collection with data...")
    mdb.add_collection('tfidf_sv')
    addmatrix_database(tfidf_sv, 'tfidf_sv')
    tfidf_sv = 0
    print("Calculating TF-IDF matrix for norwegian tweets...")
    tfidf_no = calculateTFIDF(words_no, list_tokens_no)
    print("Creating tfidf_no collection with data...")
    mdb.add_collection('tfidf_no')
    addmatrix_database(tfidf_no, 'tfidf_no')
    tfidf_no = 0


if __name__ == '__main__':
    matrix_TFIDF()