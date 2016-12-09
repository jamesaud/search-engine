import cgi

form = cgi.FieldStorage()
print('Content-type: text/html\n')
print('<title>Reply Page</title>')
if not 'user' in form:
    print('<h1>What can I help you fuck?</h1>')
else:
    print(*'Searching for <i>%s</i></h1>' % cgi.escape(form['user'].value))
