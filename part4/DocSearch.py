import os
import operator
import TextCleaner as TC
from collections import defaultdict
from collections import Counter

count = 0
class DocSearch(object):
    def __init__(self):
        self.word_docs = defaultdict(list) # Key, the word   Value, a list of docs it appears in
        self.docs = [] # List of Doc objects

    # Parse all the documents, update the Counter class
    def precompute(self, path, index_dat_name):
        global count

        files = self._get_files(path)
        urls = TC.get_urls(os.path.join(path, index_dat_name)) # dict of url mappings

        for file in files:

            print("Getting file...", count)
            count+=1
            file_path = os.path.join(path, file)  # full file path
            words = self._clean_words(file_path) # list of words cleaned
            title = TC.get_title(file_path)
            url = urls[file]
            outbound = TC.get_outbound_links(file_path)

            self._update_docs(file, words, title, url, outbound)

        self._links_to_docs()


    def _update_docs(self, file_name, list_words, title, url, outbound):  # name of file, list of terms, the doc title, doc url
        doc = Doc(file_name)
        doc.url = url
        doc.title = title
        doc.term_counts = Counter(list_words) # create dictionary of key: word, value: count
        doc.links = set(outbound)
        self.docs.append(doc)

        set_words = set(list_words) # create a set so each word appears only once

        # update the word with the corresponding doc
        for word in set_words:
            self.word_docs[word].append(doc)



    # Get a list of html files to search through
    @staticmethod
    def _get_files(path):
        # If path doesn't exist, raise error
        if not os.path.isdir(path):
            raise ValueError("Provide a valid path: %s is not valid" % path)

        # get all html files from current dir
        html_files = (file for file in os.listdir(path) if
                      os.path.splitext(file)[1].lower() == '.html')

        # If their are no html files in dir, raise error
        if not html_files:
            raise ValueError("Didn't find any html files in the given path: %s" % path)

        return html_files  # Generator of html files

    # Get a list of valid words from an html file
    @staticmethod
    def _clean_words(file):
        return TC.valid_words_from_file(file)

    def _links_to_docs(self):
        doc_urls = {doc.url : doc for doc in self.docs}
        for doc in self.docs:
            for link in doc.links:
                if link:
                    url = [url for url in doc_urls if url.endswith(link)]
                    if url:
                        doc.docs.append(doc_urls[url[0]])


class Doc(object):

    def __init__(self, name):
        self.name = name
        self.term_counts = Counter()
        self.title = None
        self.url = None

        # New
        self.links = set()
        self.docs = []

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name



"""
Use Cases:

ds = DocSearch()
ds.precompute('path/to/html')
ds.search('word')

"""

