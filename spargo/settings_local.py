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

RAVEN_CONFIG = {}

HOST = 'http://192.168.43.213:8000'
