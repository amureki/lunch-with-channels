from django.views.generic import ListView

from .models import Place


class PlaceListView(ListView):
    model = Place
