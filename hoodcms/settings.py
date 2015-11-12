
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DEBUG = True

CMS_PERMISSION = True
CMS_TEMPLATES = (
    ('cms/normal.html', 'Normal Page'),
    ('cms/header.html', 'Customer Header Page'),
)

DATE_FORMAT = 'm/d/Y'
TIME_FORMAT = 'H:i'
DATETIME_FORMAT = 'm/d/Y H:i'

ROOT_URLCONF = 'hoodcms.urls'

WSGI_APPLICATION = 'hoodcms.wsgi.application'

SITE_ID = 1
LANGUAGE_CODE = 'en'
USE_TZ = True

LANGUAGES = (
    ('en', 'English'),
    ('es', 'Spanish'),
    ('fr', 'French'),
    ('vi', 'Vietnamese'),
)

CMS_LANGUAGES = {
    'default': {
        'fallbacks': ['en'],
        'public': True,
        'hide_untranslated': False,
        'redirect_on_fallback': False,
    }
}

TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True

# Terminal output for email
SERVER_EMAIL = 'admin@localhost'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Localhost keys, override on live.
RECAPTCHA_USE_SSL = False
RECAPTCHA_PUBLIC_KEY = '6Ldd6OsSAAAAAOOu3QVFc2_pBazt7H8Fuks7hBC3'
RECAPTCHA_PRIVATE_KEY = '6Ldd6OsSAAAAANDyM9FbuAne2b2NKHkkpMWP3wIY'

#
# --- Above this line, settings can be over-ridden for deployment
# 
from hoodcms import *

# Restrict to a specific address
SITE_ROOT = "http://%s" % SITE_ADDRESS
ALLOWED_HOSTS = [SITE_ADDRESS]
EMAIL_SUBJECT_PREFIX = '[%s] ' % SITE_NAME

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

INSTALLED_APPS = (
    'person',

    'django.contrib.admin',
    'django.contrib.sites',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'meetings',
    'hoodcms',
    'cmsextra',

    'registration',
    'social_auth',
    'treebeard',
    'menus',
    'cms',
    'sekizai',
    'bootstrap3',
    'ajax_select',

    'djangocms_text_ckeditor',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    "django.core.context_processors.debug",
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'sekizai.context_processors.sekizai',
    'cms.context_processors.cms_settings',
)

# Place where static files are served in live (not used in dev)
STATIC_ROOT = os.path.join(DATA_PATH, 'static')
STATIC_URL = '/static/'

# Place where files can be uploaded, served in live and dev
MEDIA_ROOT = os.path.join(DATA_PATH, 'media')
MEDIA_URL = '/media/'

BOOTSTRAP3 = {
    'include_jquery': False,
}

AJAX_LOOKUP_CHANNELS = {
    'person_lookup'  : ('meetings.lookups', 'PersonLookup'),
}

FIXTURE_DIRS = (
    'meetings/fixtures/' ,
)

LOGIN_URL          = '/person/user/login/'
LOGIN_ERROR_URL    = '/person/user/login/'
LOGIN_REDIRECT_URL = '/person/user/'

ACCOUNT_ACTIVATION_DAYS = 30
AUTHENTICATION_BACKENDS = (
    'social_auth.backends.twitter.TwitterBackend',
    'social_auth.backends.facebook.FacebookBackend',
    'social_auth.backends.google.GoogleOAuth2Backend',
    'social_auth.backends.yahoo.YahooBackend',
    'social_auth.backends.OpenIDBackend',
    'django.contrib.auth.backends.ModelBackend',
)

