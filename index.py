from part4.TextCleaner import _stemm, _remove_stopwords

i = input("Input:")

print(_stemm(_remove_stopwords(i)))