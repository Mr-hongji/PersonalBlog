DEBUG = True
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

FILE_BASE_HOST_NAME = ''
VIDEO_BASE_HOST_NAME = ''
DOC_ROOT_PATH = 'e:/'
VIDEO_ROOT_PATH='h:/'
uploadFilePath="../static/uploadfiles/articleImages/"
