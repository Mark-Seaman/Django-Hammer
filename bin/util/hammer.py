#!/usr/bin/env python
# Create the index for a given user
from os.path import join,exists,basename
from os      import environ
from sys     import argv

from files   import do_command,list_files,list_dirs
# Wiki text formatter

from sys        import stdin
from wiki       import convert_html

# Create html file contents from stdin
def page_html():
    text = stdin.read().split('\n')
    return convert_html(text)


# Read the index text from a file
def read_index(f):
    if not exists(f):
        print "Invalid app: "+f
        exit(1)
    return open(f).read()


# Turn a wiki work into a title
def title_text(title):
    '''
    Format the title with spaces to break each word.
    '''
    title = title[0] + ''.join([ " "+c if c.isupper() else c  for c in title[1:] ])
    return title 


# Create links for each item in the folder
def app_links(files):
    return [ ' * [[%s][%s]]'%(x,title_text(x)) for x in files   if len(x)>0 ]

# Return the directory list
def directory_list(d):
    dirs = [ basename(f) for f in list_dirs(d) ]
    return  '\n'.join(app_links(dirs))


# Return the directory list
def item_list(d):
    dirs = [ basename(f) for f in list_files(d) if not f.startswith('.') and not f.startswith('Index') ]
    return  '\n'.join(app_links(dirs))


# Add a list of directory entries
def include_dirs(text,d):
    return [ l if not '[[DIRS]]' in l else directory_list(d)   for l in text ]
            

# Add a list of directory entries
def include_items(text,d):
    return [ l if not '[[ITEMS]]' in l else item_list(d)   for l in text ]
            

# Create wiki text for the index page
def index_text(doc):
    d = join(environ['pd'],doc)
    text = read_index(join(d,'.index')).split('\n')
    text = include_dirs(text,d)
    #print 'include ',d
    text = include_items(text,d)
    text.append('')
    return '\n'.join(text)


# Create wiki text for the index page
def index_html(doc):
    text = index_text(doc)
    print do_command('hammer-wiki', text)
