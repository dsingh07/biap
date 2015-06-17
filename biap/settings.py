"""
Django settings for biap project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# Create a relative path for static and template directories
import os

templates_dir = "templates"
static_dir = "static"

# Path of current file
BASE_DIR = os.path.dirname(__file__)
CURRENT_PATH = BASE_DIR.replace("\\", "/")

# Main directory
ROOT_PATH = "/".join(CURRENT_PATH.split("/")[0:-1])

DATABASE_PATH = ROOT_PATH + '/sqlite.db'

# Creating a link to static and template directories
TEMPLATE_PATH = os.path.join(ROOT_PATH, templates_dir)
TEMPLATE_PATH = TEMPLATE_PATH.replace("\\", "/")

STATIC_PATH = os.path.join(ROOT_PATH, static_dir)
STATIC_PATH = STATIC_PATH.replace("\\", "/")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# Important apps for locating static directories
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
)

# Email host setup
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'biapalert@gmail.com'
EMAIL_HOST_PASSWORD = 'imperial2014'
EMAIL_PORT = 587
EMAIL_USE_TLS = True


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'c_9&^+ah)0v^2uamkbf*oc*u6v34d3bqm*b-0kfu^3zeh2z0qj'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

TEMPLATE_DIRS = (
    TEMPLATE_PATH,
)

# List of apps available for use by project
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app1',
)

TEMPLATE_CONTEXT_PROCESSORS = (
	"django.contrib.auth.context_processors.auth",
	"django.core.context_processors.request",
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'biap.urls'

WSGI_APPLICATION = 'biap.wsgi.application'

LOGIN_URL = '/login/'


# Database setup for SQLite database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': DATABASE_PATH,
        'TEST_NAME': DATABASE_PATH,
    }
}

DEFAULT_CHARSET = 'utf_8'

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'GMT'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SITE_ID = 1

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATICFILES_DIRS = (
		STATIC_PATH,
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Important files for template directory
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

STATIC_ROOT = ''

# Reference to call static directory
STATIC_URL = '/static/'
