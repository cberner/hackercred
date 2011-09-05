from django.contrib.auth import logout as django_logout, login as django_login, \
    authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from hackercred.app.forms import RegistrationForm, PartialLinkForm, \
    PartialProjectForm, PartialCommentForm
from hackercred.app.models import Hacker, Link, Cred

def index(request):
    users = Hacker.objects.all()
    return render_to_response("index.html", {'users' : users,
                                             'registration_form' : RegistrationForm()}, 
                              context_instance=RequestContext(request))

def view_user(request, id):
    viewed_user = User.objects.get(id=id)
    comments = viewed_user.creds.filter(type="COMMENT")
    projects = viewed_user.creds.filter(type="PROJECT")
    return render_to_response("view_user.html", {'viewed_user': viewed_user, 
                                                 'comments' : comments, 
                                                 'projects' : projects,
                                                 'own_profile' : viewed_user == request.user,
                                                 'add_comment_form' : PartialCommentForm(initial={'type' : "COMMENT", 'user' : viewed_user})},
                              context_instance=RequestContext(request))

@login_required
def edit_profile(request):
    user = request.user
    comments = user.creds.filter(type="COMMENT")
    projects = user.creds.filter(type="PROJECT")
    return render_to_response("view_user.html", {'viewed_user': user, 
                                                 'comments' : comments, 
                                                 'projects' : projects,
                                                 'edit_mode' : True,
                                                 'add_link_form' : PartialLinkForm(),
                                                 'add_project_form' : PartialProjectForm(initial={'type' : "PROJECT", 'user' : user})},
                              context_instance=RequestContext(request))

@login_required
def create_comment(request):
    if request.method == "POST":
        form = PartialProjectForm(request.POST)
        if form.is_valid():
            data = form.clean()
            comment = Cred()
            comment.type = "COMMENT"
            comment.user = data['user']
            comment.added_by = request.user
            comment.text = data['text']
            comment.save()
            return HttpResponseRedirect(reverse(view_user, args=[data['user'].id]))
        
@login_required
def create_project(request):
    if request.method == "POST":
        form = PartialProjectForm(request.POST)
        if form.is_valid():
            data = form.clean()
            project = Cred()
            project.type = "PROJECT"
            project.user = data['user']
            project.external_url = data['external_url']
            project.added_by = request.user
            project.text = data['text']
            project.project_name = data['project_name']
            project.save()
            return HttpResponseRedirect(reverse(edit_profile))

@login_required
def delete_project(request, id):
    #It would be nice if this could be DELETE, but that didn't seem to work
    if request.method == "POST":
        try:
            project = Cred.objects.get(id=id)
            if project.user == request.user and project.type == "PROJECT":
                project.delete()
        except ObjectDoesNotExist:
            pass
        return HttpResponseRedirect(reverse(edit_profile))
    
@login_required
def create_link(request):
    if request.method == "POST":
        form = PartialLinkForm(request.POST)
        if form.is_valid():
            data = form.clean()
            link = Link()
            link.user = request.user
            link.url = data['url']
            link.type = data['type']
            link.save()
            return HttpResponseRedirect(reverse(edit_profile))

@login_required
def delete_link(request, id):
    #It would be nice if this could be DELETE, but that didn't seem to work
    if request.method == "POST":
        try:
            link = Link.objects.get(id=id)
            if link.user == request.user:
                link.delete()
        except ObjectDoesNotExist:
            pass
        return HttpResponseRedirect(reverse(edit_profile))
    
def logout(request):
    django_logout(request)
    return HttpResponseRedirect(reverse(index))

def register(request):
    if request.method == 'POST': # If the form has been submitted...
        form = RegistrationForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            form.save()
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            django_login(request, user)
            return HttpResponseRedirect(reverse(index)) # Redirect after POST
    else:
        form = RegistrationForm() # An unbound form

    return render_to_response("registration/register.html", {'form': form}, context_instance=RequestContext(request))