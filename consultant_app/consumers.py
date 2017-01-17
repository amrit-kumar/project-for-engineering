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


redis_conn = redis.Redis("localhost", port=6379)

@receiver(post_save, sender=Comment)
def send_update(sender, instance, **kwargs):
    print("++++++++++++++++++++++++++",redis_conn)
    print("send update function in consumers.py")
    # Loop through all reply channels and send the update
    for reply_channel in redis_conn.smembers("readers"):
        print("rrrrrrrrrrrrrrrrrrrr", redis_conn.smembers("readers"))
        Channel(reply_channel).send({
            "text": json.dumps({
                "content": "channel running"
            })
        })



@channel_session
def ws_connect(message):
    client=message.content['client']
    print("client in connect",client)
    server=message.content['server']
    print("server in connect",server)

    print("cccccccccccccccccccccccc",message.content,"######33",message.reply_channel)

    # Accept connection
    message.reply_channel.send({"accept": True})
    # Work out room name from path (ignore slashes)
    room = message.content['path'].strip("/")
    print("pathhhhhhhhhhhhhhh",message.content['path'])
    print("rooooooooooooooooooom",room)
    # Save room in session and add us to the group
    message.channel_session['room'] = room
    Group("chat-%s" % room).add(message.reply_channel)

# Connected to websocket.receive
@channel_session
def ws_message(message):
    # hi=message.session.session_key
    # print("************************",hi)
    print("rrrrrrrrrrrrrrrrrrrrrr",message.content,"$$$$$$$$$$$$$$$$$$$$",message.channel_session)

    Group("chat-%s" % message.channel_session['room']).send({
        "text": message['text'],
        # "notification":Notification.objects.all(),
    })

# Connected to websocket.disconnect
@channel_session
def ws_disconnect(message):

    print("ddddddddddddddddd",message.content)
    Group("chat-%s" % message.channel_session['room']).discard(message.reply_channel)

# def http_consumer(message):
#     # Make standard HTTP response - access ASGI path attribute directly
#     response = HttpResponse("Hello world! You asked for %s" % message.content['path'])
#     # response1=HttpResponse('/localhost:8000/')
#     # url = reverse('192.168.1.33:8000/')
#     # response1= HttpResponseRedirect(url)
#     print("HEYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY")
#     # Encode that response into message format (ASGI)
#     for chunk in AsgiHandler.encode_response(response):
#         message.reply_channel.send(chunk)