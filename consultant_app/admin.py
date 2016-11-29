from django.contrib import admin
from .models import *

admin.site.register(Project)

admin.site.register(Comment)


class UserAdmin(admin.ModelAdmin):
    exclude = ('password',)

admin.site.register(User,UserAdmin)
