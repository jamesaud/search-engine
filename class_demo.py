import sys
import pdb
import os
from HTMLParser import HTMLParser
from nltk.corpus import stopwords
from import PorterStemmer


STOPWORDS = set(s.lower() for s in stopwords.words('english'))
STEMMER = PorterStemmer()
INVERTED_IDX_PATH = 'invindex.dat'
DOC_IDX_PATH = 'docs.dat'

def main():
    
    args = parse_args()
    if args_is_valid(args):
        print 'Usage: python index.py pages_dir/ index.dat'
        print 'pages_dir/ : the directory including HTML files to be p...'
        print 'index.dat : the index file containing mapping from name...'
        return

    # mapping of words to documents
    inverted_index = None
    # sorted tuple in order of:
    # doc length
    # doc title
    # doc url

    doc_index = None

    iterator_fname = files_in_dir(args['index'])
    for fname in files_in_dir(args['index']):
        #tokens in a list
        tokens, length_doc, title_doc, url_doc = parse_file(fname)
        
        tokens = filter_stopwords(tokens)

        tokens = apply_stemmer(tokens)

        update_inverted_index(tokens)
        
        update_doc_index(doc_index, length_doc, title_doc, url_doc)
    
    store_inverted_index(inverted_index)
    store_doc_index(doc_index)

def parse_args():
    if (len(sys.argv) < 3):
        print 'Not enough arguments'
        return
    output = dict()
    output['pages_dir'] = sys.argv[1]
    output['index'] = sys.argv[2]
    return output

def args_is_valid():
    pass

def args_is_not_valid():
    pass

def files_in_dir(dir_path):
    for filename in os.listdir(dir_path):
        if filename.endswith('.html'):
            yield filename

def update_inverted_index(inverted_index, tokens):
    # dictionary of (token, freq)
    token_count = count_tokens(tokens)
    for token, freq in token_count.items():
        if token not in inverted_index:
            inverted_index[token] = [(fname, freq)]
        else:
            # token is already in inverted index
            inverted_index[token].append( (fname, freq) )


def count_tokens(tokens):
    # Counter is subclass of dictionary
    return Counter(tokens)


def update_doc_index(doc_index, length, title, url):
    doc_index.append( (length, title, url) )


def store_inverted_index(inverted_index):
    # can use pickle mod instead
    with open(INVERTED_IDX_PATH, 'w') as f:
        json.dump(inverted_index, f)


def parse_file(fname):
    pass

def filter_stopwords(tokens):
    return [token for token in tokens if token not in STOPWORDS]

def apply_stemmer(tokens):
    return [STEMMER.stem(token) for token in tokens]

def
