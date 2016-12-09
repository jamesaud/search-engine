from collections import Counter
import os
import re
import math

class Document(object):
    # Static variable, shared by all Document objects
    word_docs = {}  # Word as key, list of documents that word appears in as value
    idf_scores = Counter()  # Word as key, score as value

    """
    word_counts words: counts
    total_words  total number of words in document
    title    title of the document

    """
    def __init__(self):
        self.word_counts = Counter()
        self.total_words = None
        self.title = None
        self.name = None
        self.url = None
        self.tf_scores = Counter()  # Word as key, score as value
        self.tf_idf_scores = Counter() # Word as key, score as value


    def __eq__(self, other):
        return self.name == other.name



def parse_index(object):
    pass




def parse_docs_dat(file, document_list):

    if not os.path.isfile(file):
        raise ValueError("Path Incorrect")

    with open(file) as f:
        lines = f.readlines()

    for line in lines:
        split = line.split()
        doc = Document() # Creates a new Document object
        doc.name = split[0]
        doc.total_words = int(split[1])
        doc.title = ' '.join(split[2:-1])
        doc.url = split[-1]
        document_list[doc.name] = doc
    return document_list


def update_word_docs(word, list_of_names):
    Document.word_docs[word] = len(list_of_names)


#List of names and counts are two lists of equal lengths.
def update_docs(word, list_of_names, counts, document_list):
    for name, count in zip(list_of_names, counts):
        doc = document_list.get(name, None)
        if doc:
            doc.word_counts[word] = int(count)


def parse_invindex(file, document_list):
    if not os.path.isfile(file):
        raise ValueError("Path Incorrect")

    with open(file) as f:
        lines = f.readlines()

    for line in lines:
        try:
            split = line.replace('b', '').replace("'", "").replace(', ', ',').split()
            word = split[0]
            list_of_names = split[1].replace('[', '').replace(']','').split(',')
            counts = split[2].replace('[', '').replace(']','').split(',')
            update_word_docs(word, list_of_names)
            update_docs(word, list_of_names, counts, document_list)

        except IndexError:
            pass

    return document_list

def calculate_tf(list_documents):
    for doc in list_documents:
        total_words = doc.total_words
        for word, times in doc.word_counts.items():
            doc.tf_scores[word] = times/total_words

def calculate_idf(list_documents):
    total_docs = len(list_documents)
    for word, num_docs in Document.word_docs.items():
        idf = math.log(total_docs/num_docs)
        Document.idf_scores[word] = idf


def calculate_tf_idf(list_documents):
    for doc in list_documents:
        tf_scores = doc.tf_scores
        idf_scores = doc.idf_scores
        for word in tf_scores:
            tf_idf_score = tf_scores[word] * idf_scores[word]
            doc.tf_idf_scores[word] = tf_idf_score


def find_final_score(term_list, list_documents):
    pass

document_list = {}  # Key is document name, value is the Document object
path = os.getcwd()

dat_path = os.path.join(os.path.join(path, 'pages'), 'docs.dat')
document_list = parse_docs_dat(dat_path, document_list)

inv_path = os.path.join(os.path.join(path, 'pages'), 'invindex.dat')
document_list = parse_invindex(inv_path, document_list)

documents = list(document_list.values())
calculate_tf(documents)
calculate_idf(documents)
calculate_tf_idf(documents)

d = documents[0]
#print(d.tf_scores)
#print(d.tf_idf_scores)
k = d.tf_idf_scores
top25 = Counter(k)
print top25.most_common(25)
