from django.contrib.auth.decorators import login_required
from django.http        import HttpResponseRedirect, HttpResponse
from django.shortcuts   import render
from os.path            import join, exists, dirname
from os                 import system,environ

from models             import *

def missing(request,title):
    '''
    Render the view for a missing document
    '''
    text = format_doc('MissingFile')
    template = doc_template(title)
    create_link = '<a href="/%s/%s/add">%s</a>' % (title,template,title)
    return render(request, 'doc.html', {'title': title, 'text': text%create_link })


@login_required(login_url='/login')
def doc(request,title):
    '''
    Render the appropriate doc view
    '''
    print 'doc: %s'%(title)
    if is_doc(title):
        text = format_doc(title)
        return render(request, 'doc.html', {'title': title, 'text': text})
    else:
        return missing(request,title)


def home(request):
    '''
    Render the home view
    '''
    return doc(request, 'Index')


def redirect(title):
    '''
    Go to a specific page
    '''
    print 'redirect: %s'%(title)
    return HttpResponseRedirect('/'+title) 


@login_required(login_url='/login')
def edit_form (request, title=None):
    '''
    Create a form for editing the object details
    '''
    print 'form: %s'%(title)
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if request.POST.get('cancel', None):
            title = form.data['path']
            if not title:
                title = 'Home'
            return redirect(title)
        else:
            if form.is_valid():
                print 'save: %s'%(title)
                title = form.cleaned_data['path']
                write_doc(title, form.cleaned_data['body'])
                return redirect(title)
    else:
        note =  Note()
        if  title:
            note.path = title
            if is_doc(title):
                print 'read: %s'%(title)
                note.body = read_doc(title)
        form =  NoteForm(instance=note)
    data =  { 'form': form, 'title': title  }
    return render(request, 'edit.html', data)


def add(request,title,template):
    '''
    Render the add view
    '''
    print 'add: %s, %s'%(title,template)
    clone_template(title)
    return edit_form (request,title)


def edit(request,title):
    '''
    Render the add view
    '''
    print 'edit: %s'%(title)
    return edit_form (request,title)


def delete(request,title):
    '''
    Delete the record
    '''
    print 'delete: %s'%(title)
    delete_doc (title)
    return redirect(dirname(title))

  
# Sample code:
#    if request.user.is_anonymous(): return 0
#    if not request.user.is_superuser:  return redirect('/NoAccess') 
#    u = UserAccount.objects.get(pk=request.user.pk).pk
#    if not u==user_id:    return redirect('/NoAccess')
