from part4.TextCleaner import _stemm, _remove_stopwords

words = 'hello this is a phrase that is going to be parsed by nltk'.split()
print(_stemm(_remove_stopwords(words)))