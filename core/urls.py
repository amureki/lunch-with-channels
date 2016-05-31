from channels import include as routing_include
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin

from places.views import PlaceListView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', PlaceListView.as_view(), name='index'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_PATH,
                          document_root=settings.MEDIA_ROOT)

channel_routing = [
    routing_include('votes.urls.websocket_routing', path=r'^/votes/stream'),
    routing_include('votes.urls.votes_routing'),
]
