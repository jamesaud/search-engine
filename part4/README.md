# mornash-jamaudre-p4

#Part 1
You'll need: 
>nltk, nltk stopwords,    nltk wordnet, beautifulsoup4


In pages/invindex.dat the format is:

>Term ListOfDocsTermAppearsIn ListOfCountsOfTerm


The ListOfCountsOfTerm correspondss 1 to 1 with the ListOfDocsTermAppearsIn. That is: hello [doc1, doc2, doc3] [4 5 6]
means that 'hello' appeared in doc1 4 times, doc2 5 times, doc3 6 times


In pages/docs.dat the format is:
>Doc Length Title FullUrl

Where Doc is the document name, length is the total number of terms in the document, title is the title tag contents, and FullUrl is the mapping from index.dat

To run, do:
> python2 index.py pages index.dat
