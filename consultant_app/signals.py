from django.db.models.signals import post_save
from . models import *
from django.dispatch import Signal
from django.db.models.signals import pre_save, pre_delete, post_save, post_delete
from django.dispatch import receiver
from django.shortcuts import get_object_or_404, render
from rest_framework.authtoken.models import Token

post_update = Signal(providing_args = ['instance'])
from django.http import HttpResponse,HttpResponseRedirect
from channels.handler import AsgiHandler
from django.core.urlresolvers import reverse
from channels import Group, Channel
from channels.sessions import channel_session
import redis
from django.db.models.signals import pre_save, pre_delete, post_save, post_delete
from django.dispatch import receiver
import json
from .views import *
from .models import *

from consultant_app.consumers import *


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
def project_notify(sender, created,**kwargs):

    obj = kwargs.get('instance')
    if obj.status=='pending' and created == True :
        abc= Project.objects.get(title=obj.title)
        consultant=abc.consultant
        consultant=User.objects.get(username=consultant)
        admin=User.objects.get(is_superuser=True)
        recipient=consultant.supporter
        if recipient is not None:
            Notification.objects.create(
                recipient=recipient,
                project=obj,
                type="assigned_project",
                send_by=admin,
                text="Your consultant %s has been assigned a new project %s" % (consultant.username,obj.title)
            )
        else:
            return None

    if obj.status == 'completed' and created == False:
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
def send_update(sender,created, **kwargs):
    obj = kwargs.get('instance')
    if obj.role == 'consultant':
        try:
            send_by=User.objects.get(is_superuser=True)
            bcd='You have been assigned a new consultant %s'% obj.username
            abc=get_object_or_404(Notification,send_by=send_by,recipient=obj.supporter,text=bcd)
            return None
        except:
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
        else:
            return None
    try:
        abc= get_object_or_404(Token,user=obj)
        return None
    except:
            if obj.role == 'supporter' and obj.is_superuser!=True and obj.is_active==False and created == True:
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


redis_conn = redis.Redis("localhost", 6379)
@receiver(post_save, sender= Comment)
def comment_recieved(sender,created,**kwargs):
    obj= kwargs.get('instance')
    if obj.supporter.is_superuser is False and created == True:
        if obj.project.consultant.supporter == obj.supporter:
            recipient=User.objects.get(is_superuser=True)
            print("chalaaaaaaaaaaaaaaaaaaaaaaaaa")
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
            if obj.project.consultant.supporter != obj.supporter:
                print("22222222222222222")
                recipient1 = User.objects.get(is_superuser=True)
                hi=Notification.objects.create(
                    recipient=recipient1,
                    comment=obj,
                    project=obj.project,
                    type="commented",
                    send_by=obj.supporter,
                    text="%s has commented on %s" % (obj.supporter, obj.project))
                serializers = Nserializer(hi)
                info = serializers.data
                Channel('repeat-me').send({'info': info, 'status': True})



                recipient2 = User.objects.get(username=obj.project.consultant.supporter.username)
                if recipient1 !=recipient2:
                    print("33333333333333333333")
                    Notification.objects.create(
                        recipient=recipient2,
                        comment=obj,
                        project=obj.project,
                        type="commented",
                        send_by=obj.supporter,
                        text="%s has commented on %s" % (obj.supporter, obj.project))
                else:
                    pass

        return None

    else:
        if obj.supporter.is_superuser and obj.project.consultant.supporter.is_superuser is False and created == True:
            print("44444444444444444444444")
            recipient=obj.project.consultant.supporter
            Notification.objects.create(
                recipient=recipient,
                comment=obj,
                project=obj.project,
                type="commented",
                send_by=obj.supporter,
                text="%s has commented on %s" % (obj.supporter, obj.project)
            )
            return None



#
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