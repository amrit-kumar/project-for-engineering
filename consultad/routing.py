from channels.routing import route
# from consultant_app.consumers import ws_add, ws_message, ws_disconnect
from consultant_app.consumers import ws_connect, ws_message, ws_disconnect
from consultant_app.consumers import ws_message

# channel_routing = [
#     route("http.request", "consultant_app.consumers.http_consumer"),
# ]

channel_routing = [
    route("websocket.connect", ws_connect),
    route("websocket.receive", ws_message),
    route("websocket.disconnect", ws_disconnect),
]
# channel_routing = [
#     route("websocket.connect", ws_add),
#     route("websocket.receive", ws_message),
#     route("websocket.disconnect", ws_disconnect),
# ]