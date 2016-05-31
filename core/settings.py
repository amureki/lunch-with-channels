import os
from urllib.parse import urlparse

from configurations import Configuration, values
from django.core.urlresolvers import reverse_lazy


class Common(Configuration):
    PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
    BASE_DIR = os.path.abspath(os.path.join(PROJECT_DIR, os.pardir))

    # Quick-start development settings - unsuitable for production
    # See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = 'secret'

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True

    ALLOWED_HOSTS = []

    # Application definition

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.gis',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',

        'channels',
        'stdimage',

        'core',
        'places',
        'votes'
    ]

    MIDDLEWARE_CLASSES = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'core.middleware.UsernameMiddleware',
    ]

    ROOT_URLCONF = 'core.urls'

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': False,
            'OPTIONS': {
                'context_processors': [
                    'django.contrib.auth.context_processors.auth',
                    'django.template.context_processors.debug',
                    'django.template.context_processors.i18n',
                    'django.template.context_processors.media',
                    'django.template.context_processors.static',
                    'django.template.context_processors.request',
                    'django.template.context_processors.tz',
                    'django.template.context_processors.csrf',
                    'django.contrib.messages.context_processors.messages',
                ],
                'loaders': [
                    ('core.loaders.ProductionCachedLoader', [
                        'django.template.loaders.filesystem.Loader',
                        'django.template.loaders.app_directories.Loader',
                    ]),
                ],
            },
        },
    ]

    WSGI_APPLICATION = 'core.wsgi.application'

    DATABASES = values.DatabaseURLValue(
        default='postgres://localhost/lunchtime',
        conn_max_age=None,
    )

    AUTH_PASSWORD_VALIDATORS = [
        {
            'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
        },
    ]

    SITE_ID = 1
    SITE_URL = values.URLValue(environ_prefix='',
                               default='http://localhost:8000')

    INTERNAL_IPS = (
        '127.0.0.1',
    )

    # Internationalization
    # https://docs.djangoproject.com/en/1.9/topics/i18n/

    LANGUAGE_CODE = 'en-us'

    TIME_ZONE = 'Europe/Berlin'

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/1.9/howto/static-files/

    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, '_static')
    MEDIA_URL = values.Value(default='http://127.0.0.1:8000/media/', environ_prefix='')

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,
        'root': {
            'level': 'DEBUG' if DEBUG else 'INFO',
            'handlers': ['console', 'sentry'],
        },
        'formatters': {
            'verbose': {
                'format': '%(levelname)-8s %(name)s: %(message)s',
            },
        },
        'handlers': {
            'sentry': {
                'level': 'WARNING',
                'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose'
            },
        },
        'loggers': {
            'django': {
                'handlers': ['console'],
                'propagate': False,
                'level': 'INFO',
            },
            'raven': {
                'level': 'WARNING',
                'handlers': ['console'],
                'propagate': False,
            },
            'sentry.errors': {
                'level': 'WARNING',
                'handlers': ['console'],
                'propagate': False,
            },
        },
    }

    IMAGE_THUMBNAIL_VARIATIONS = {
        'xs': (128, 128),
        'xs_cropped': (128, 128, True),
        's': (300, 200),
        's_cropped': (300, 200, True),
        'm': (640, 480),
        'm_cropped': (640, 480, True),
        'l': (1024, 768),
        'l_cropped': (1024, 768, True),
    }

    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'asgi_redis.RedisChannelLayer',
            'CONFIG': {
                'hosts': [os.environ.get('REDIS_URL', 'redis://localhost:6379')],
            },
            'ROUTING': 'core.urls.channel_routing',
        },
    }


class Dev(Common):
    @property
    def MEDIA_PATH(self):  # NoQA
        o = urlparse(self.MEDIA_URL)
        return o.path

    MEDIA_ROOT = values.PathValue(os.path.join(Common.BASE_DIR, '_media'),
                                  check_exists=False)
    DEBUG = True


class Prod(Common):
    DEBUG = False
    SECRET_KEY = values.SecretValue()
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

    INSTALLED_APPS = [
        'raven.contrib.django.raven_compat',
    ] + Common.INSTALLED_APPS

    MIDDLEWARE_CLASSES = [
        'django.middleware.security.SecurityMiddleware',
    ] + Common.MIDDLEWARE_CLASSES

    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True

    ALLOWED_HOSTS = [
        '*',  # heroku will filter for us
    ]
