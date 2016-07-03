from django.views.generic import ListView

from .models import Place


class PlaceListView(ListView):
    model = Place
    ordering = '?'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['most_wanted'] = self.model.most_wanted()
        return context
