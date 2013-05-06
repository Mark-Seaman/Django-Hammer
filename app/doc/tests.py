"""
Test to make sure that this application is running properly.
"""

from django.http            import HttpRequest, HttpResponse
from django.template.loader import render_to_string
from django.test            import TestCase
from os                     import listdir
from subprocess             import Popen,PIPE

from Hammer.settings        import DOC_ROOT, STATICFILES_DIRS
from doc.views              import home,list_docs,doc,template,clone_doc
from doc.models             import Note,NoteForm,list_docs,read_doc


def diff(s1,s2):
    '''
    Calculate the text difference for a test
    '''
    t1 = '/tmp/diff1'
    t2 = '/tmp/diff2'
    #print 'Response:', t1
    #print 'Expected:', t2
    open(t1, 'wt').write(s1)
    open(t2, 'wt').write(s2)
    diffs = Popen([ 'diff', t1, t2 ], stdout=PIPE).stdout.read()
    #print diffs
    return diffs.split('\n')

             

#TODO: create a function to diff two text string using 'diff'
class AppConfigTest(TestCase):

    def expected_template(self, doc, temp):
         self.assertEqual (temp, template(doc))
            
    def test_static_directory(self):
        '''
        Make sure that the static storage has files in it
        '''
        static_dir = STATICFILES_DIRS[0]
        files = len(listdir(static_dir))
        #print 'Static root: %d %s'%(files, static_dir)
        self.assertEqual(files, 4)

    def test_clone(self):
        '''
        Make sure that the template cloning works
        '''
        self.expected_template('XxXx','UserStory')
        self.expected_template('Xx','UserStory')
        self.expected_template('X/xXx','')

        doc = 'XxXx'
        temp = template(doc)
        clone_doc(doc,temp)
        #self.assertTrue(False)
