#!/usr/bin/python
# Create a slide show from text

from files import read_input
from re import IGNORECASE,DOTALL,compile

# Global page being built
page  = [ ]
first = True
header = 'template/bin/header.html'
footer = 'template/bin/footer.html'

bridge_str = \
'''<slide class="fill nobackground" style="background-image: url(images/water2.jpg)">
    <hgroup class="auto-fadein">
      <h2 class="white">%s</h2>
      <h3 class="white">%s</h3>
    </hgroup>
  </slide>'''

config_str = \
'''var SLIDE_CONFIG = {
  settings: {
    title: '%s',
    subtitle: '%s',
    useBuilds: true,
    usePrettify: true,
    enableSlideAreas: true, 
    enableTouch: true, 
    favIcon: 'images/google_developers_logo_tiny.png',
    fonts: [
      'Open Sans:regular,semibold,italic,italicsemibold',
      'Source Code Pro'
    ],
  },
  presenters: [{
    name: '%s',
    company: 'Shrinking World Solutions',
    gplus: 'http://plus.google.com/mark.b.seaman',
    www: 'http://shrinking-world.org',
    twitter: '@mdseaman',
  }]
};
'''

# Print out the starting and ending HTML
def print_config (title,subtitle,author):
    open('slide_config.js','w').write(config_str % (title,subtitle,author))

# Print out the starting and ending HTML
def print_template (template):
    print open(template).read()

# Output a bridge slide
def print_bridge_page():
    global page, first
    subtitle = 'subtitle'
    title = 'title'
    if len(page)>1: subtitle = page[-1][7:-5]
    if len(page)>0: title = page[-2][7:-5]
    if not first: print ('</slide>\n')
    print (bridge_str+'\n') % (title,subtitle)
    page = []
    first = True

# Create bold text if needed
def make_bold(line):
    pat = compile(r"\*\*(.*)\*\*", IGNORECASE | DOTALL)
    return pat.sub(r'<h2>\1</h2>', line)

# Create bold text if needed
def make_italic(line):
    pat = compile(r"\*([a-zA-Z0-9].*[a-zA-Z0-9])\*", IGNORECASE | DOTALL)
    return pat.sub(r'<i>\1</i>', line)

# Process one line of text
def process_one_line(line):
    global page, first
    if line=='---':
        print_bridge_page()
        return
    if len(line)<1 and not first:
        page.append('</slide>\n')
        print '\n'.join(page)
        page = []
        first = True
        return
    if first:
        page.append('<slide>\n')
        page.append('   <h2>'+line+'</h2>')
    else:
        page.append('   <h3>'+make_bold(line)+'</h3>')
    first = False

# Print all slides
def print_slides (input):
    map(process_one_line, input) 
    process_one_line('')

# Print all the slides as an HTML file for Reveal.js
def print_slide_deck(lines):
    print_config(lines[0],lines[1],lines[2])
    print_template (header)
    print_slides (lines[4:])
    print_template (footer)

# Process the slides
print_slide_deck(read_input())
