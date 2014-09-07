# -*- coding: utf-8 -*-

# Django settings for cruncy project.
from os.path import join, abspath, dirname

DEBUG = False
TEMPLATE_DEBUG = DEBUG

DIRNAME = abspath(dirname(__file__).decode('utf-8'))

ROOT_DIR = abspath(join(DIRNAME, '../..'))

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {

#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'linkme_db',
#         'USER': 'linkme',
#         'PASSWORD': 'linkme',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }

    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'crunchy_db2',
        'USER': 'crunchy',
        'PASSWORD': 'crunchy',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['*']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = abspath(join(ROOT_DIR, 'static'))

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = [
    abspath(join(ROOT_DIR, 'assets')),
]

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'bs-ll4(fe5aj+q135x1ol+fqfp7t21_6r1!=(q8aqycosvzwwz'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'crunchy.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'crunchy.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.

    abspath(join(ROOT_DIR, 'templates')),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
    'south',
    'api',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'compressor',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
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

CORS_ORIGIN_ALLOW_ALL = True

REST_FRAMEWORK = {

    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
    )
}


# # django-compressor app
COMPRESS_PRECOMPILERS = [
    ('text/less', 'lessc {infile} {outfile}'),
]
COMPRESS_PARSER = 'compressor.parser.HtmlParser'
COMPRESS_OFFLINE = True


# ----------- #
# Twitter API #
# ----------- #

TWITTER_CONSUMER_KEY = 'e5nvCEf47j5gWvSkwnvGRg'
TWITTER_CONSUMER_SECRET = 'epqawTF3DDCa1H6WhhITycZrCSJuJ0bjGl8hpJkEZw'
TWITTER_ACCESS_TOKEN_KEY = '2182812798-Avp4hD5H1T75icyI54BaJAllXTT2AfEIE7e8tUY'
TWITTER_ACCESS_TOKEN_SECRET = 'DEHjdqGee6yPt0vbFSglKs0g0ZB0NTQmYLK9TdFMVOhZq'
TWITTER_GET_USERS_URL = 'https://api.twitter.com/1.1/users/lookup.json?user_id='
TWITTER_AUTH = 'https://api.twitter.com/1.1/account/verify_credentials.json'


# ----------- #
# Monkeylearn API #
# ----------- #
MONKEYLEARN_CLASSIFY_TEXT_URL = 'https://api.monkeylearn.com/api/v1/categorizer/FBaJ7Bzk/classify_text/'
MONKEYLEARN_CLASSIFY_BATCH_TEXT_URL = 'https://api.monkeylearn.com/api/v1/categorizer/FBaJ7Bzk/classify_batch_text/'
MONKEYLEARN_CLASSIFY_LANG_URL = 'https://api.monkeylearn.com/api/v1/categorizer/hDDngsX8/classify_text/'
MONKEYLEARN_AUTHTOKEN = '3e39e12cdc032d3df28ff9179cc9988e01083696'
# MONKEYLEARN_AUTHTOKEN = 'af280d5de7f613a4271f625d3ebb7c79c1b3e1d9'

# ----------- #
# Monkeylearn language detection API #
# ----------- #

MONKEYLEARN_LANG_CLASSIFY_BATCH_TEXT_URL = 'https://api.monkeylearn.com/api/v1/categorizer/hDDngsX8/classify_batch_text/'
MONKEYLEARN_LANG_AUTHTOKEN = '3e39e12cdc032d3df28ff9179cc9988e01083696'






