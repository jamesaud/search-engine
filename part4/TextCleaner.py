from nltk.corpus import stopwords
import re
import os
from bs4 import BeautifulSoup
from nltk.stem.porter import *



# opens, reads, then closes a file
def _read_file(file_name):
    with open(file_name, 'r') as text_file:
        contents = text_file.read()
    return contents

# remove stopwords
def _remove_stopwords(listof_tokens):
    return [tok for tok in listof_tokens if tok not in set(stopwords.words('english'))]


# apply stemmer
def _stemm(listof_tokens):
    stemmer = PorterStemmer()
    return [stemmer.stem(word) for word in listof_tokens]

# http://stackoverflow.com/questions/1936466/beautifulsoup-grab-visible-webpage-text
def get_visible_text(file):
    soup = BeautifulSoup(file, )
    texts = soup.findAll(text=True)

    def visible(element):
        if element.parent.name in ['style', 'script', '[document]', 'head', 'title']: # Filter out unwanted html code
            return False
        elif re.match('<!--.*-->', element): # filter out comments
            return False
        return True

    visible_texts = filter(visible, texts)
    return list(visible_texts)

def get_title(file):
    with open(file) as f:
        soup = BeautifulSoup(f, )
    if soup.title:
        return soup.title.string

    return 'None' # If it doesn't have a title, assign it to None

# Parses the list of text and extracts cleansed words
def clean_text(lst_text):
    for line in lst_text:
        line = ''.join([char for char in line.strip() if char.isalpha() or char.isdigit() or (char in ' -:/')]) # Filter
        line = line.lower() # Case doesn't matter
        line = line.replace('/', ' ') # Replaces slashes with spaces
        line = re.sub(' - ', ' ', line) # Replace dashes that are inbetween spaces
        line = re.sub('(?<=[a-zA-Z]):', '', line)  # Remove ":" character if it is after a letter

        if line: # Make sure it isn't empty,
            if len(line)==1 and not (line[0].isalpha() or line[0].isdigit()): # if it's a single character, and not alphanumeric
                continue # Skip this line if not alphanumeric
            for word in line.split(): # Return 1 word at a time, so the final list is simply a list of words
                yield word

# return a list of words from the given file
def valid_words_from_file(file):
    content = _read_file(file)
    content = get_visible_text(content)
    content = clean_text(content)
    content = _remove_stopwords(content)
    content = _stemm(content)
    return content # Return a generator


# returns dict of short url mapped to real url
def get_urls(index_dat):
    with open(index_dat, 'r') as f:
        lines = f.readlines()

    mappings = {}
    for line in lines:
        split = line.split()
        mappings[split[0]] = split[1] # set the shorthand url as the key, the real url as the value

    return mappings


def get_outbound_links(file):
    soup = BeautifulSoup(open(file), )
    return [x.get('href') for x in soup.findAll('a')]
