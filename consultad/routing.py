from channels.routing import route
# from consultant_app.consumers import ws_add, ws_message, ws_disconnect
from consultant_app.consumers import ws_connect, ws_message, ws_disconnect,repeat_me
from consultant_app.consumers import ws_message
from django.conf.urls import url,include

# channel_routing = [
#     route("http.request", "consultant_app.consumers.http_consumer"),
# ]

channel_routing = [
    route("websocket.connect", ws_connect,path=r"^/chat"),
    route("websocket.receive", ws_message,path=r"^/chat"),
    route("websocket.disconnect", ws_disconnect),
    route("repeat-me", repeat_me),

]
# inner_routes = [
#     route("websocket.connect", repeat_me, path=r'^/stream/'),
# ]

# routing = [
#     include(inner_routes, path=r'^/repeat_me')
# ]
