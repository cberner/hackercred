from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core import validators
from hackercred.app.models import Link, Cred, UserProfile
import random
import string
 
def uniqueEmail(field_data):
    try:
        User.objects.get(email=field_data)
    except User.DoesNotExist:
        return
    raise validators.ValidationError('The email address "%s" is already in use.' % field_data) 

class RegistrationForm(forms.Form):
    first_name = forms.CharField(min_length=1, max_length=30, validators=[validators.RegexValidator(
                regex="^[a-zA-Z\-']*$", message=u"Only letters, hyphens, and apostrophes are allowed", code="custom")])
    last_name = forms.CharField(min_length=1, max_length=30, validators=[validators.RegexValidator(
                regex="^[a-zA-Z\-']*$", message=u"Only letters, hyphens, and apostrophes are allowed", code="custom")])
    email = forms.EmailField(validators=[uniqueEmail])
    password = forms.CharField(label="Password", min_length=1, max_length=30, widget=forms.PasswordInput)
    
    def save(self):
        #We use email as the primary key, but the username is required. So make a random one, 
        #and prefix it with @@@@@ so that we can tell it apart from users who have set their username
        random_username = "@@@@@" + "".join([random.choice(string.letters) for i in xrange(20)])
        #Lower case the email address, so that the same one can't be registered with different casing.
        u = User.objects.create_user(username=random_username,
                                     email=self.cleaned_data['email'].lower(),
                                     password=self.cleaned_data['password'])
        u.first_name = self.cleaned_data['first_name']
        u.last_name = self.cleaned_data['last_name']
        u.save()
        return u

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super(LoginForm, self).__init__(*args, **kwargs)


    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(email=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError("Please enter a correct email address and password. Note that both fields are case-sensitive.")
            elif not self.user_cache.is_active:
                raise forms.ValidationError("This account is inactive.")
        self.check_for_test_cookie()
        return self.cleaned_data

    def check_for_test_cookie(self):
        if self.request and not self.request.session.test_cookie_worked():
            raise forms.ValidationError(
                _("Your Web browser doesn't appear to have cookies enabled. "
                  "Cookies are required for logging in."))

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache

class PartialProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('job_title', 'employer')

class PartialLinkForm(forms.ModelForm):
    class Meta:
        model = Link
        fields = ('type', 'url')
        exclude = ('user',)
        
class PartialProjectForm(forms.ModelForm):
    class Meta:
        model = Cred
        fields = ('project_name', 'external_url', 'text', 'user', 'type')
        exclude = ('added_by')
        widgets = {'user': forms.HiddenInput(), 'type' : forms.HiddenInput()}

class PartialCommentForm(forms.ModelForm):
    class Meta:
        model = Cred
        fields = ('text', 'user', 'type')
        exclude = ('project_name', 'external_url')
        widgets = {'user': forms.HiddenInput(), 'type' : forms.HiddenInput(), 
                   'text' : forms.Textarea(attrs={'cols': 10, 'rows':5})}


















