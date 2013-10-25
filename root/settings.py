# coding=utf-8
__author__ = 'timirlan666@gmail.com'
from os import path

DEBUG = True
TEMPLATE_DEBUG = DEBUG

PROJECT_ROOT = path.abspath(path.join(path.dirname(__file__), '..'))

ADMINS = (
    ('admin', 'timirlan666@gmail.com'),
)
MANAGERS = ADMINS

SECRET_KEY = 'mt%&amp;^9i!9c4-0o030ejv3%+3csif-g62i0qlfnw$a!+9p8%$r@'
ROOT_URLCONF = 'root.urls'

USE_TZ = True
TIME_ZONE = 'Asia/Yekaterinburg'

SITE_ID = 1

USE_I18N = True
USE_L10N = True
LANGUAGE_CODE = 'ru-RU'
LANGUAGES = (
    ('ru-RU', 'Russian'),
    ('en-us', 'English')
)
LOCALE_PATHS = (
    path.join(PROJECT_ROOT, 'locale'),
)


MEDIA_ROOT = path.join(PROJECT_ROOT, 'www', 'media')
MEDIA_URL = '/media/'
STATIC_ROOT = path.join(PROJECT_ROOT, 'www', 'static')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    path.join(PROJECT_ROOT, 'root', 'static'),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

TEMPLATE_DIRS = (
    path.join(PROJECT_ROOT, 'templates').replace('\\','/'),
)
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages"
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'south',
    'debug_toolbar',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

WSGI_APPLICATION = 'root.wsgi.application'

try:
    from local_settings import *
except ImportError:
    print "No local settings found"
    if DEBUG:
        print "Using sqlite3"
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': 'database.sqlite3',
                'USER': '',
                'PASSWORD': '',
                'HOST': '',
                'PORT': '',
            }
        }