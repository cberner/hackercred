from django.contrib import admin
from hackercred.app.models import Link, Cred, UserProfile

admin.site.register(Link)
admin.site.register(Cred)
admin.site.register(UserProfile)
