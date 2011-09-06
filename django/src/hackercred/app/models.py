from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

class Hacker(User):
    def projects(self):
        return self.creds.filter(type="PROJECT")
    
    class Meta:
        proxy = True

class Cred(models.Model):
    TYPES = (("PROJECT", "Project"), ("COMMENT", "Comment"))
    text = models.TextField()
    #Only used for PROJECT
    project_name = models.CharField(max_length=128, blank=True)
    #Only used for project
    external_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(User, related_name='+')
    type = models.CharField(max_length=64, choices=TYPES)
    user = models.ForeignKey(User, related_name='creds')
    
    def __unicode__(self):
        return "%s [%s] %s" % (self.user, self.type, self.text)
    
class Link(models.Model):
    TYPES = (("FACEBOOK", "Facebook"), ("LINKEDIN", "LinkedIn"), 
             ("GITHUB", "GitHub"), ("BLOG", "Blog"))
    url = models.URLField()
    type = models.CharField(max_length=64, choices=TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name='links')
    
    def display_type(self):
        for t,d in Link.TYPES:
            if t == self.type:
                return d
        assert False
        
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    
    job_title = models.CharField(max_length=128, blank=True)
    employer = models.CharField(max_length=128, blank=True)
    
    def __unicode__(self):
        return self.user.username
    
    def employment_str(self):
        if self.job_title:
            return self.job_title + (" at %s" % self.employer if self.employer else "")
        else:
            return "employed at %s" % self.employer if self.employer else None
    
def create_user_profile(sender, instance, **kwargs):
    if 'created' in kwargs and kwargs['created']:
        profile = UserProfile()
        profile.user = instance
        profile.save()
    
post_save.connect(create_user_profile, User, dispatch_uid="app.models")