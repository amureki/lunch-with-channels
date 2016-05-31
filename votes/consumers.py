import json

from channels import Channel, Group
from channels.auth import channel_session_user, channel_session_user_from_http

from core.utils import catch_client_error
from votes.models import Vote


@channel_session_user_from_http
def ws_connect(message):
    Group('votes', channel_layer=message.channel_layer).add(
        message.reply_channel)


def ws_receive(message):
    payload = json.loads(message['text'])
    payload['reply_channel'] = message.content['reply_channel']
    Channel('votes.receive', channel_layer=message.channel_layer).send(payload)


@channel_session_user
def ws_disconnect(message):
    Group('votes', channel_layer=message.channel_layer).discard(
        message.reply_channel)


@channel_session_user
@catch_client_error
def votes_update(message):
    place_id = message.content.get('place_id')
    username = message.content.get('username')
    Vote.update(place_id, username)
