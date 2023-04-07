"""
Django settings for Tolk project.

Generated by 'django-admin startproject' using Django 2.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""
import os
import dj_database_url
from dotenv import load_dotenv

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# load the environment variables.
load_dotenv(os.path.join(BASE_DIR, ".env"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = int(os.environ.get('DEBUG', default=0))

# HTTPS settings
if os.environ.get('ENV') == 'production':
    # hosts allowed for use with this application
    ALLOWED_HOSTS = [os.environ.get('APP_HOST')]
    # csrf won't work if this is net set.
    CSRF_TRUSTED_ORIGINS = [os.environ.get('APP_ORIGIN')]
    # Set this to True to avoid transmitting the CSRF cookie over HTTP accidentally.
    CSRF_COOKIE_SECURE = True
    # Set this to True to avoid transmitting the session cookie over HTTP accidentally.
    SESSION_COOKIE_SECURE = True

# Application definition
INSTALLED_APPS = [
    # 3rd party
    'daphne',
    'channels',
    'rest_framework',

    # built-in
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',  # 3rd party
    'django.contrib.staticfiles',

    # locals
    'chat.apps.ChatConfig',
    'accounts.apps.AccountsConfig',
    'Authentication.apps.AuthenticationConfig',
    'web_interface.apps.WebInterfaceConfig',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Tolk.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'Tolk.wsgi.application'

ASGI_APPLICATION = "Tolk.asgi.application"

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
DATABASES = {
    'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
}

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files settings
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATIC_URL = '/static/'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'assets'),
)

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = '/media/'

# Authentication Settings
# authentication user model
# https://docs.djangoproject.com/en/2.2/topics/auth/customizing.html
AUTH_USER_MODEL = 'accounts.User'

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

# Channel layers backends
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [
                os.environ.get("CACHE_URL")
            ],
        },
    },
}


# Redis Cache
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.environ.get("CACHE_URL"),
        'TIMEOUT': 60 * 60 * 24,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
        "KEY_PREFIX": "chat"
    },
}

# Rest Framework
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
        'rest_framework.renderers.AdminRenderer',
    ]
}

# **** storage settings ****
if os.environ.get('ENV') == 'production':
    DEFAULT_FILE_STORAGE = 'storages.backends.dropbox.DropBoxStorage'
    DROPBOX_OAUTH2_TOKEN = os.environ.get('DROPBOX_OAUTH2_TOKEN')
    DROPBOX_APP_KEY = os.environ.get('DROPBOX_APP_KEY')
    DROPBOX_APP_SECRET = os.environ.get('DROPBOX_APP_SECRET')
    DROPBOX_OAUTH2_REFRESH_TOKEN=os.environ.get('DROPBOX_OAUTH2_REFRESH_TOKEN')