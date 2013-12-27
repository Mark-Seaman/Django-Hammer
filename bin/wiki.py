#!/usr/bin/env python
# Wiki text formatter

from os.path    import isfile, exists
from sys        import argv, stdin
from re         import compile, IGNORECASE, DOTALL

# Create bold text if needed
def make_heading(line):
    pat = compile(r"\* (.*) \*", IGNORECASE | DOTALL)
    return pat.sub(r'<h1>\1</h1>', line)

# Create bold text if needed
def make_bold(line):
    pat = compile(r"\*\*(.*)\*\*", IGNORECASE | DOTALL)
    return pat.sub(r'<b>\1</b>', line)

# Create bold text if needed
def make_italic(line):
    pat = compile(r"\*([a-zA-Z0-9].*[a-zA-Z0-9])\*", IGNORECASE | DOTALL)
    return pat.sub(r'<i>\1</i>', line)

# Add paragraph breaks if needed
def break_paragraphs(line):
    if line=='': return '</p><p>'
    else: return line

# Remove the muse tag from the first line
def remove_muse(line):
    return line.replace ('-*-muse-*-', '').replace ('-*- muse -*-', '').rstrip()

# Preserve any four spaces together
def preserve_spaces(line):
    return line.replace('    ', '&nbsp;&nbsp;&nbsp;&nbsp;')

# Break lines for <space> at beginning
def space_breaks(line):
    always_break = True
    if always_break or (len(line)>0 and line[0]==' '):
        return  '<br/> '+line
    return line

# Add horizontal rules
def format_rules(line):
    i=line.find('---')
    if i!=-1:
       return line.replace('---', '<hr>')
    return line

# Add bullets
def format_bullets(line):
    i=line.find('  * ')
    if i!=-1:
        return "<ul><li>"+line[i+4:]+"</li></ul>"
    return line

# Convert the url in a string to an HTML anchor
def muse_double_anchor(url):
    s = r"\[\[([\/\w\.\:\-\_]*)\]\[([ \w\.\-\_\,\?\%]*)\]\]"
    pat = compile(s, IGNORECASE | DOTALL)
    return pat.sub(r' <a href="\1">\2</a> ', url)

# Convert the url in a string to an HTML anchor
def muse_single_anchor(url):
    s = r"\[\[([\/\w\.\-\_]*)\]\]"
    pat = compile(s, IGNORECASE | DOTALL)
    return  pat.sub(r' <a href="\1">\1</a> ', url)

# Convert the url in a string to an HTML anchor
def muse_anchor(url):
    url = muse_double_anchor(url)
    return muse_single_anchor(url)

# Convert the url in a string to an HTML anchor
def url_to_anchor(url):
    s = r"(^|[\n ])(([\w]+?://[\w\#$%&~.\-;:=,?@\[\]+]*)(/[\w\#$%&~/.\-;:=,?@\[\]+]*)?)"
    pat = compile(s, IGNORECASE | DOTALL)
    return pat.sub(r'\1<a href="\2" target="_blank">\2</a>', url)

# Convert the url in a string to an HTML image tag
def url_to_image(url):
    s = r"\[\[images/(([\w\#$%&~.\-;:=,?@\[\]+]*)(/[\w\#$%&~/.\-;:=,?@\[\]+]*)?)\]\]"
    pat = compile(s, IGNORECASE | DOTALL)
    return pat.sub(r'<img src="/media/mybook/images/\1" alt="\1">', url)

# Convert the Wiki Words to hyperlinks
def wiki_words(text):
    s = r"([^A-Za-z\"\']*)([A-Z][a-z]+[A-Z][a-z]+([A-Z][a-z]+)*)([^A-Za-z\'\"]*)"
    pat = compile(s, DOTALL)
    return muse_anchor(pat.sub(r'\1[[\2]]\4', text))

# Convert a single line of muse to html
def convert_links(text1):
    text = text1
    text = url_to_image(text)
    text = url_to_anchor(text)
    text = muse_anchor(text)
    if text==text1: text = wiki_words(text)
    return text

# Convert a single text line to html
def convert_line(line):
    line = remove_muse(line).rstrip()
    line = space_breaks(line)
    line = format_rules(line)
    line = format_bullets(line)
    line = break_paragraphs(line)
    line = convert_links(line)
    line = preserve_spaces(line)
    line = make_heading(line)
    line = make_bold(line)
    return make_italic(line)

# Convert array of strings to html body text
def convert_html(text):
    text = map(convert_line, text)
    return '\n'.join(text)

# The first line holds the page title
def get_title(text):
    if len(text)>0: 
        return remove_muse(text[0]).rstrip()[2:][:-2]
    return 'No title'


def do_command(cmd, input=None):
    '''
    Run the command as a process and capture stdout & print it
    '''
    try:
        if input:
            p = Popen(cmd.split(), stdin=PIPE, stdout=PIPE)
            p.stdin.write(input)
            p.stdin.close()
        else:
            p = Popen(cmd.split(), stdout=PIPE)
            return  p.stdout.read()
    except:
        return '<h1>Command Error</h1>'+\
            '<p>An error occurred while trying to execute the command:</p>'+\
            '<p>COMMAND: %s</p>'%cmd +\
            '<p>INPUT: %s</p>'%input



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


def print_tab_text(lines, format_lines):
    if format_lines:
        print '           ', convert_html(lines)
    else:
        print '           ', '\n'.join(lines)


def print_tab(text, format_lines):
    '''
    Print one tab of text
    '''
    lines = text.split('\n')
    heading = lines[0]
    print '     <tab heading="%s">'%heading
    print '        <div class="page">'
    #print '        <b>'+heading+'</b>'
    print_tab_text(lines[1:], format_lines)
    print '        </div>'
    print '     </tab>'


def print_all_tabs(text, format_lines=True):
    '''
    Print all the tabs of text from the file
    '''
    tab_groups = group_tabs(text)
    print convert_html(text.split('**')[0].split('\n'))
    if len(tab_groups)>1:
        print '<div ng-controller="TabbedViewCtrl">'
        print '  <tabset ng-show="true">'
        for g in tab_groups:
            print_tab(g, format_lines)
        print '  </tabset>'
        print '</div>'


def read_text(f):
    '''
    Return the text from the file
    '''
    if exists(f):
        return open(f).read()
    return 'No file found, '+f
