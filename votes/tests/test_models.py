import pytest

from votes.models import Vote


@pytest.mark.django_db
class TestVote:
    def test_update(self, place, username):
        assert not Vote.objects.exists()
        Vote.update(place.id, username)
        assert Vote.objects.exists()
