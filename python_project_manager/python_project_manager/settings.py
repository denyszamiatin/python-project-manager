"""
Django settings for new_site project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=&u1-+^4m$6%ge5bhqnatfy(3m#34ta#68qy5xa)7dcilfg$94'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

TEMPLATE_DIRS = (
	os.path.join(BASE_DIR, 'project_manager\templates'),
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
	'project_manager',
	'modeltranslation',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'python_project_manager.urls'

LOGIN_URL = '/login/'

LOGIN_REDIRECT_URL = '/main/'

WSGI_APPLICATION = 'python_project_manager.wsgi.application'

AUTH_PROFILE_MODULE = 'project_manager.UserProfile'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
		'NAME': 'python_project_manager',
		'USER': 'root',
		'PASSWORD': '1111',
		#'HOST': ,
		#'PORT': ,
    }
#	'reserve': {
#		'ENGINE': 'django.db.backends.mysql',
#        'NAME': os.path.join(BASE_DIR, 'python_project_manager.mysql'),
#	}
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

ugettext = lambda s: s
LANGUAGES = (
	('en', ugettext('English')),
    ('uk', ugettext('Ukrainian')),
)

MODELTRANSLATION_TRANSLATION_FILES = {
	'project_manager.translation',
}

MODELTRANSLATION_DEFAULT_LANGUAGE = 'en'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

MEDIA_ROOT = os.path.join(BASE_DIR, "media")

MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(BASE_DIR, "static")

STATIC_URL = '/static/'

STATICFILES_DIRS = ('python_project_manager/project_manager/static/', )

STATICFILES_FINDERS = {
	'django.contrib.staticfiles.finders.FileSystemFinder',
	'django.contrib.staticfiles.finders.AppDirectoriesFinder',
}
