import pytest


@pytest.mark.django_db
class TestPlace:
    def test_today_rating(self, place, vote, username):
        assert place.today_rating == 1

    def test_voters(self, place, vote, username):
        assert username in place.voters

    def test_voted_by(self, place, vote, username):
        assert place.voted_by(username)
