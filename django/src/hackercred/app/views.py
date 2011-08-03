from django.contrib.auth import logout as django_logout, login as django_login, \
    authenticate
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from hackercred.app.forms import RegistrationForm

def index(request):
    return render_to_response("index.html", context_instance=RequestContext(request))

def view_user(request, id):
    viewed_user = User.objects.get(id=id)
    return render_to_response("view_user.html", {'viewed_user': viewed_user}, context_instance=RequestContext(request))

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