from __future__ import print_function
import os
from part4.TextCleaner import _stemm, _remove_stopwords
from part5.retrieve2 import find_tf_idf_scores, docs_by_tf_idf
from operator import itemgetter

__path = os.getcwd()
DAT_PATH = os.path.join(__path, 'testpages/docs.dat')
INV_PATH = os.path.join(os.path.join(__path, 'testpages/invindex.dat'))



def clean_words(word_list):
    return _stemm(_remove_stopwords(word_list))


def search_words(word_list):
    doc_list = find_tf_idf_scores(DAT_PATH, INV_PATH, word_list)
    doc_scores = docs_by_tf_idf(doc_list, word_list)
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


def demo_for_dan():

    words = 'hello this is a phrase that is going to be parsed by nltk we are the world we are the children hello this is \
    my name nice to meet you hi there bicycle'.split()

    results = give_me_my_results(words, 25)
    doc = results[0]

    print("I'm calling a function called 'give_me_my_results'...\n")

    print(results)
    print("\nHey Dan, this function returned", len(results), "Document Objects.")
    print("\nWhat can you do with Document Objects? Glad you asked.")
    print("\nLook at the Document class in part5/retrieve2.py. For one document, I'll use the first result, you can get the...")
    print("- Word Counts: (too long to show)")
    print("- Title:", doc.title)
    print("- Name:", doc.name)
    print("- URL:", doc.url)
    print("- TF_Scores: (too long to show)")
    print("- TF_IDF_Scores: (too long to show)")

    print("\nRun a mother f***ing for-loop over the results, display them through the CGI Page.")
    print("\nGonna have to run the crawler overnight to get an actual large set of pages to finalize it tomorrow.")

if __name__ == '__main__':
    demo_for_dan()