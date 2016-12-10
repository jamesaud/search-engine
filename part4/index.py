## High Level Report
## A few assumptions were made when cleaning & storing the text. 1) maintaining numbers as tokens so that zip codes & other numberical 
## values can be searched for. 2) removing : only from the end of a string, to preserve times such as 1:45 3) separating words held
## together by a slash so that it becomes "buy" & "rent" as opposed to "buy/rent". 4) adding words we deemed relevant to the nltk
## stopwords library. 

from __future__ import print_function
import os
import sys
from DocSearch import DocSearch

# takes in a DocSearch object, writes the inverse index to the provided file
# Writes: Term, ListOfDocuments, Occurences In Documents
def write_inverse_index(file, DS):
    word_docs = DS.word_docs

    with open(file, 'w') as f:
        for word, doc_lst in word_docs.items():   # word is key,   doc_lst is value
            counts = [doc.term_counts[word] for doc in doc_lst] # Get counts of each doc as a list

            # I don't know why I have to unicode them like this, but to make it work I just do.
            f.write('{0} {1} {2}\n'.format(word.encode('utf-8'), [doc.name for doc in doc_lst], str(counts).encode('utf-8')))

def write_docs_dat(file, DS):
    docs = DS.docs

    with open(file, 'w') as f:
        for doc in docs:
            length = sum(val for val in doc.term_counts.values())

            f.write('{0} {1} {2} {3}\n'.format(doc.name, length, [doc.title], doc.url))

def main():
    def parse_args():
        args = sys.argv
        if len(args) != 3:
            raise ValueError("Incorrect number of arguments")

        args = args[1:] # remove the index.py from args

        return args

    directory, index_file = parse_args()


    path = os.getcwd()
    path = os.path.join(path, directory)

    d = DocSearch()

    d.precompute(path, index_file)

    print('\n\n', d.docs[0].docs)


    to_write_inverse = os.path.join(path, 'invindex.dat')
    to_write_doc = os.path.join(path, 'docs.dat')

    write_inverse_index(to_write_inverse, d)
    write_docs_dat(to_write_doc, d)

    print("Succesfully wrote invindex.dat and docs.dat")

if __name__ == '__main__':
    main()



# NLTK download wordnet, stopwords


