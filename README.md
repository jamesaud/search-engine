# dajanels-jamaudre-finalproject
i427 Search Informatics / Fall 2016 - Final Project

Report

-------------------------------------------------------------

Running back-end programs:

	Crawler - in directory 'part3/scrapy': 
		- scrapy crawl bfs
	
	invindex & docs.dat (in directory '/part4')comes from this command: 
		- python index.py pages index.dat

	calculations for page rank - in directory 'part5/retrieve2.py' & '/index.py'
	
	retrieval - /cgiform.cgi



Search Engine URL - http://cgi.soic.indiana.edu/~jamaudre/search/search/spud.html


Discussion and notes:
  We used OR to find our hit list. However, we weight results more favorably
  if they have more of the search terms. We realize that OR is much more
  inclusive, but we thought it would be better for a search engine to return
  as many results as it could than to have too few of results.

  As far as combining our PageRank and TFIDF scores, we had a few different 
  techniques. The first one is used for OR-only hits in the list, and we 
  just multiply the two scores together. This way, the pages with a higher page rank
  will be higher on the results as well. But we wanted a way to give a substantial 
  reward to those pages that had all of the query terms and pages that had an exact
  match with the query. So we made a second scoring mechanism for handling each
  case, first AND-only hits. Pages that had ALL of the search terms (order does not 
  matter) will be weighted more heavily than those found with just OR. We thought it
 would be best to double these scores. And for those results that had an exact match
  with the query would have a score of: 2^n * (PageRank * TFIDF) where n is the number
  of terms in the search query. Our TFIDT was the sum of each TFIDF score for each search term, so documents that included more of the terms more frequently were awarded a higher score. 


  Code design is as object oriented as necessary. However, there are several files which contain utilitiy functions, such as our TextCleaner.py, which do not lend themselves to OOP style programming. 

Each subfolder of our project (part4, part5) has its own unit_tests.py file. To run it, just do 'python unit_tests.py'. Code coverage is not optimal, but important functions are tested. part3 (the crawler) does not have unit_tests as it was not easily implemented.

Page rank was an interesting problem for us, and we think we took a simple yet effective approach. Following the formula and explanation found at pr.efactory.de/e-pagerank-implementation.shtml, we implemented the code into Python and integrated it with our codebase. 

In order to avoid refactoring code based on parsing docs.dat, a new file pr.dat is written which links pages to their pagerank. These values, along with the inv_index.dat, are precomputed. When a user searches for terms, our program reads in from these precomputed files and quickly (less than a second) can compute our evaluation of TF-IDFT & Page Rank to deliver the results page.

Our page base was 20,000 pages starting from alexa.com/topsites/countries/US using BFS traversal. We had a hard time deciding where to start in order to acquire a wide variety of sites and content. The first time we crawled, we started on reddit (granted it was with DFS) and ended up getting stuck on crawling exclusively user profile pages for a long time before deciding to stop the crawler and start somewhere else. 


User Eval Experiment

We had our roommates test our search engine and they got disappointing results. They searched terms like "ultimate frisbee" and "audl" and the pages they were looking for did not come up. We intend to keep our crawler running for a few days longer in hopes that it will pick up some more pages and more variety. More general search terms yielded better results, as did search terms with more key words in it. The way we implemented the search engine allows OR results to appear, so that more key words means a greater amount of results but also more focused results because of our TF-IDF score summation.
We had them also search Google for their search querries, which was a hands-down won in terms of quality. Simply, our search engine did not crawl enough pages to provide valid results for specialized queries like 'ultimate frisbee'. Something to note was that our results were always very valid in terms of containing the right information. This is because of TF-IDF having such an impact on our results, guaranteeing a high volume of terms inside the document itself.

In the future, hooking up our engine to a database system rather than text files would be a much better way of quickly getting results. It also would help with maintaining data integrity and a consistent API for accessing information. Also, page rank would be a more determining factor as we would have a better network of pages that link to one another. In our network, not that many pages formed a graph.

Sources:
The page rank website we mentioned above.
    
