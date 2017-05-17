import sys
import os
from os import path

SETTINGS_DIR = path.dirname(__file__)
PROJECT_ROOT = path.dirname(SETTINGS_DIR)
PROJECT_NAME = path.basename(PROJECT_ROOT)
sys.path.append(path.join(PROJECT_ROOT, 'libraries'))
BASE_DIR = path.dirname(path.dirname(path.abspath(__file__)))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'spargo',
        'USER': 'postgres',
        'PASSWORD': 'anggacumi',
        'HOST': '',
        'PORT': '',
    }
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
        'APP_DIRS': False,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
        },
    },
]

RAVEN_CONFIG = {}

HOST = "http://192.168.0.11:8000"
