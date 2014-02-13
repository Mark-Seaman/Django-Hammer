#!/usr/bin/env python
# Create a tabbed view of a user document

from os         import chdir,environ
from sys        import argv
from os.path    import join,exists
from re         import compile, IGNORECASE, DOTALL
from subprocess import Popen,PIPE
from random     import choice

from util.wiki  import convert_html,do_command,read_text


# Feature a single line of the input stream
def lookup_quote(line, lines):
    if '[[QUOTE]]' in line:
        t = filter(lambda l:len(l)>4, lines[2:])
        t = filter(lambda l:not '**' in l, t)
        t = filter(lambda l:not '[[QUOTE]]' in l, t)
        return '<b>'+choice(t)+'</b><br>'
    return line


# Select a line of text to feature
def extract_random_line(text):
    lines = text.split('\n')
    return '\n'.join([ lookup_quote(line, lines) for line in lines ])


def group_tabs(text):
    results = []
    groups = text.split('**')
    for i,g in enumerate(groups):
        if i%2>0:
            if i+1<len(groups):
                results.append(groups[i]+groups[i+1])
            else:
                results.append(groups[i])
    return results


def print_tab(text):
    '''
    Print one tab of text
    '''
    lines   = text.split('\n')
    heading = lines[0]
    body    = lines[1:]
    print '     <tab heading="%s">'%heading
    print '        <div class="page">'
    print '        <b>'+heading+'</b>'
    print convert_html(body)
    print '        </div>'
    print '     </tab>'


def print_all_tabs(text):
    '''
    Print all the tabs of text from the file
    '''
    tab_groups = group_tabs(text)
    tabs = text.split('**')
    body = tabs[0].split('\n')
    print convert_html(body)
    if len(tab_groups)>1:
        print '<div ng-controller="TabbedViewCtrl">'
        print '  <tabset ng-show="true">'
        for g in tab_groups:
            print_tab(g)
        print '  </tabset>'
        print '</div>'


def print_tab_doc(f):
    '''
    Formatter to add tabs to the HTML formatting
    '''
    f = join(environ['pd'], f)
    text = read_text(f)
    text = extract_random_line(text)
    print_all_tabs(text)
