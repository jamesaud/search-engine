from __future__ import print_function
import os
from part4.TextCleaner import _stemm, _remove_stopwords
from part5.retrieve2 import find_scores, docs_by_score
from operator import itemgetter

__path = os.getcwd()
DAT_PATH = os.path.join(__path, 'testpages/docs.dat')
INV_PATH = os.path.join(os.path.join(__path, 'testpages/invindex.dat'))
PR_PATH = os.path.join(os.path.join(__path, 'testpages/pr.dat'))



def clean_words(word_list):
    return _stemm(_remove_stopwords(word_list))


def search_words(word_list):
    doc_list = find_scores(DAT_PATH, INV_PATH, PR_PATH, word_list)
    doc_scores = docs_by_score(doc_list, word_list)
    return doc_scores

def limit_results(doc_score_dict, num_results):
    return doc_score_dict.most_common(num_results)


"""
Returns a sorted list of web pages that match the query terms
:param list_words: list[str], the terms to search for
:param limit_results: int, the number of results to return
:return: list[Document]: a list of document objects
Note - Document API is in part5.retrieve2
"""
def give_me_my_results(list_words, limit):

    list_words = clean_words(list_words)
    doc_scores = search_words(list_words)
    sorted_doc_scores = limit_results(doc_scores, limit)

    return map(itemgetter(0), sorted_doc_scores)


