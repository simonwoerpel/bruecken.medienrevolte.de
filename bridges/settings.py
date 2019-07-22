"""
Django settings for bridges project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os


def get_env(x, y=None):
    return os.environ.get(x, y)


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = get_env('DJANGO_DEBUG', 'false') == 'true'

SECRET_KEY = get_env('DJANGO_SECRET_KEY', ')sk24e10sa*a3)x$f123g5i_-6_6tzemdd_+znhv54ki7=c^xc')

# TEMPLATE_DEBUG = False

ALLOWED_HOSTS = [get_env('DJANGO_ALLOWED_HOSTS', '*')]

SITE_ID = 1


# Application definition

INSTALLED_APPS = (
    # 'django.contrib.admin',
    # 'django.contrib.auth',
    'django.contrib.contenttypes',
    # 'django.contrib.sessions',
    'django.contrib.sites',
    # 'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    # 'nvd3',
    'bootstrap3',
    'djgeojson',
    'theme',
    'erm',
    'app',
)

MIDDLEWARE = [
    'django.middleware.cache.UpdateCacheMiddleware',
    # 'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    # 'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    # 'django.contrib.messages.middleware.MessageMiddleware',
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # 'django.template.context_processors.debug',
                'django.template.context_processors.request',
                # 'django.contrib.auth.context_processors.auth',
                # 'django.contrib.messages.context_processors.messages',
            ]
        }
    },
]

ROOT_URLCONF = 'bridges.urls'

WSGI_APPLICATION = 'bridges.wsgi.application'

# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.spatialite',
        'NAME': os.path.join(BASE_DIR, 'db.spatialite'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'de'

TIME_ZONE = 'Europe/Berlin'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

STATIC_ROOT = get_env('STATIC_ROOT', os.path.join(BASE_DIR, '../static'))

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

MEDIA_URL = '/media/'

MEDIA_ROOT = get_env('MEDIA_ROOT', os.path.join(BASE_DIR, 'media'))

# SPATIALITE_LIBRARY_PATH = 'mod_spatialite'

if not DEBUG:
    CACHES = {
        'default': {
            # 'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            # 'LOCATION': '127.0.0.1:11211',
            'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
            'LOCATION': '/tmp/django_cache/bridges',
            'TIMEOUT': None,
            'KEY_PREFIX': 'mr_bridges',
        }
    }


try:
    from .local_settings import *  # noqa
except ImportError:
    pass
