from nltk import RegexpParser
from nltk import Tree
from nltk import pos_tag
from nltk.tokenize import MWETokenizer


def extract_phrases(my_tree, phrase):
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


def retrieve_composedword():
    sentences = ["President of the United States of America",
                 "He studies Information Technology",
                 "Great Britain left the European Union"]

    grammar = "NP: {<NNP><NNP>+|<NNP><NNPS>+<IN><NNP>+}"
    cp = RegexpParser(grammar)
    res = []
    for x in sentences:

        sentence = pos_tag(x.split())
        tree = cp.parse(sentence)

        list_of_noun_phrases = extract_phrases(tree, 'NP')
        for phrase in list_of_noun_phrases:
            temp = []
            temp += ([x[0] for x in phrase.leaves()])
            res.append(temp)
    return res


def composedword_handler():
    tokenizer = MWETokenizer(retrieve_composedword())
    sentences = ["President of the United States of America",
                 "He studies Information Technology",
                 "Great Britain left the European Union"]
    print(tokenizer.tokenize(sentences[0].split()))
    print(tokenizer.tokenize(sentences[1].split()))
    print(tokenizer.tokenize(sentences[2].split()))
