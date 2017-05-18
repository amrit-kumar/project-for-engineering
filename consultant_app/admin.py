from django.contrib import admin
from .models import *
from versatileimagefield.registry import versatileimagefield_registry
from versatileimagefield.fields import VersatileImageField
from .versatilimagefield import *
from django.contrib import auth

class UserAdmin(admin.ModelAdmin):
    def render_change_form(self, request, context, *args, **kwargs):
         context['adminform'].form.fields['supporter'].queryset = User.objects.filter(role='supporter')
         return super(UserAdmin, self).render_change_form(request, context, args, kwargs)

class ProjectAdmin(admin.ModelAdmin):
    def render_change_form(self, request, context, *args, **kwargs):
         context['adminform'].form.fields['consultant'].queryset = User.objects.filter(role='consultant')
         return super(ProjectAdmin, self).render_change_form(request, context, args, kwargs)

class To_do_listAdmin(admin.ModelAdmin):
    def render_change_form(self, request, context, *args, **kwargs):
         context['adminform'].form.fields['user'].queryset = User.objects.filter(role='supporter')
         return super(To_do_listAdmin, self).render_change_form(request, context, args, kwargs)

class NotificationAdmin(admin.ModelAdmin):
    def render_change_form(self, request, context, *args, **kwargs):
         context['adminform'].form.fields['recipient'].queryset = User.objects.filter(role='supporter')
         return super(NotificationAdmin, self).render_change_form(request, context, args, kwargs)

class CommentAdmin(admin.ModelAdmin):
    def render_change_form(self, request, context, *args, **kwargs):
         context['adminform'].form.fields['supporter'].queryset = User.objects.filter(role='supporter')
         return super(CommentAdmin, self).render_change_form(request, context, args, kwargs)


class SkillsetAdmin(admin.ModelAdmin):
    def render_change_form(self, request, context, *args, **kwargs):
         context['adminform'].form.fields['supporter'].queryset = User.objects.filter(role='supporter')
         return super(SkillsetAdmin, self).render_change_form(request, context, args, kwargs)


admin.site.register(User, UserAdmin)
admin.site.register(Project,ProjectAdmin)
admin.site.register(To_do_list,To_do_listAdmin)
admin.site.register(Notification,NotificationAdmin)
admin.site.register(Comment,CommentAdmin)
admin.site.register(Technology)
admin.site.register(SkillSet,SkillsetAdmin)

admin.site.register(Eventshigh)
admin.site.register(Goeventz)
admin.site.register(Bookmyshow)
admin.site.register(Meraevents)
admin.site.register(Insider)





