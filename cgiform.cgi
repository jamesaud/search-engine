#! /usr/bin/env python
from __future__ import division
print('Content-type: text/html\n')
import cgi
from index import give_me_my_results
from operator import itemgetter


form = cgi.FieldStorage()

html="""
<h1>Top {length} Results</h1>
<h2><i>{extra}</i></h2>
{content}
"""
results = ''
length = ''
extra = ''

terms = form.getfirst('query', 'this is a simple test to find results').split()
display_terms = [] + terms



try:
  docs = give_me_my_results(terms, 100)
  if docs[0].final_score == 0:
      if len(terms) == 1:
        terms.append('looking') # Filthy, we have a bug where some len(1) words cause the scores to be 0. So we append a rather uncommon word.
        docs = give_me_my_results(terms, 100)
        docs = [doc for doc in docs if doc.final_score > 0]

  if docs[0].final_score == 0:
      print("<h4>The search term only appeared once in the results, causing tf_idf to be 0. Sorting by PageRank.</h4>")
      docs_pr = [(doc, doc.pagerank) for doc in docs]
      docs = sorted(docs_pr, key=itemgetter(1), reverse=True)
      docs = map(itemgetter(0), docs)
      
  length = len(docs)
  extra = "For the search term: {0}".format(' '.join(display_terms))
except ValueError:
  results = '<h1>Sorry, no results found</h1>'
else:
  for doc in docs:
      results += '''
      <h4>{title}</h4>
      <p><a href="{url}">{url}</a></p>
      <p>Page Rank: {pr}, TF-IDF: {tf}, Final-Score: {fs}</p>
      <br>'''.format(title=doc.title, url=doc.url, pr=doc.pagerank, tf=doc.final_score/float(doc.pagerank), fs=doc.final_score)

print(html.format(content=results, length=length, extra=extra))
