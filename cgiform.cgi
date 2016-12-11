#! /usr/bin/env python
print('Content-type: text/html\n')
import cgi
from index import give_me_my_results

form = cgi.FieldStorage()

html="""
<h1>Results</h1>
{content}
"""
results = ''

terms = form.getfirst('query', 'this is a simple test to find results').split()
try:
  docs = give_me_my_results(terms, 100)
except ValueError:
  results = '<h1>Sorry, no results found</h1>'
else:
  for doc in docs:
      results += '''
      <h4>{title}</h4>
      <p><a href="{url}">{url}</a></p>
      <br>'''.format(title=doc.title, url=doc.url)

print(html.format(content=results))
