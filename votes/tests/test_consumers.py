import json

import pytest
from asgiref.inmemory import ChannelLayer as InMemoryChannelLayer
from channels import Group
from channels.message import Message
from django.contrib.sessions.backends.file import SessionStore as FileSessionStore

from votes.consumers import ws_connect, ws_receive, ws_disconnect, votes_update


@pytest.fixture
def message_factory(settings, tmpdir):
    def factory(name, **content):
        channel_layer = InMemoryChannelLayer()
        message = Message(content, name, channel_layer)
        settings.SESSION_FILE_PATH = str(tmpdir)
        message.channel_session = FileSessionStore()
        return message
    return factory


@pytest.mark.django_db
def test_ws_connect(message_factory):
    message = message_factory(
        'votes',
        path='/votes/stream',
        client=['10.0.0.1', 12345],
        reply_channel='test-reply',
    )
    ws_connect(message)
    assert 'test-reply' in message.channel_layer._groups['votes']


@pytest.mark.django_db
def test_ws_receive(message_factory):
    message = message_factory(
        'test',
        text=json.dumps({'message': 'M'}),
        reply_channel='test-reply',
    )
    Group('votes', channel_layer=message.channel_layer).add('test-reply')

    ws_receive(message)

    _, reply = message.channel_layer.receive_many(['votes.receive'])
    assert reply['message'] == 'M'
    assert reply['reply_channel'] == 'test-reply'


@pytest.mark.django_db
def test_ws_disconnect(message_factory):
    message = message_factory('test', reply_channel='test-reply1')
    Group('votes', channel_layer=message.channel_layer).add('test-reply1')
    Group('votes', channel_layer=message.channel_layer).add('test-reply2')

    ws_disconnect(message)
    assert 'test-reply1' not in message.channel_layer._groups['votes']


@pytest.mark.django_db
def test_votes_update(message_factory, place, username):
    message = message_factory(
        'test',
        reply_channel='test-reply',
        command='update',
        place_id=place.id,
        username=username,
    )
    votes_update(message)
    assert place.vote_set.count() == 1
