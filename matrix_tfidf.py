def calculateTF(wordDict, corpus):
    tfDict = {}
    numDocuments = len(corpus)
    for word,count in wordDict.items():
        tfDict[word] = count/float(numDocuments)
    return tfDict

def calculateIDF(corpus):
    import math
    idfDict = {}
    N = len(corpus)
    idfdict = dict.fromkeys(corpus[0].keys(), 0)
    for doc in corpus:
        for word, val in doc.items():
            if val > 0:
                idfDict[word] +=1

    for word, val in idfDict.items():
        idfDict[word] = math.log10(N/ float(val))

    return idfDict

def calculateTFID(tfBow, idfs):
    tfidf = {}
    for word, val in tfBow.items():
        tfidf[word] = val * idfs[word]
    return tfidf


