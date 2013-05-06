from django.db          import models
from django.forms       import ModelForm
from subprocess         import Popen,PIPE
from os.path            import exists,join,dirname
from os                 import listdir,remove
from Hammer.settings    import DOC_ROOT

class Note (models.Model):
    '''
    Note data model
    '''
    path  = models.CharField (max_length=200)
    body  = models.TextField ()

class NoteForm (ModelForm):
    '''
    Note form data model used to edit notes
    '''
    class Meta:
        model=Note


def doc_file(title):
    '''
    Path to doc in file system
    '''
    return join(DOC_ROOT,title)


def doc_template(title):
    '''
    Find the template file for this document
    '''
    folder = dirname(doc_file(title))
    template = folder+'/.template'
    if exists(template):
        return open(template).read()[:-1]
    else:
        return 'Note'


def clone_template(title):
    '''
    Copy the template into the new page folder
    '''
    t = doc_file(join('template',doc_template(title)))
    if exists(t):
        text = open(t).read()%title
        f = open(doc_file(title),'wt')
        f.write(text)
        f.close()    


def do_command(cmd):
    '''
    Run the command as a process and capture stdout & print it
    '''
    return  Popen(cmd.split(),stdout=PIPE).stdout.read()


def is_special_doc(title):
    '''
    Pick out the special docs
    '''
    return False

    
def is_doc(title):
    '''
    Look for the document
    '''
    return is_special_doc(title) or exists(doc_file(title))     


def list_docs(folder='.'):
    '''
    Return the doc in the requested folder
    '''
    return listdir(doc_file(folder))


def format_doc(title):
    '''
    Run the wiki formatter on the document
    '''
    if is_special_doc(title):
        return special_doc_command(title)   
    return do_command('wiki-html-content '+doc_file(title))


def read_doc(title):
    '''
    Run the wiki formatter on the document
    '''
    return open(doc_file(title)).read()


def write_doc(title,body):
    '''
    Save the document file
    '''
    return  open(doc_file(title), 'wt').write(body)


def delete_doc(title):
    if is_doc(title):
        remove(doc_file(title)) 
