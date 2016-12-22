from . models import *
from django.dispatch import Signal
from django.db.models.signals import pre_save, pre_delete, post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from consultant_app.models import *
import django.dispatch
from django.core.signals import request_finished

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
        consultant=abc.consultant.username
        consultant=User.objects.get(username=consultant)

        recipient=consultant.supporter
        Notification.objects.create(
            recipient=recipient,
            project=obj,
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
            text="Supporter %s has completed project %s" % (consultant.supporter, obj.title)
        )
        return None

@receiver(pre_save, sender=User)
def send_update(sender, **kwargs):
    obj = kwargs.get('instance')
    print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",obj)
    if obj.role == 'consultant':
        recipient = obj.supporter
        Notification.objects.create(
            recipient=recipient,
            text="You have been assigned a new consultant %s" % obj.username
        )
        return None
    flag=False
    for i in User.objects.all():
        if i.username == obj.username:
            flag= True
            break;

    if flag==False:
        if obj.role == 'supporter' and obj.is_superuser!=True:
            recipient = User.objects.get(is_superuser=True)
            Notification.objects.create(
                recipient=recipient,
                text="A new supporter %s has been registered" % obj.username
            )
            return None

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
            text= "%s has commented on %s" % (obj.supporter, obj.project)
        )
        return None
    else:
        if obj.supporter.is_superuser:
            Notification.objects.create(
                recipient=obj.project.consultant.supporter,
                comment=obj,
                project=obj.project,
                text="%s has commented on %s" % (obj.supporter, obj.project)

            )
            return Comment.pk

@receiver(post_save, sender=User)
def send_update(sender, **kwargs):
    obj = kwargs.get('instance')
    print("bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",obj)
    # if obj.role == 'consultant':
    #     recipient = obj.supporter
    #     Notification.objects.create(
    #
    #         recipient=recipient,
    #         text="You have been assigned a new consultant %s" % obj.username
    #     )
    #     return None
    # flag=False
    # for i in User.objects.all():
    #     if i.username == obj.username:
    #         flag= True
    #         break;
    #
    # if flag==False:
    if obj.role == 'consultant':
        # sender = User.objects.get(username=obj.username)
        recipient=User.objects.get(is_superuser=True)
        # if recipient
        # recipient = obj.username
        print("recipient tttttttttttttttt",recipient)

        Notification.objects.create(
            sender=obj,
            recipient=recipient,
            text="You have been assigned a new consultant %s" % obj.username
        )
        return None

    # return None



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



#In these cases, you can register to receive signals sent only by particular senders

# def save_profile(sender, instance, **kwargs):
#     instance.profile.save()


#
# @receiver(post_save, sender=Project)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         print("Request finished!!!!!!!!!!!!!!!!!!!!")
#         Notification.objects.create(user=instance)
#
# @receiver(post_save, sender=Project)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()


# post_save.connect(save_profile, sender=User)
# Signal.connect(receiver, sender=None, weak=True, dispatch_uid=None)
#Defining signals
# pizza_done = django.dispatch.Signal(providing_args=["toppings", "size"])
# @receiver(pre_save, sender=Project)
#sender is model name
# def my_handler(sender, **kwargs):
#     ...

#The my_handler function will only be called when an instance of MyModel is saved.
# @receiver(request_finished)
# def my_callback(sender, **kwargs):
#     print("Request finished!")


# request_finished.connect(my_callback, dispatch_uid="my_unique_identifier")


#end result is that your receiver function will only be bound to the
#  signal once for each unique dispatch_uid value:

#connecting and disconnecting signals


