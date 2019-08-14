"""
Django settings for PersonalBlog project.

Generated by 'django-admin startproject' using Django 2.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

from .environment import ENV

import os

current_env = ENV()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '6^ya9(0ryi)41rb=ba1@u*+!yrg(ll=k+t0vt3#2(^tok63@-u'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = current_env.get_config("DEBUG")

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog.apps.BlogConfig',
    'shop',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'PersonalBlog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'PersonalBlog.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = current_env.get_config("DATABASES")



# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'perblog',
#         'USER': 'root',
#         'PASSWORD': '123456',
#         'HOST': '127.0.0.1',
#         'PORT': '3306',
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
#STATIC_ROOT='/opt/static/django'
if current_env.get_config("STATIC_ROOT"):
    globals()["STATIC_ROOT"] = current_env.get_config("STATIC_ROOT")

if current_env.get_config("DOC_ROOT_PATH"):
    globals()["DOC_ROOT_PATH"] = current_env.get_config("DOC_ROOT_PATH")

if current_env.get_config("VIDEO_ROOT_PATH"):
    globals()["VIDEO_ROOT_PATH"] = current_env.get_config("VIDEO_ROOT_PATH")

FILE_BASE_HOST_NAME = current_env.get_config("FILE_BASE_HOST_NAME")
VIDEO_BASE_HOST_NAME = current_env.get_config("VIDEO_BASE_HOST_NAME")

STATIC_URL = '/static/'
STATICFILES_DIRS =(
    os.path.join(BASE_DIR, 'static'),
)

uploadFilePath = current_env.get_config("uploadFilePath")
