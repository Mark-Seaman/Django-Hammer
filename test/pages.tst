#!/usr/bin/env python
# Run a python script to test the web pages

from os.path  import join
from os import environ,chdir,system
from platform import node

host = 'localhost:8089'

pages = '''
login
Index'''

#pages = ''

chdir (join(environ['p'],'test'))

if 'seaman-' not in node():
    f = 'web-pages.correct'
    print open(f).read(),

else:
    from page_test import test_web_pages
    print 'Testing Host:',host
    print 'Starting the server'
    system ('server-stop && server-start')
    test_web_pages(host,pages)
    system ('server-stop>/dev/null')
