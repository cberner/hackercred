from django import forms
from django.contrib.auth.models import User
from django.core import validators
from hackercred.app.models import Link, Cred, UserProfile
 
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
        u = User.objects.create_user(username=self.cleaned_data['email'],
                                     email=self.cleaned_data['email'],
                                     password=self.cleaned_data['password'])
        u.first_name = self.cleaned_data['first_name']
        u.last_name = self.cleaned_data['last_name']
        u.save()
        return u

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
                   'text' : forms.Textarea(attrs={'cols': 60, 'rows':5})}


















