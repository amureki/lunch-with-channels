import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
os.environ.setdefault('DJANGO_CONFIGURATION', 'Dev')

from configurations.wsgi import get_wsgi_application  # NoQA
from raven.contrib.django.raven_compat.middleware.wsgi import Sentry  # NoQA
from whitenoise.django import DjangoWhiteNoise  # NoQA


application = DjangoWhiteNoise(get_wsgi_application())

from django.conf import settings  # NoQA

if not settings.DEBUG:
    application = Sentry(application)
