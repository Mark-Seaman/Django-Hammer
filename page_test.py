#!/usr/bin/env python
# Run a python script to test support center web pages

from os.path  import join,exists
from os import system,environ,chdir
from platform import node
from subprocess import Popen,PIPE
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Global vars
browser = ''
accept_all_pages = False


def get_page_text(host,page):
    '''
    Get Support Center page
    '''
    try:
        browser.get(join(host,page))
        body = browser.find_element_by_tag_name('body')
        text = body.text.decode('ascii','ignore')
    except:
        text = 'File not found: '+join(host,page)
    return '\n\nTitle:%s\n%s\n' % (browser.title, text )


def login(host,page):
    '''
    Login to the Support Center web site
    '''     
    get_page_text(host,page)
    from local_settings import username,password
    username_field = browser.find_element_by_name('username')
    username_field.send_keys(username)
    password_field = browser.find_element_by_name('password')
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)


def print_page_text(host,page):
    '''
    Print the text from a Support Center page
    '''
    print get_page_text(host,page)


def save_page_text(host,page,output):
    '''
    Get the web page, extract the text, and save the file
    '''
    f=open(output, 'wt')
    text = get_page_text(host,page)
    f.write(text)
    f.close()


def page_names(url):
    '''
    select the file name to use
    '''
    page=url.replace('/','-')
    if page=='': 
        page='index'
    page = 'page-'+page
    #print 'page_names:',  ( page+'.out', page+'.correct')
    return ( page+'.out', page+'.correct')


def test_page(host,url):
    '''
    Compare the actual page to the expected one
    '''
    output,correct = page_names(url)
    save_page_text(host,url,output)
    if not exists(correct):
        accept_page_text(url)


def accept_page_text(url):
    '''
    Make the actual page be the expected one
    '''
    output,correct = page_names(url)
    print 'Accept text from ',url
    system('cp '+output+' '+correct)


def diff(t1,t2):
    '''
    Calculate the text difference for a test
    '''
    diffs = Popen([ 'diff', t1, t2 ], stdout=PIPE).stdout.read()
    return diffs


def show_page_diffs(url):
    '''
    Print differences between the actual page to the expected one
    '''
    output,correct = page_names(url)
    diffs = diff(output, correct)
    if len(diffs)>1 and url!='': 
        system('tdiff '+output[:-4])


def test_web_page(host,page):
    '''
    Test a single page from the requested host
    '''
    print 'Testing', page, '...'
    test_page(host,page)
    if accept_all_pages: 
        accept_page_text(page)
    show_page_diffs(page)


def test_web_pages(host,pages,login_page=False):
    '''
    Get the home page, Login, Read all pages
    '''
    global browser
    browser = webdriver.Chrome()
    try:
        browser.implicitly_wait(5)
        if login_page:
            get_page_text(host,'logout')
            login(host,'xxx')
        for page in pages.split('\n'):
            print host, page
            test_web_page(host,page)
    except:
        print 'Test web pages failed'

    browser.quit()
