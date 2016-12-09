from __future__ import print_function
##High level report:
## Using a dictionary to store words as keys and pages they appeard on as values. No need to store the frequencies here.
## using a set where we do not want repeats in elements. queues where we want to be able to pop elements out until empty and lists else where. 

import sys
import os
import re
from nltk import SnowballStemmer
from DocSearch import DocSearch
from TextCleaner import *

# opens, reads, then closes a file
def _read_file(file_name):
    text_file = open(file_name, 'r')
    return text_file

def create_dict(file_name):
    d = dict()
    with open(file_name) as f:
        lines = f.readlines()
    for line in lines:
        l = line.strip().replace(']','[').replace("'", "").replace(",",'').split("[")
        d[l[0].strip()] = l[1].split()
    return d

# create dict of query terms and pages appeared on 
def find_pages(dictionary, queue):
    found = dict()
    for q in queue:
        if dictionary.has_key(q):
            found[q] = list(dictionary[q])
        else:
            found[q] = []
    return found

def check_or(dct):
    hitlist = set()
    for key, value in dct.iteritems():
        hitlist.update(value)
    return list(hitlist)

def check_and(dct):
    sets = [set(lst) for lst in dct.values()]
    return set.intersection(*sets)

            
def check_most(dct):
    cutoff = len(dct) / 2
    pages = check_or(dct)
    hitlist = list()
    for page in pages:
        pagect = 0
        for key, value in dct.iteritems():
            if page in value:
                pagect = pagect + 1
        if pagect >= cutoff:
            hitlist.append(page)
    return hitlist           
    
def stem_queue(q):
    stemmer = SnowballStemmer("english")
    queue = list()
    for word in q:
        queue.append(stemmer.stem(word))
    return queue

def parse_args():
    args = sys.argv
    args = args[1:]

    if args[0] not in ("or", "and", "most"):
        print (args[1])
        print ("Error - mode not recognized.")
    else:
        pass
    return args

def main():
    queue = parse_args()

    mode = queue.pop(0)
    words = queue[1:]
    q = stem_queue(words)


    # The Path
    curr_path = os.getcwd()
    path_to_pages = os.path.join(curr_path, 'pages')
    path_to_inv = os.path.join(path_to_pages, 'invindex.dat')
    path_to_index = os.path.join(path_to_pages, 'index.dat')

    d = create_dict(path_to_inv)

    query_dict = find_pages(d, q)



    if mode == "and":
        output = check_and(query_dict)
    elif mode == "or":
        output = check_or(query_dict)
    elif mode == "most":
        output = check_most(query_dict)
    
    urls = get_urls(path_to_index)

    for file in output:
        full_url = urls[file]
        print("URL:", full_url, "Title:", get_title(os.path.join(path_to_pages, file))) # this should be thae path to the file. use os.path.join() like i did above

    print("Hits found: ", len(output))
    print("Number of docs searched: ", len(get_urls(path_to_index)))

if __name__ == '__main__':
    main()

