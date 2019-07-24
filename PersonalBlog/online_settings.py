DEBUG = False
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/opt/db/db.sqlite3',
    }
}

STATIC_ROOT='/opt/static/django'

FILE_BASE_HOST_NAME = 'http://perblog.natapp1.cc/doc'
VIDEO_BASE_HOST_NAME = 'http://perblog.natapp1.cc/video'
