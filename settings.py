from djangoappengine.settings_base import *

import os

DEBUG = True
TEMPLATE_DEBUG = DEBUG

SECRET_KEY = 'h^*8i&wtn2nxxx!vq7)9qu$=yoja5($ei+ptbke6gehhz!q_6d'

INSTALLED_APPS = (
    'djangoappengine',
    'djangotoolbox',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',

    'portal',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
)

GOOGLEMAP_KEY = 'ABQIAAAAAgsL8nQfPb88CRkYuof-ARR74NuISGPxD1o9Y7ny4W1rvbN7tBTTxSUHohLWbnt2ic_eIoClxTpX5w'

DEFAULT_CHARSET = 'utf-8'
FILE_CHARSET = 'utf-8'

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/login/'

TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'

ADMIN_MEDIA_PREFIX = '/media/admin/'
MEDIA_ROOT = ''
MEDIA_URL = '/media/'
TEMPLATE_DIRS = (os.path.join(os.path.dirname(__file__), 'templates'))

ROOT_URLCONF = 'urls'
