from django.contrib.auth.models import User
from django.db import models

class Cred(models.Model):
    TYPES = (("RECOMMEND", "Recommendation"), ("ARTICLE", "Article"), 
             ("CONTRIBUTE", "Contribution"))
    text = models.TextField()
    external_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(User, related_name='+')
    type = models.CharField(max_length=64, choices=TYPES)
    user = models.ForeignKey(User, related_name='creds')
    
class Link(models.Model):
    TYPES = (("FACEBOOK", "Facebook"), ("LINKEDIN", "LinkedIn"), 
             ("GITHUB", "GitHub"), ("BLOG", "Blog"))
    url = models.URLField()
    type = models.CharField(max_length=64, choices=TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name='links')