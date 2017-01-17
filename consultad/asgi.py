import os
import channels.asgi

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "consultad.settings")
print("in asgi.py file")
channel_layer = channels.asgi.get_channel_layer()