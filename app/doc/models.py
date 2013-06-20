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
    path  = models.CharField (max_length=200, editable=False)
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


def do_command(cmd, input=None):
    '''
    Run the command as a process and capture stdout & print it
    '''
    if input:
        p = Popen(cmd.split(), stdin=PIPE, stdout=PIPE)
        p.stdin.write(input)
        p.stdin.close()
    else:
        p = Popen(cmd.split(), stdout=PIPE)
    return  p.stdout.read()

    
def is_doc(title):
    '''
    Look for the document
    '''
    return exists(doc_file(title))     


def format_doc(title):
    '''
    Run the wiki formatter on the document
    '''
    return do_command('hammer-show %s'%title)


def read_doc(title):
    '''
    Run the wiki formatter on the document
    '''
    return do_command('hammer-read %s'%title)


def write_doc(title,body):
    '''
    Save the document file
    '''
    body = body.replace('\r','')
    do_command('hammer-write %s'%title, body)


def delete_doc(title):
    if is_doc(title):
        remove(doc_file(title)) 
