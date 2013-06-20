from datetime           import datetime
from django.contrib.auth.decorators import login_required
from django.http        import HttpResponseRedirect, HttpResponse
from django.shortcuts   import render
from os.path            import join, exists, dirname
from os                 import system,environ

from models             import *

def user(request):
    '''
    Name of requesting user
    '''
    return request.user.username


def log_page(user,title):
    '''
    Log the page hit in page.log
    '''
    f=open('page.log','a')
    f.write(str(datetime.now())+', '+user+', '+title+'\n')
    f.close()


def missing(request,title):
    '''
    Render the view for a missing document
    '''
    text = format_doc('MissingFile')
    template = doc_template(join(user(request),title))
    href = "%s/%s/add" % (title,template)
    return redirect(href)
    #link = '<a href="/%s">%s</a>' % (href,title)
    #return render(request, 'doc.html', {'title': title, 'text': text%link })


def redirect(title):
    '''
    Go to a specific page
    '''
    print 'redirect: %s'%(title)
    return HttpResponseRedirect('/'+title) 



@login_required(login_url='/login')
def doc(request,title):
    '''
    Render the appropriate doc view
    '''
    doc = join(user(request),title)
    log_page (user(request), title)
    print 'doc: %s'%(title)
    if title.endswith('/'):
        return redirect(title+'Index')
    if is_doc(doc):
        text = format_doc(doc)
        return render(request, 'doc.html', {'title': title, 'text': text})
    else:
        return missing(request,title)


def home(request):
    '''
    Render the home view
    '''
    if not request.user.is_anonymous():
        return doc(request,'Index')
    log_page ('Annonymous', 'Index')
    return render(request, 'doc.html', {'title': 'Index', 'text': format_doc('__App__/Index')})


@login_required(login_url='/login')
def edit_form (request, title=None):
    '''
    Create a form for editing the object details
    '''
    print 'form: %s'%(title)
    name = user(request)
    doc = join(name,title)
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if request.POST.get('cancel', None):
            # TODO: set real cancel redirect
            #title = form.data['path']
            if not title:
                title = 'Home'
            return redirect('Index')
        else:
            if form.is_valid():
                print 'save: %s'%(title)
                write_doc(doc, form.cleaned_data['body'])
                return redirect(title)
    else:
        note =  Note()
        if  title:
            note.path = title
            if is_doc(doc):
                print 'read: %s'%(title)
                note.body = read_doc(doc)
        form =  NoteForm(instance=note)
    data =  { 'form': form, 'title': title  }
    return render(request, 'edit.html', data)


def add(request,title,template):
    '''
    Render the add view
    '''
    print 'add: %s, %s'%(title,template)
    clone_template(join(user(request),title))
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
    delete_doc (join(user(request),title))
    return redirect(dirname(title))

  
# Sample code:
#    if request.user.is_anonymous(): return 0
#    if not request.user.is_superuser:  return redirect('/NoAccess') 
#    u = UserAccount.objects.get(pk=request.user.pk).pk
#    if not u==user_id:    return redirect('/NoAccess')

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/ThankYou")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {
        'form': form,
    })
