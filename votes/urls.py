from channels import route

from .consumers import (
    ws_connect, ws_receive, ws_disconnect, votes_update
)

websocket_routing = [
    route('websocket.connect', ws_connect),
    route('websocket.receive', ws_receive),
    route('websocket.disconnect', ws_disconnect),
]

votes_routing = [
    route('votes.receive', votes_update, command='^update$'),
]
