#!/usr/bin/python
# Create a slide show from text

from files import read_input
from re import IGNORECASE,DOTALL,compile
from subprocess import Popen,PIPE

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
def print_bridge_page(title,subtitle):
    print (bridge_str+'\n') % (title,subtitle)

# Create bold text if needed
def make_bold(line):
    pat = compile(r"\*\*(.*)\*\*", IGNORECASE | DOTALL)
    return pat.sub(r'<h2>\1</h2>', line)

# Create bold text if needed
def make_italic(line):
    pat = compile(r"\*([a-zA-Z0-9].*[a-zA-Z0-9])\*", IGNORECASE | DOTALL)
    return pat.sub(r'<i>\1</i>', line)

# Return the formatted html code for this file
def wiki_text (filename):
    return  Popen(['wiki-html-content', filename],stdout=PIPE).stdout.read()   

# Process one line of text
def print_slide(filename):
    #text = open('slides/50-Tricks/'+filename).read()
    text = wiki_text('slides/50-Tricks/'+filename)
    print '<slide>\n',text,'</slide>\n'

# Print all the slides as an HTML file for Reveal.js
def print_slide_deck(lines):
    print_config(lines[0],lines[1],lines[2])
    print_template (header)
    for slide in lines[4:]:
        if ''==slide: 
            continue
        if slide.startswith('Bridge:'):
            print_bridge_page(slide[len('Bridge:'):],'')
            continue
        if slide=='---': break
        print_slide (slide)
    print_template (footer)

# Process the slides
print_slide_deck(read_input())
