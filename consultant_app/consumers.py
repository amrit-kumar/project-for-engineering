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
import base64
from django.dispatch import Signal
from django.db.models.signals import pre_save, pre_delete, post_save, post_delete
from urllib import parse
from channels.auth import http_session_user, channel_session_user, channel_session_user_from_http
import logging
import ast
from django.utils.encoding import force_text
from django.core.cache import cache
from consultant_app.models import User
from http.cookies import SimpleCookie as cookie






redis_conn = redis.Redis("localhost", port=6379)

# @receiver(post_save, sender=Comment)
# def send_update(sender, instance, **kwargs):
#     print("send update function in consumers.py")
#     # Loop through all reply channels and send the update
#     for reply_channel in redis_conn.smembers("readers"):
#         print("rrrrrrrrrrrrrrrrrrrr", redis_conn.smembers("readers"))
#         Channel(reply_channel).send({
#             "text": json.dumps({
#                 "content": "channel running"
#             })
#         })


# @receiver(post_save, sender= Comment,**kwargs)
# @channel_session
#
@channel_session_user_from_http
def ws_connect(message):
    print("ccccccccccccccccccccccc ",message.content)
    # print("sessioniddddddddddd",message.content['headers'][0][1],"user is..",message.channel_session.__dict__['_session_cache']['_auth_user_id'])
    # cookiestring = "\n".join(message.headers.get_all('Cookie', failobj=[]))
    # c = cookie()
    # c.load(cookiestring)
    # n=Notification.objects.filter(unread=True)
    # serializers=Nserializer(n,many=True)

    message.reply_channel.send({"accept": True})
    room = message.content['path'].strip("/")
    message.channel_session['room'] = room
    Group("chat-%s" % room).add(message.reply_channel)

    # session = cache.get('sessionid')
    # s = message.Session()
    # c=s.cookies
    # print("CCCCCCCCCCCCc",c)


    # session='3hqb6wlupk9361ajmv6e3fh8atp4bwdm'
    # data = session.get_decoded()
    # uid = data.get('_auth_user_id', None)
    # user = User.objects.get(id=uid)
    # Group("chat-%s" % message.user.username).add(message.reply_channel)

    # for i in serializers.data:
    # Group("chat-%s" % room).send({
        # "text": message['text'],
        # "text": str(serializers.data)
        # })

# @channel_session_user
@channel_session
def ws_message(message):
    # user=User.objects.get(id=16)
    # try:
        print("rrrrrrrrrrrrrrrrrrrrrr",message.content)
        print("TEXT IN SEND ",message.content['text'])
        data1=message.content['text']
        # var1=json.loads(data1)

        # print("!!!!!!!!!!!!!!!!!!!!!!!",var1,"|||||||||||||||||",type(var1))
        # comment=ast.literal_eval(message.content['text'])
        # print("project%%",var1['project'],"supporter%%",var1['supporter'])
        project=Project.objects.get(id=53)
        user=User.objects.get(id=16)




# except:
    #     print("sorry")
    # else:
        n = Notification.objects.create(text="%s has commented on %s" % (user.username, project.title),
                                        recipient=project.consultant.supporter, type='commented',
                                        )
        serializers = Nserializer(n)
        serializers.data['comment']=message.content['text']
        hi=serializers.data

        # Group("chat-%s" % message.user.username[0]).send({
        # "text": str(serializers.data),
        Group("chat-%s" % message.channel_session['room']).send(content={
            'text': json.dumps({
                'message': message.content['text'],
                'data': hi,
            # "text": message['text'],
            # "text": str(serializers.data),
            })
                },

            # {
            # 'text': json.dumps({
            #     'message': message.content['text'],
            #     'data': hi,
            # # "text": message['text'],
            # # "text": str(serializers.data),
            # })
            #     }
        )

# Connected to websocket.disconnect
@channel_session_user
def ws_disconnect(message):

    print("ddddddddddddddddd",message.content)
    # Group("chat-%s" % message.user.username[0]).discard(message.reply_channel)

    Group("chat-%s" % message.channel_session['room']).discard(message.reply_channel)


def repeat_me(message):
    print("repeatttttttttttttttttttttt",message.content['info']['text'])
    #here message.content['info'] is dict and it can be string
    Group("chat").send({
    "text": json.dumps({'status': message.content['status'], 'info':
     message.content['info']})
     })

@channel_session
def ws_echo(message):
    print("eeeeeeeeeeeeeeecccccchooooooo")
    if 'username' not in message.channel_session:
        return
    room = message.channel_session['room']
    logging.info('Echoing message %s from username %s in room %s',
                 message.content['text'], message.channel_session['username'],
                 room)