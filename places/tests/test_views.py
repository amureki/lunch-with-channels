import pytest
from django.core.urlresolvers import reverse


@pytest.mark.django_db
class TestPlaceListView:
    def test_200(self, client):
        url = reverse('index')
        response = client.get(url)
        assert response.status_code == 200

    def test_most_wanted(self, client, vote):
        url = reverse('index')
        response = client.get(url)
        assert response.status_code == 200
        assert vote.place.name in response.context['most_wanted']
