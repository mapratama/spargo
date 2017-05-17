"""
Django settings for spargo project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from os import path

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SETTINGS_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.dirname(SETTINGS_DIR)
PROJECT_NAME = os.path.basename(PROJECT_ROOT)

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = path.join(PROJECT_ROOT, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'e!h_vh(ifaabuxv-68f0wf6*k91ooae9y*lg+*_+v674f5+1_!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'django_rq',

    'spargo.apps.banks',
    'spargo.apps.banners',
    'spargo.apps.categories',
    'spargo.apps.jne',
    'spargo.apps.j_and_t',
    'spargo.apps.models',
    'spargo.apps.orders',
    'spargo.apps.photos',
    'spargo.apps.products',
    'spargo.apps.types',
    'spargo.apps.users',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

JPEGTRAN_COMMAND = "jpegtran -copy none -progressive -optimize -outfile '%(filename)s'.diet "\
                   "'%(filename)s' && mv '%(filename)s.diet' '%(filename)s'"

STANDARD_POST_PROCESSORS = [{'PATH': 'thumbnails.post_processors.optimize',
                             'png_command': 'optipng -force -o3 %(filename)s',
                             'jpg_command': JPEGTRAN_COMMAND}]

THUMBNAILS = {
    'METADATA': {
        'PREFIX': 'thumbs',
        'BACKEND': 'thumbnails.backends.metadata.RedisBackend',
        'db': 2
    },
    'STORAGE': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage'
    },
    'BASE_DIR': 'thumb',
    'SIZES': {
        'size_90': {
            'PROCESSORS': [
                {'PATH': 'thumbnails.processors.resize', 'width': 90, 'height': 90, 'method': 'fill'},
                {'PATH': 'thumbnails.processors.crop', 'width': 90, 'height': 90},
            ],
            'POST_PROCESSORS': STANDARD_POST_PROCESSORS
        },
        'size_200': {
            'PROCESSORS': [
                {'PATH': 'thumbnails.processors.resize', 'width': 200, 'height': 200, 'method': 'fill'},
                {'PATH': 'thumbnails.processors.crop', 'width': 200, 'height': 200},
            ],
            'POST_PROCESSORS': STANDARD_POST_PROCESSORS
        },
        'size_400': {
            'PROCESSORS': [
                {'PATH': 'thumbnails.processors.resize', 'width': 400, 'height': 400, 'method': 'fill'}
            ],
            'POST_PROCESSORS': STANDARD_POST_PROCESSORS
        },
        'size_600x300': {
            'PROCESSORS': [
                {'PATH': 'thumbnails.processors.resize', 'width': 600, 'height': 300, 'method': 'fill'},
                {'PATH': 'thumbnails.processors.crop', 'width': 600, 'height': 300},
            ],
            'POST_PROCESSORS': STANDARD_POST_PROCESSORS
        },
        'source_800': {
            'PROCESSORS': [
                {'PATH': 'thumbnails.processors.resize', 'width': 800, 'height': 800, 'method': 'fill'},
                {'PATH': 'thumbnails.processors.crop', 'width': 800, 'height': 800},
            ],
        },
    }
}

ROOT_URLCONF = 'spargo.urls'

WSGI_APPLICATION = 'spargo.wsgi.application'

GOOGLE_API_KEY = "AIzaSyAi1QxOJZjcavE1a1frerCaOvbJtbXc5GU"

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/0',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    },
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

AUTH_USER_MODEL = 'users.User'
CACHED_AUTH_PREPROCESSOR = 'spargo.apps.users.models.cached_auth_preprocessor'
# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Jakarta'

USE_I18N = True

USE_L10N = True

USE_TZ = True

GOOGLE_API_KEY = "AIzaSyAi1QxOJZjcavE1a1frerCaOvbJtbXc5GU"

# DJANGO RQ SETTINGS
RQ_QUEUES = {
    'default': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 0
    }
}

if 'test' in os.sys.argv:
    TEST = True
else:
    TEST = False

try:
    from settings_local import *  # noqa
except ImportError:
    pass

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

