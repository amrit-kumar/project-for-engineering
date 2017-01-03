from django.db.models.signals import post_save
from . models import *
from django.dispatch import Signal
from django.db.models.signals import pre_save, pre_delete, post_save, post_delete
from django.dispatch import receiver
from django.shortcuts import get_object_or_404, render
from rest_framework.authtoken.models import Token

post_update = Signal(providing_args = ['instance'])




# @receiver(post_save, sender=Project)
# def project_notification(sender, **kwargs):
#
#     obj = kwargs.get('instance')
#     abc = Project.objects.get(title=obj.title)
#     consultant = abc.consultant
#     consultant = User.objects.get(username=consultant)
#     if obj.status == 'completed':
#         recipient = User.objects.get(is_superuser=True)
#         Notification.objects.create(
#             recipient=recipient,
#             project=obj,
#             text="Supporter %s has completed project %s" % (consultant.supporter, obj.title)
#         )
#         return None


@receiver(post_save, sender=Project)
def project_notify(sender, **kwargs):

    obj = kwargs.get('instance')
    if obj.status=='pending':
        abc= Project.objects.get(title=obj.title)
        consultant=abc.consultant
        consultant=User.objects.get(username=consultant)
        admin=User.objects.get(is_superuser=True)
        recipient=consultant.supporter
        Notification.objects.create(
            recipient=recipient,
            project=obj,
            type="assigned_project",
            send_by=admin,
            text="Your consultant %s has been assigned a new project %s" % (consultant.username,obj.title)
        )
    if obj.status == 'completed':
        abc = Project.objects.get(title=obj.title)
        consultant = abc.consultant
        consultant = User.objects.get(username=consultant)
        recipient = User.objects.get(is_superuser=True)
        Notification.objects.create(
            recipient=recipient,
            project=obj,
            type="project_completed",
            send_by=consultant.supporter,
            text="Supporter %s has completed project %s" % (consultant.supporter, obj.title)
        )
        return None
@receiver(post_save, sender=User)
def send_update(sender, created,**kwargs):
    obj = kwargs.get('instance')
    if obj.role == 'consultant' and created:
        recipient = obj.supporter
        admin=User.objects.get(is_superuser=True)
        if recipient is not None:
            Notification.objects.create(
                recipient=recipient,
                type="assigned_consultant",
                send_by=admin,
                text="You have been assigned a new consultant %s" % obj.username
            )
            return None
        else:
            return None
    try:
        abc= get_object_or_404(Token,user=obj)
        return None
    except:
            if obj.role == 'supporter' and obj.is_superuser!=True:
                recipient = User.objects.get(is_superuser=True)
                Notification.objects.create(
                    recipient=recipient,
                    send_by=obj,
                    type="registered",
                    text="A new supporter %s has been registered" % obj.username
                )
                return None
            else:
                return None
@receiver(post_save, sender= Comment)
def comment_recieved(sender,**kwargs):
    obj= kwargs.get('instance')
    if obj.supporter.role=='supporter':
        recipient=User.objects.get(is_superuser=True)
        Notification.objects.create(
            recipient= recipient,
            comment= obj,
            project=obj.project,
            type="commented",
            send_by=obj.supporter,
            text= "%s has commented on %s" % (obj.supporter, obj.project)
        )
        return None
    else:
        if obj.supporter.is_superuser:
            Notification.objects.create(
                recipient=obj.project.consultant.supporter,
                comment=obj,
                project=obj.project,
                type="commented",
                send_by=obj.supporter,
                text="%s has commented on %s" % (obj.supporter, obj.project)

            )
            return None


# @receiver(post_save, sender=User)
# def send_update(sender,**kwargs):
#     obj=kwargs.get('instance')
#     if obj.role == 'supporter':
#         recipient = User.objects.get(is_superuser=True)
#         Notification.objects.create(
#             recipient=recipient,
#             text="A new supporter %s has been registered" % obj.username
#         )
#         return None