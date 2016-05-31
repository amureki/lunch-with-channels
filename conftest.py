import pytest
from django.contrib.gis.geos import Point

from model_mommy import mommy
from model_mommy.generators import gen_string

from core.utils import generate_name
from places.models import Place
from votes.models import Vote


@pytest.fixture
def username():
    username = generate_name()
    return username


@pytest.fixture
def place():
    place = mommy.make(
        Place,
        name=gen_string(15), address=gen_string(15),
        location=Point(52, 13, srid=4326)
    )
    return place


@pytest.fixture
def vote(username, place):
    return mommy.make(Vote, username=username, place=place)
