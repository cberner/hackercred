from django.contrib.auth.models import User
from django.db import models

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